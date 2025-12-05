<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- Modified principles: All principles added from scratch based on project requirements
- Added sections: Book Development Standards, RAG Chatbot Standards, Technical Constraints, Success Criteria
- Removed sections: None (new constitution)
- Templates requiring updates:
  - ✅ plan-template.md: Constitution Check section exists and will enforce new principles
  - ✅ spec-template.md: Requirements section will align with new principles
  - ✅ tasks-template.md: Task categorization reflects new principle-driven requirements
  - ✅ adr-template.md: Architecture decisions will follow new principles
  - ✅ checklist-template.md: Checklists will verify compliance with new principles
- Follow-up TODOs: None
-->
# Unified Book + RAG System Constitution — "Physical AI & Humanoid Robotics"

## Core Principles

### Accuracy & Reliability
All scientific, technical, and historical claims must come from credible sources (Peer-reviewed research, robotics textbooks, official documentation, standards). All statements must be traceable and verifiable.

### Clarity & Accessibility
Written for readers with CS / AI / engineering backgrounds. Concepts should build progressively from fundamentals → advanced robotics. Use clear explanations, diagrams, and examples to support understanding.

### Reproducibility & Transparency
Algorithms must include explanations + pseudo code or code snippets. Architectural diagrams, control loops, sensor/actuator explanations must be replicable. All citations in consistent APA format.

### Safety & Ethical Responsibility
Include discussions on safety, human-robot interaction, alignment, biases, and limitations. The Chaybot must never output unsafe robotics instructions or hallucinated content.

### Unified Source of Truth
The book's content is the only authoritative dataset used by the Chatbot. RAG system must not use external internet content unless explicitly designed for it.

### Technical Standards Compliance
Minimum sources: 80 (40% peer-reviewed). Zero plagiarism tolerance. Writing clarity: Flesch-Kincaid grade 12 (technical but readable). Markdown format compatible with Docusaurus. Include: diagrams with captions, code examples, tables, architecture sections. Every claim that sounds factual must include citation. Organize book into modular chapters: Fundamentals → AI Systems → Robotics Hardware → Embodiment → Control → Vision → Motion → Ethics → Future Directions.

## Book Development Standards
- Word count target: 70,000–100,000 words.
- Docusaurus build must succeed without errors.
- Deploy via GitHub Pages using GitHub Actions workflow.
- Include diagrams with captions, code examples, tables, architecture sections.
- Organize book into modular chapters covering: Fundamentals → AI Systems → Robotics Hardware → Embodiment → Control → Vision → Motion → Ethics → Future Directions.

## RAG Chatbot Standards
- Retrieval: Qdrant Cloud Free Tier as vector store. Embedding generated from final published book. User-selected text must trigger local-context-only answers.
- Generation: Answers must cite the exact source location (chapter/section). If no relevant information found → respond: "This topic is not covered in the book."
- Safety: Disallow harmful robotics instructions (e.g., weaponization). No hallucinations; bot should clearly state uncertainty.
- System behavior: Answers must be grounded, concise, and technically accurate. Tone: professional technical assistant / tutor.

## Technical Constraints
- Book: Target word count 70,000–100,000 words, Docusaurus compatible, deployable via GitHub Pages.
- Chatbot: Backend: FastAPI. Databases: Neon Serverless Postgres + Qdrant. Integration: OpenAI Agents with Free Gemini 2.5 Flash model / ChatKit SDK. Frontend: JS/React widget embedded inside Docusaurus site.
- Must run on free-tier friendly architecture.
- Sanitize all user inputs.
- No sensitive keys stored in client-side code.
- Follow best practices for API security and environment variables.

## Success Criteria
- BOOK: All chapters complete, coherent, and technically accurate. Claims verified and properly cited. Build passes Docusaurus validation and renders correctly on GitHub Pages. At least one technical reviewer validates core robotics content.
- CHATBOT: Can answer >80% of book-related questions correctly using retrieved context. Always cites chapter/section for source. Correctly handles "not in book" queries. Seamlessly embedded into book UI.
- OVERALL: Unified documentation, clear structure, zero plagiarism, strong technical foundation. Final book + chatbot deployed and publicly accessible on GitHub Pages.

## Governance
This constitution governs all development activities for the Unified Book + RAG System project. All code, documentation, and system design must comply with these principles. Amendments to this constitution require explicit approval and must be documented with clear rationale. All team members must review and acknowledge these principles before contributing to the project. Code reviews must verify compliance with all listed principles. Any conflicts between this constitution and other project documentation must be resolved in favor of this constitution.

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
