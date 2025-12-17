Agent Skill Name:
Chapter Content Personalization Skill

Purpose:
Personalize the content of a book chapter for a logged-in user based on their software and hardware background, while preserving the original meaning, structure, and learning objectives of the chapter.

Invocation Trigger:
- User presses the “Personalize Chapter” button at the start of a chapter
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
- Adapt explanations to match the user’s background level
- Adjust examples to align with the user’s experience
- Add clarifying notes for beginners when needed
- Reduce unnecessary explanations for advanced users
- Preserve factual accuracy and original intent
- Maintain chapter structure (headings, sections, flow)

Rules:
- Do NOT introduce new topics outside the chapter scope
- Do NOT remove core concepts
- Do NOT change technical correctness
- Do NOT personalize tone excessively (remain professional and educational)
- Do NOT reference user data explicitly in the output

Output Requirements:
- Return personalized chapter content in Markdown
- Keep headings and section order intact
- Highlight adaptations subtly through clearer explanations or examples
- Output must be suitable for direct rendering in Docusaurus

Failure Handling:
- If user profile data is incomplete, apply minimal personalization
- If chapter content is insufficient, return original content unchanged

Evaluation Criteria:
- Content remains accurate and readable
- Personalization improves clarity for the user’s level
- No hallucinated or irrelevant material
- Output aligns with the user’s background without overfitting

System Alignment:
- Must follow global rules defined in `sp.constitution`
- Must support reuse across multiple chapters
- Must be deterministic and consistent for similar inputs