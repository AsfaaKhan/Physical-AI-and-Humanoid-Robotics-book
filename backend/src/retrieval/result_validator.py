"""
Result Validator Module for RAG Retrieval Validation

This module handles:
- Validation of retrieval results for relevance and consistency
- Quality metrics calculation
- Consistency checking across multiple queries
- Performance validation
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import time
from collections import defaultdict
import statistics

from src.retrieval.query_processor import RetrievalResult, ContentChunk
from src.utils import setup_logging
from src.retrieval.query_processor import process_query


logger = setup_logging()


@dataclass
class ValidationResult:
    """
    Contains validation metrics and assessment of retrieval quality.
    Based on data-model.md specifications.
    """
    retrieval_result: RetrievalResult
    precision_score: float
    traceability_score: float
    consistency_score: float
    latency_score: float
    overall_quality: float
    validation_details: Dict[str, Any]
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class MetadataFilter:
    """
    Defines criteria for filtering retrieval results by metadata.
    Based on data-model.md specifications.
    """
    field_name: str
    operator: str
    value: Any
    filter_description: str

    def apply(self, data: Dict[str, Any]) -> bool:
        """
        Apply this filter to a data dictionary and return whether it matches.

        Args:
            data: Dictionary of metadata to check against

        Returns:
            True if the data matches this filter, False otherwise
        """
        if self.field_name not in data:
            return False

        data_value = data[self.field_name]

        if self.operator == "equals":
            return data_value == self.value
        elif self.operator == "contains":
            if isinstance(data_value, str) and isinstance(self.value, str):
                return self.value in data_value
            elif isinstance(data_value, list):
                return self.value in data_value
            return False
        elif self.operator == "in":
            if isinstance(self.value, list):
                return data_value in self.value
            return False
        elif self.operator == "not_in":
            if isinstance(self.value, list):
                return data_value not in self.value
            return False
        else:
            # Default to equality check for unknown operators
            return data_value == self.value


def create_metadata_filter(field_name: str, operator: str, value: Any, description: str = None) -> MetadataFilter:
    """
    Factory function to create a MetadataFilter instance.

    Args:
        field_name: Name of the field to filter on
        operator: Operator to use for comparison (e.g., "equals", "contains", "in", "not_in")
        value: Value to compare against
        description: Optional description of the filter

    Returns:
        MetadataFilter instance
    """
    if description is None:
        description = f"Filter {field_name} {operator} {value}"

    return MetadataFilter(
        field_name=field_name,
        operator=operator,
        value=value,
        filter_description=description
    )


def validate_retrieval_result(retrieval_result: RetrievalResult) -> ValidationResult:
    """
    Validate a retrieval result based on multiple quality metrics.

    Args:
        retrieval_result: The retrieval result to validate

    Returns:
        ValidationResult containing all validation metrics
    """
    logger.info("Starting validation of retrieval result...")

    # Calculate individual validation scores
    precision_score = calculate_precision_score(retrieval_result)
    traceability_score = calculate_traceability_score(retrieval_result)
    consistency_score = calculate_consistency_score(retrieval_result)
    latency_score = calculate_latency_score(retrieval_result)

    # Calculate overall quality as average of all scores
    overall_quality = (precision_score + traceability_score + consistency_score + latency_score) / 4.0

    # Create validation details
    validation_details = {
        'precision_details': get_precision_details(retrieval_result),
        'traceability_details': get_traceability_details(retrieval_result),
        'consistency_details': get_consistency_details(retrieval_result),
        'latency_details': get_latency_details(retrieval_result),
        'query_info': {
            'query_text': retrieval_result.query_request.query_text,
            'top_k_requested': retrieval_result.query_request.top_k,
            'num_results_returned': len(retrieval_result.retrieved_chunks),
            'filters_applied': retrieval_result.metadata_filters_applied
        }
    }

    # Create and return validation result
    validation_result = ValidationResult(
        retrieval_result=retrieval_result,
        precision_score=precision_score,
        traceability_score=traceability_score,
        consistency_score=consistency_score,
        latency_score=latency_score,
        overall_quality=overall_quality,
        validation_details=validation_details
    )

    logger.info(f"Validation completed - Overall quality: {overall_quality:.3f}")
    return validation_result


def calculate_precision_score(retrieval_result: RetrievalResult) -> float:
    """
    Calculate precision score based on relevance of retrieved chunks.

    Args:
        retrieval_result: The retrieval result to evaluate

    Returns:
        Precision score between 0.0 and 1.0
    """
    if len(retrieval_result.retrieved_chunks) == 0:
        return 0.0

    # For now, we'll calculate precision based on relevance scores
    # In a real system, we'd compare against ground truth
    relevance_scores = [chunk.relevance_score for chunk in retrieval_result.retrieved_chunks]

    # Calculate mean relevance score as proxy for precision
    avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0

    # Normalize to 0-1 scale (assuming relevance scores are already normalized)
    # In a real system, we'd have more sophisticated evaluation
    precision = min(1.0, max(0.0, avg_relevance))

    return precision


def calculate_traceability_score(retrieval_result: RetrievalResult) -> float:
    """
    Calculate traceability score based on ability to link results back to source URLs.

    Args:
        retrieval_result: The retrieval result to evaluate

    Returns:
        Traceability score between 0.0 and 1.0
    """
    if len(retrieval_result.retrieved_chunks) == 0:
        return 0.0

    # Count chunks with valid source URLs
    valid_source_count = 0
    for chunk in retrieval_result.retrieved_chunks:
        if chunk.source_url and chunk.source_url.strip() != "":
            valid_source_count += 1

    # Calculate traceability as percentage of chunks with valid sources
    traceability = valid_source_count / len(retrieval_result.retrieved_chunks)
    return traceability


def calculate_consistency_score(retrieval_result: RetrievalResult) -> float:
    """
    Calculate consistency score based on stability of results.
    This is a simplified version - in practice, you'd run the same query multiple times.

    Args:
        retrieval_result: The retrieval result to evaluate

    Returns:
        Consistency score between 0.0 and 1.0
    """
    # For now, we'll calculate based on variance in relevance scores
    # Lower variance indicates more consistent results
    if len(retrieval_result.retrieved_chunks) < 2:
        # Can't calculate variance with less than 2 items
        return 1.0  # Perfect consistency by default for single results

    relevance_scores = [chunk.relevance_score for chunk in retrieval_result.retrieved_chunks]

    # Calculate standard deviation as measure of consistency
    mean_score = sum(relevance_scores) / len(relevance_scores)
    variance = sum((score - mean_score) ** 2 for score in relevance_scores) / len(relevance_scores)
    std_dev = variance ** 0.5

    # Convert to consistency score (inverse relationship with variance)
    # Assuming max possible std dev is 0.5 (half the range 0-1)
    max_possible_std_dev = 0.5
    consistency = max(0.0, 1.0 - (std_dev / max_possible_std_dev))

    return consistency


def calculate_latency_score(retrieval_result: RetrievalResult) -> float:
    """
    Calculate latency score based on retrieval time performance.

    Args:
        retrieval_result: The retrieval result to evaluate

    Returns:
        Latency score between 0.0 and 1.0
    """
    # Target: <2 seconds for 95% of queries (from success criteria)
    target_ms = 2000.0  # 2 seconds in milliseconds

    # Higher score for lower latency, with 1.0 for perfect performance
    if retrieval_result.retrieval_time_ms <= 0:
        return 1.0  # If no time recorded, assume best case

    # Score decreases as latency increases
    # Using inverse relationship with some smoothing
    latency_ratio = retrieval_result.retrieval_time_ms / target_ms
    latency_score = max(0.0, min(1.0, 1.0 - (latency_ratio - 1.0) * 0.5))  # Gentle penalty beyond target

    return max(0.0, latency_score)


def get_precision_details(retrieval_result: RetrievalResult) -> Dict[str, Any]:
    """
    Get detailed information about precision calculation.

    Args:
        retrieval_result: The retrieval result to analyze

    Returns:
        Dictionary with precision-related details
    """
    if len(retrieval_result.retrieved_chunks) == 0:
        return {'message': 'No chunks to evaluate'}

    relevance_scores = [chunk.relevance_score for chunk in retrieval_result.retrieved_chunks]

    details = {
        'avg_relevance_score': sum(relevance_scores) / len(relevance_scores),
        'min_relevance_score': min(relevance_scores),
        'max_relevance_score': max(relevance_scores),
        'relevance_variance': statistics.pvariance(relevance_scores) if len(relevance_scores) > 1 else 0,
        'relevance_std_dev': statistics.pstdev(relevance_scores) if len(relevance_scores) > 1 else 0,
        'num_chunks_evaluated': len(relevance_scores)
    }

    return details


def get_traceability_details(retrieval_result: RetrievalResult) -> Dict[str, Any]:
    """
    Get detailed information about traceability calculation.

    Args:
        retrieval_result: The retrieval result to analyze

    Returns:
        Dictionary with traceability-related details
    """
    details = {
        'total_chunks': len(retrieval_result.retrieved_chunks),
        'chunks_with_valid_source': 0,
        'chunks_without_source': 0,
        'sources': set()
    }

    for chunk in retrieval_result.retrieved_chunks:
        if chunk.source_url and chunk.source_url.strip() != "":
            details['chunks_with_valid_source'] += 1
            details['sources'].add(chunk.source_url)
        else:
            details['chunks_without_source'] += 1

    details['sources'] = list(details['sources'])
    details['traceability_percentage'] = (details['chunks_with_valid_source'] / details['total_chunks']) * 100 if details['total_chunks'] > 0 else 0

    return details


def get_consistency_details(retrieval_result: RetrievalResult) -> Dict[str, Any]:
    """
    Get detailed information about consistency calculation.

    Args:
        retrieval_result: The retrieval result to analyze

    Returns:
        Dictionary with consistency-related details
    """
    if len(retrieval_result.retrieved_chunks) == 0:
        return {'message': 'No chunks to evaluate'}

    relevance_scores = [chunk.relevance_score for chunk in retrieval_result.retrieved_chunks]

    details = {
        'num_chunks_evaluated': len(relevance_scores),
        'relevance_scores': relevance_scores,
        'mean_relevance': sum(relevance_scores) / len(relevance_scores),
        'relevance_variance': statistics.pvariance(relevance_scores) if len(relevance_scores) > 1 else 0,
        'relevance_std_dev': statistics.pstdev(relevance_scores) if len(relevance_scores) > 1 else 0
    }

    return details


def get_latency_details(retrieval_result: RetrievalResult) -> Dict[str, Any]:
    """
    Get detailed information about latency calculation.

    Args:
        retrieval_result: The retrieval result to analyze

    Returns:
        Dictionary with latency-related details
    """
    details = {
        'retrieval_time_ms': retrieval_result.retrieval_time_ms,
        'target_time_ms': 2000.0,  # 2 seconds target
        'is_within_target': retrieval_result.retrieval_time_ms <= 2000.0,
        'latency_ratio': retrieval_result.retrieval_time_ms / 2000.0
    }

    return details


def validate_retrieval_consistency(query_text: str, num_runs: int = 5, top_k: int = 5) -> float:
    """
    Validate consistency by running the same query multiple times and comparing results.

    Args:
        query_text: Query text to test for consistency
        num_runs: Number of times to run the query
        top_k: Number of results to retrieve each time

    Returns:
        Consistency score based on result stability across runs
    """
    logger.info(f"Validating consistency over {num_runs} runs for query: {query_text[:50]}...")

    from src.retrieval.query_processor import process_query

    run_results = []
    for run_idx in range(num_runs):
        try:
            result = process_query(query_text, top_k=top_k)
            run_results.append(result)
            logger.debug(f"Run {run_idx + 1} completed with {len(result.retrieved_chunks)} results")
        except Exception as e:
            logger.error(f"Run {run_idx + 1} failed: {str(e)}")
            # Add empty result to maintain count
            run_results.append(None)

    # Calculate consistency across runs
    if not run_results or all(result is None for result in run_results):
        return 0.0

    # Count successful runs
    successful_runs = [r for r in run_results if r is not None]
    if not successful_runs:
        return 0.0

    # Calculate consistency as percentage of runs that produced same number of results
    result_counts = [len(r.retrieved_chunks) for r in successful_runs]
    mode_count = max(set(result_counts), key=result_counts.count)
    consistency_runs = sum(1 for count in result_counts if count == mode_count)

    consistency_score = consistency_runs / len(successful_runs)

    logger.info(f"Consistency validation completed: {consistency_score:.3f} ({consistency_runs}/{len(successful_runs)} runs consistent)")
    return consistency_score


def validate_metadata_filtering(filters: Dict[str, Any], expected_count_range: tuple = (1, 10)) -> Dict[str, Any]:
    """
    Validate that metadata filtering works correctly.

    Args:
        filters: Metadata filters to test
        expected_count_range: Tuple of (min, max) expected results

    Returns:
        Dictionary with validation results
    """
    logger.info(f"Validating metadata filtering with filters: {filters}")

    from src.retrieval.query_processor import process_query

    try:
        # Use a generic query to test filtering
        result = process_query("test query for filtering validation", top_k=20, filters=filters)

        actual_count = len(result.retrieved_chunks)
        min_expected, max_expected = expected_count_range

        is_in_range = min_expected <= actual_count <= max_expected
        is_filtered = len(filters) > 0  # Should have applied filters

        validation_result = {
            'filters_applied': filters,
            'actual_result_count': actual_count,
            'expected_range': expected_count_range,
            'is_in_range': is_in_range,
            'is_filtered': is_filtered,
            'success': is_in_range and is_filtered,
            'message': f"Got {actual_count} results, expected {min_expected}-{max_expected}"
        }

        logger.info(f"Metadata filtering validation: {'SUCCESS' if validation_result['success'] else 'FAILED'} - {validation_result['message']}")
        return validation_result

    except Exception as e:
        logger.error(f"Metadata filtering validation failed: {str(e)}")
        return {
            'filters_applied': filters,
            'error': str(e),
            'success': False,
            'message': f"Validation failed with error: {str(e)}"
        }


def validate_precision_with_sample_queries() -> Dict[str, Any]:
    """
    Validate precision using sample queries with known expected results.

    Returns:
        Dictionary with precision validation results
    """
    logger.info("Validating precision with sample queries...")

    # Sample queries with expected characteristics
    sample_queries = [
        ("What is Physical AI?", 5),
        ("ROS2 basics", 5),
        ("humanoid robotics", 5),
        ("machine learning concepts", 5),
    ]

    precision_results = []

    for query, top_k in sample_queries:
        try:
            result = process_query(query, top_k=top_k)
            precision = calculate_precision_score(result)
            precision_results.append({
                'query': query,
                'precision': precision,
                'num_results': len(result.retrieved_chunks)
            })
            logger.debug(f"Query '{query}' precision: {precision:.3f}")
        except Exception as e:
            logger.error(f"Precision validation failed for query '{query}': {str(e)}")
            precision_results.append({
                'query': query,
                'precision': 0.0,
                'num_results': 0,
                'error': str(e)
            })

    # Calculate overall precision
    valid_results = [r for r in precision_results if 'error' not in r]
    if valid_results:
        avg_precision = sum(r['precision'] for r in valid_results) / len(valid_results)
    else:
        avg_precision = 0.0

    validation_result = {
        'sample_queries_tested': len(sample_queries),
        'successful_queries': len(valid_results),
        'average_precision': avg_precision,
        'individual_results': precision_results,
        'success': avg_precision >= 0.5  # Arbitrary threshold for validation
    }

    logger.info(f"Precision validation completed - Average: {avg_precision:.3f}")
    return validation_result


def generate_validation_report(validation_result: ValidationResult) -> str:
    """
    Generate a human-readable validation report.

    Args:
        validation_result: The validation result to report on

    Returns:
        Formatted validation report string
    """
    report = f"""
RETRIEVAL VALIDATION REPORT
==========================

Timestamp: {validation_result.timestamp}
Query: "{validation_result.retrieval_result.query_request.query_text}"

QUALITY METRICS:
- Precision Score: {validation_result.precision_score:.3f}
- Traceability Score: {validation_result.traceability_score:.3f}
- Consistency Score: {validation_result.consistency_score:.3f}
- Latency Score: {validation_result.latency_score:.3f}
- Overall Quality: {validation_result.overall_quality:.3f}

DETAILED RESULTS:
- Retrieved {len(validation_result.retrieval_result.retrieved_chunks)} chunks in {validation_result.retrieval_result.retrieval_time_ms:.2f}ms
- Requested top-{validation_result.retrieval_result.query_request.top_k} results
- Applied filters: {bool(validation_result.retrieval_result.metadata_filters_applied)}

VALIDATION STATUS: {'PASS' if validation_result.overall_quality >= 0.7 else 'WARNING' if validation_result.overall_quality >= 0.5 else 'FAIL'}
"""
    return report


if __name__ == "__main__":
    # Example usage would require actual retrieval results
    print("Result validator module - requires actual retrieval results to test")