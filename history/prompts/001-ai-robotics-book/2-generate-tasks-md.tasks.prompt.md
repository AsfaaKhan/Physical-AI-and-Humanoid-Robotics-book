---
id: 2
title: generate-tasks-md
stage: tasks
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-ai-robotics-book
branch: master
user: Claude
command: /sp.tasks
labels: [tasks, planning, docusaurus, rag, backend]
links:
  spec: E:\HACKATHON-PROJECT\Human-ai-book-Hackathon\specs\001-ai-robotics-book\spec.md
  ticket: null
  adr: null
  pr: null
files:
 - E:\HACKATHON-PROJECT\Human-ai-book-Hackathon\specs\master\tasks.md
tests:
 - E:\HACKATHON-PROJECT\Human-ai-book-Hackathon\specs\master\tasks.md
---

## Prompt

```
PHASE 1 — Repository + Environment Setup
[ ] Create folder: book/
[ ] Initialize Docusaurus project inside book/:
    npx create-docusaurus@latest book classic

[ ] Create folder: chatbot-backend/
[ ] Add backend structure:
    chatbot-backend/app/
    chatbot-backend/app/api/
    chatbot-backend/app/rag/
    chatbot-backend/app/db/

[ ] Create file: chatbot-backend/requirements.txt
[ ] Add dependencies: fastapi, uvicorn, qdrant-client, psycopg, sqlalchemy, openai, python-dotenv

[ ] Create file: chatbot-backend/app/main.py
[ ] Setup FastAPI skeleton + health endpoint

[ ] Create .gitignore for repo

PHASE 2 — Docusaurus Book Structure
[ ] Inside book/docs/, create chapter folders:
    intro/
    module-1-ros2/
    module-2-gazebo-unity/
    module-3-isaac/
    module-4-vla/
    capstone/
    appendix/
    references/

[ ] Generate index.md files for each folder

[ ] Configure sidebars.js for nested structure

[ ] Create README.md describing book structure

PHASE 3 — Chapter Skeleton Generation

INTRODUCTION
[ ] Create: docs/intro/what-is-physical-ai.md
[ ] Create: docs/intro/humanoid-roadmap.md

MODULE 1 — ROS2
[ ] Create: module-1-ros2/ros2-basics.md
[ ] Create: module-1-ros2/ros2-nodes.md
[ ] Create: module-1-ros2/ros2-topics.md
[ ] Create: module-1-ros2/ros2-services-actions.md
[ ] Create: module-1-ros2/urdf.md
[ ] Create: module-1-ros2/ros2-control.md

MODULE 2 — Simulation (Gazebo + Unity)
[ ] Create: module-2-gazebo-unity/gazebo-basics.md
[ ] Create: module-2-gazebo-unity/sdf-urdf-import.md
[ ] Create: module-2-gazebo-unity/unity-robotics-hub.md
[ ] Create: module-2-gazebo-unity/ros2-unity-bridge.md

MODULE 3 — NVIDIA Isaac
[ ] Create: module-3-isaac/isaac-intro.md
[ ] Create: module-3-isaac/isaac-sim-basics.md
[ ] Create: module-3-isaac/isaac-ros.md
[ ] Create: module-3-isaac/vlm-integration.md

MODULE 4 — VLA (Vision-Language-Action)
[ ] Create: module-4-vla/vlm-overview.md
[ ] Create: module-4-vla/transformers-for-robots.md
[ ] Create: module-4-vla/openvla.md
[ ] Create: module-4-vla/action-generation.md

CAPSTONE — Autonomous
[ ] Create: capstone/project-overview.md
[ ] Create: capstone/hardware-design.md
[ ] Create: capstone/software-architecture.md
[ ] Create: capstone/navigation.md
[ ] Create: capstone/perception.md
[ ] Create: capstone/control.md

APPENDIX
[ ] Create: appendix/glossary.md
[ ] Create: appendix/symbols.md
[ ] Create: appendix/resources.md

REFERENCES
[ ] Create: references/index.md

PHASE 4 — Media Assets

[ ] Create folder: book/static/img/
[ ] Add placeholder images for each module
[ ] Add mermaid diagram templates inside docs

PHASE 5 — RAG Backend (FastAPI + Qdrant + Neon)
Backend File Creation:
[ ] Create: app/api/embed.py
[ ] Create: app/api/search.py
[ ] Create: app/api/chat.py

[ ] Create: app/rag/chunker.py
[ ] Create: app/rag/retriever.py
[ ] Create: app/rag/vector_store.py
[ ] Create: app/rag/llm.py

[ ] Create: app/db/neon.py
[ ] Create: app/db/logging.py

Backend Tasks:
[ ] Implement text chunking (chunker.py)
[ ] Implement Qdrant client wrapper (vector_store.py)
[ ] Implement embedding generation using OpenAI
[ ] Add ingestion script to extract all docs/ markdown text
[ ] Create /search endpoint → vector similarity search
[ ] Create /chat endpoint → RAG response + citations
[ ] Add Neon logging table: conversations, queries, citations


PHASE 6 — Chatbot Frontend (Docusaurus UI)
[ ] Create folder: book/src/components/Chatbot/

[ ] Create files:
    ChatbotWidget.jsx
    ChatMessage.jsx
    ChatInput.jsx
    ChatSidebar.jsx
    chatbot.css

[ ] Add floating widget logic
[ ] Add API service file: book/src/config/chatbot.js
[ ] Add global CSS via book/src/css/custom.css

[ ] Add "Ask About This Section" highlight action for docs pages

PHASE 7 — Integration
 [ ] Connect frontend to backend API (env-based switching)
[ ] Test message → backend RAG → citation → UI
[ ] Add fallback when backend is sleeping (Railway/Render)
[ ] Display sources with clickable chapter links
[ ] Test highlight → query → chat response flow

PHASE 8 — Deployment
DOCUSAURUS:
[ ] Configure GitHub Pages deployment workflow:
    .github/workflows/deploy-book.yml

[ ] Set correct baseUrl in docusaurus.config.js

BACKEND:
[ ] Deploy FastAPI to Railway or Render
[ ] Add environment variables:
    OPENAI_API_KEY
    QDRANT_URL
    QDRANT_KEY
    NEON_DB_URL

[ ] Test production RAG responses
[ ] Test UTF-8 support
[ ] Test CORS for Docusaurus → API

PHASE 9 — Testing
[ ] Create tests folder: chatbot-backend/tests/
[ ] Add:
    test_chunker.py
    test_embeddings.py
    test_retriever.py
    test_chat_endpoint.py

[ ] Create QA prompt set for hallucination testing
[ ] Benchmark retrieval accuracy (top-k = 3, 5, 7)
[ ] Test load speed for 100+ queries

PHASE 10 — Final Release
[ ] Final proofreading of all chapters
[ ] Add acknowledgements page
[ ] Add About the Author page
[ ] Tag repo as v1.0.0
[ ] Create release notes in GitHub
[ ] Publish final site + chatbot
```

## Response snapshot

Generated tasks.md file with 108 specific, actionable tasks organized by user story priority. The tasks follow the required checklist format with Task IDs, story labels for user story phases, and specific file paths. The implementation strategy follows the user story priorities from the spec: US1 (P1) - Book access, US2 (P1) - RAG chatbot, US3 (P2) - Context-specific highlighting. Tasks are organized in phases with Phase 1 (Setup), Phase 2 (Foundational), Phases 3-5 (User Stories), Phase 6 (Integration), Phase 7 (Testing), and Phase 8 (Polish).

## Outcome

- ✅ Impact: Created comprehensive task breakdown with 108 specific, actionable items for implementing the Physical AI & Humanoid Robotics Book + RAG System
- 🧪 Tests: Tasks include testing components for RAG accuracy, citation verification, and user story acceptance scenarios
- 📁 Files: Generated E:\HACKATHON-PROJECT\Human-ai-book-Hackathon\specs\master\tasks.md with structured task breakdown
- 🔁 Next prompts: Ready for task execution phase using individual task items
- 🧠 Reflection: Tasks are organized by user story priority to enable independent implementation and testing of each feature

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks follow proper checklist format with IDs, story labels, and file paths
- Graders run and results (PASS/FAIL): PASS - tasks are specific, actionable, and organized by user story
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin executing Phase 1 tasks to set up repository structure