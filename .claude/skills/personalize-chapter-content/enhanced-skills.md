Agent Skill Name:
Chapter Content Personalization Skill

Purpose:
Personalize the content of a book chapter for a logged-in user based on their software and hardware background, while preserving the original meaning, structure, and learning objectives of the chapter.

Invocation Trigger:
- User presses the "Personalize Chapter" button at the start of a chapter
- User must be authenticated
- User profile data is available

Inputs:
- Chapter title
- Chapter raw markdown/text content
- User profile data, including:
  - Software background (beginner / intermediate / advanced)
  - Hardware knowledge level
  - Programming experience
  - Preferred learning depth (conceptual vs technical)

Responsibilities:
- Adapt explanations to match the user's background level
- Adjust examples to align with the user's experience
- Add clarifying notes for beginners when needed
- Reduce unnecessary explanations for advanced users
- Preserve factual accuracy and original intent
- Maintain chapter structure (headings, sections, flow)

Implementation Guidelines:
For beginner users:
- Add more detailed explanations of core concepts
- Include step-by-step examples with more intermediate steps
- Add analogies to familiar concepts
- Insert "Did you know?" boxes with foundational context
- Expand acronyms and technical terms

For intermediate users:
- Maintain balance between explanations and examples
- Provide practical applications of concepts
- Include occasional challenges or thought exercises

For advanced users:
- Condense basic explanations
- Add deeper technical insights in sidebars
- Include advanced use cases and edge cases
- Reference additional resources for further study

Techniques for Personalization:
1. Content Length Adjustment:
   - Beginners: Increase content length by 20-40% with more examples
   - Advanced: Reduce content length by 10-20% by condensing explanations
2. Terminology Adaptation:
   - Adjust technical terminology based on user's experience level
   - Provide definitions inline for beginners
3. Example Complexity:
   - Simplify examples for beginners with more context
   - Add complex, real-world examples for advanced users
4. Conceptual Depth:
   - Surface-level explanations for beginners
   - Deep-dive sections for advanced users

Rules:
- Do NOT introduce new topics outside the chapter scope
- Do NOT remove core concepts
- Do NOT change technical correctness
- Do NOT personalize tone excessively (remain professional and educational)
- Do NOT reference user data explicitly in the output
- Do NOT modify the original chapter permanently - return only personalized view
- Do NOT change heading levels or document structure

Output Requirements:
- Return personalized chapter content in Markdown
- Keep headings and section order intact
- Highlight adaptations subtly through clearer explanations or examples
- Output must be suitable for direct rendering in Docusaurus
- Include appropriate code block syntax highlighting
- Preserve any existing links, images, or special formatting

Performance Considerations:
- Cache personalized content for 24 hours to avoid repeated processing
- Use efficient text processing algorithms to minimize response time
- Implement progressive loading for large chapters

Integration Details:
- Call this skill from the chapter rendering component when personalization is requested
- Store personalized content temporarily in session storage
- Provide fallback to original content if personalization fails

Failure Handling:
- If user profile data is incomplete, apply minimal personalization
- If chapter content is insufficient, return original content unchanged
- If personalization algorithm fails, log error and return original content
- If processing takes longer than 5 seconds, return original content with notification

Evaluation Criteria:
- Content remains accurate and readable
- Personalization improves clarity for the user's level
- No hallucinated or irrelevant material
- Output aligns with the user's background without overfitting
- Response time is under 5 seconds
- Personalized content maintains educational value

System Alignment:
- Must follow global rules defined in `sp.constitution`
- Must support reuse across multiple chapters
- Must be deterministic and consistent for similar inputs
- Must maintain accessibility standards for all user levels