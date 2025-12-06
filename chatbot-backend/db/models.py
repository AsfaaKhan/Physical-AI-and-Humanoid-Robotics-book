from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    source_url = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    metadata_json = Column(Text)  # Store metadata as JSON string
    chunk_count = Column(Integer, default=0)
    status = Column(String, default="pending")  # pending, processing, completed, failed


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), index=True)
    content = Column(Text)
    chunk_index = Column(Integer)
    embedding_id = Column(String)  # Reference to Qdrant point ID
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    metadata_json = Column(Text)  # Store metadata as JSON string


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String, index=True)
    user_input = Column(Text)
    agent_response = Column(Text)
    citations = Column(Text)  # Store citations as JSON string
    context_used = Column(Text)  # Store context as JSON string
    confidence_estimate = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_log_id = Column(UUID(as_uuid=True), index=True)
    rating = Column(Integer)  # 1-5 scale
    comment = Column(Text)
    is_helpful = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())