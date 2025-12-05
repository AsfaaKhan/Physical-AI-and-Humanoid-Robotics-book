# Tasks: Physical AI & Humanoid Robotics Book + RAG System

**Feature**: Physical AI & Humanoid Robotics Book with integrated RAG chatbot
**Branch**: `001-ai-robotics-book`
**Spec**: `/specs/001-ai-robotics-book/spec.md`
**Plan**: `/specs/master/plan.md`
**Date**: 2025-12-06

## Implementation Strategy

This project will be implemented in phases following user story priorities. The implementation starts with foundational setup, then progresses through the three primary user stories: (1) Book access and navigation, (2) RAG chatbot functionality, and (3) Context-specific highlighting. Each phase builds upon the previous while maintaining independent testability.

**MVP Scope**: Phases 1-3 (Repository setup, Book structure, and basic RAG functionality) to deliver the core educational content with basic chat capabilities.

## Phase 1: Setup (Project Initialization)

Initialize the repository structure and foundational components.

- [X] T001 Create folder: book/
- [X] T002 Initialize Docusaurus project inside book/: npx create-docusaurus@latest book classic --typescript
- [ ] T003 Create folder: chatbot-backend/
- [ ] T004 Add backend structure: chatbot-backend/app/, chatbot-backend/app/api/, chatbot-backend/app/rag/, chatbot-backend/app/db/
- [ ] T005 Create file: chatbot-backend/requirements.txt with dependencies: fastapi, uvicorn, qdrant-client, psycopg, sqlalchemy, openai, python-dotenv, PyYAML, markdown
- [ ] T006 Create file: chatbot-backend/app/main.py with FastAPI skeleton + health endpoint
- [X] T007 Create .gitignore for repo with Python, Node.js, and IDE exclusions
- [X] T008 Configure basic Docusaurus settings in book/docusaurus.config.js

## Phase 2: Foundational (Blocking Prerequisites)

Establish the foundational book structure and content organization.

- [X] T009 Inside book/docs/, create chapter folders: intro/, module-1-ros2/, module-2-gazebo-unity/, module-3-isaac/, module-4-vla/, capstone/, appendix/, references/
- [ ] T010 Generate index.md files for each folder with placeholder content
- [X] T011 Configure sidebars.js for nested structure following the 4 course modules
- [X] T012 Create README.md describing book structure
- [ ] T013 Create folder: book/static/img/ for media assets
- [ ] T014 Create folder: book/src/components/Chatbot/ for chatbot UI components

## Phase 3: [US1] Reader accesses educational content (Priority: P1)

Implement the core book functionality to provide educational content to readers.

**Goal**: Enable readers to access and navigate the comprehensive technical book on Physical AI & Humanoid Robotics.

**Independent Test**: The book must be fully accessible with all chapters, diagrams, and code examples available to readers. Readers can navigate between chapters and access all content without restrictions.

- [X] T015 [P] [US1] Create: docs/intro/what-is-physical-ai.md with foundational concepts
- [X] T016 [P] [US1] Create: docs/intro/humanoid-roadmap.md with robotics evolution overview
- [X] T017 [P] [US1] Create: docs/module-1-ros2/ros2-basics.md with ROS2 fundamentals
- [X] T018 [P] [US1] Create: docs/module-1-ros2/ros2-nodes.md with node architecture
- [X] T019 [P] [US1] Create: docs/module-1-ros2/ros2-topics.md with topic communication
- [X] T020 [P] [US1] Create: docs/module-1-ros2/ros2-services-actions.md with services and actions
- [X] T021 [P] [US1] Create: docs/module-1-ros2/urdf.md with robot description format
- [X] T022 [P] [US1] Create: docs/module-1-ros2/ros2-control.md with control systems
- [X] T023 [P] [US1] Create: docs/module-2-gazebo-unity/gazebo-basics.md with simulation fundamentals
- [X] T024 [P] [US1] Create: docs/module-2-gazebo-unity/sdf-urdf-import.md with model formats
- [X] T025 [P] [US1] Create: docs/module-2-gazebo-unity/unity-robotics-hub.md with Unity integration
- [X] T026 [P] [US1] Create: docs/module-2-gazebo-unity/ros2-unity-bridge.md with communication protocols
- [X] T027 [P] [US1] Create: docs/module-3-isaac/isaac-intro.md with NVIDIA Isaac overview
- [X] T028 [P] [US1] Create: docs/module-3-isaac/isaac-sim-basics.md with simulation concepts
- [X] T029 [P] [US1] Create: docs/module-3-isaac/isaac-ros.md with Isaac-ROS integration
- [X] T030 [P] [US1] Create: docs/module-3-isaac/vlm-integration.md with vision-language models
- [X] T031 [P] [US1] Create: docs/module-4-vla/vlm-overview.md with vision-language-action systems
- [X] T032 [P] [US1] Create: docs/module-4-vla/transformers-for-robots.md with transformer applications
- [X] T033 [P] [US1] Create: docs/module-4-vla/openvla.md with open VLA frameworks
- [X] T034 [P] [US1] Create: docs/module-4-vla/action-generation.md with action planning
- [X] T035 [P] [US1] Create: docs/capstone/project-overview.md with capstone project description
- [X] T036 [P] [US1] Create: docs/capstone/hardware-design.md with humanoid design principles
- [X] T037 [P] [US1] Create: docs/capstone/software-architecture.md with system architecture
- [X] T038 [P] [US1] Create: docs/capstone/navigation.md with navigation algorithms
- [X] T039 [P] [US1] Create: docs/capstone/perception.md with perception systems
- [X] T040 [P] [US1] Create: docs/capstone/control.md with control systems
- [X] T041 [P] [US1] Create: docs/appendix/glossary.md with technical terms
- [X] T042 [P] [US1] Create: docs/appendix/symbols.md with mathematical notation
- [X] T043 [P] [US1] Create: docs/appendix/resources.md with additional resources
- [X] T044 [P] [US1] Create: docs/references/index.md with citation format guide
- [X] T045 [US1] Add placeholder images for each module in book/static/img/
- [X] T046 [US1] Add mermaid diagram templates inside docs for architecture illustrations
- [X] T047 [US1] Update docusaurus.config.js to include all new documentation pages
- [X] T048 [US1] Test Docusaurus build to ensure all pages are accessible

## Phase 4: [US2] Reader uses RAG chatbot for questions (Priority: P1)

Implement the core RAG functionality to answer questions based on book content.

**Goal**: Provide a RAG chatbot that answers questions based only on book content with proper citations.

**Independent Test**: The RAG chatbot must correctly answer questions based on book content, cite the relevant chapter/section, and properly respond when information isn't available in the book.

- [ ] T049 [P] Create: chatbot-backend/app/rag/chunker.py for text chunking functionality
- [ ] T050 [P] Create: chatbot-backend/app/rag/vector_store.py for Qdrant integration
- [ ] T051 [P] Create: chatbot-backend/app/rag/llm.py for OpenAI/Gemini integration
- [ ] T052 [P] Create: chatbot-backend/app/rag/retriever.py for content retrieval
- [ ] T053 [P] Create: chatbot-backend/app/db/neon.py for database operations
- [ ] T054 [P] Create: chatbot-backend/app/db/logging.py for query logging
- [ ] T055 [P] Create: chatbot-backend/app/api/embed.py for content embedding API
- [ ] T056 [P] Create: chatbot-backend/app/api/search.py for search API
- [ ] T057 [P] Create: chatbot-backend/app/api/chat.py for chat API
- [ ] T058 [US2] Implement text chunking in app/rag/chunker.py with configurable chunk size
- [ ] T059 [US2] Implement Qdrant client wrapper in app/rag/vector_store.py with proper error handling
- [ ] T060 [US2] Implement embedding generation using OpenAI in app/rag/llm.py
- [ ] T061 [US2] Add ingestion script to extract all docs/ markdown text for indexing
- [ ] T062 [US2] Create /search endpoint → vector similarity search in app/api/search.py
- [ ] T063 [US2] Create /chat endpoint → RAG response + citations in app/api/chat.py
- [ ] T064 [US2] Add Neon logging table for conversations, queries, citations in app/db/logging.py
- [ ] T065 [US2] Test RAG functionality with sample queries about ROS2 concepts
- [ ] T066 [US2] Verify citation accuracy in chatbot responses
- [ ] T067 [US2] Test fallback response when information not found in book content

## Phase 5: [US3] Reader highlights text for context-specific answers (Priority: P2)

Enhance the chatbot with the ability to answer questions based on highlighted text context.

**Goal**: Enable readers to highlight text and ask context-specific questions with relevant answers.

**Independent Test**: When text is highlighted and a question is asked, the chatbot must provide answers based only on the highlighted text and surrounding context.

- [ ] T068 [P] Create: book/src/components/Chatbot/ChatbotWidget.jsx with floating widget UI
- [ ] T069 [P] Create: book/src/components/Chatbot/ChatMessage.jsx for message display
- [ ] T070 [P] Create: book/src/components/Chatbot/ChatInput.jsx for user input
- [ ] T071 [P] Create: book/src/components/Chatbot/ChatSidebar.jsx for sidebar interface
- [ ] T072 [P] Create: book/src/components/Chatbot/chatbot.css for styling
- [ ] T073 [P] Create: book/src/config/chatbot.js for API configuration
- [ ] T074 [US3] Add floating widget logic in ChatbotWidget.jsx with open/close functionality
- [ ] T075 [US3] Add "Ask About This Section" highlight action for docs pages
- [ ] T076 [US3] Implement text selection detection and context passing to backend
- [ ] T077 [US3] Add API service in book/src/config/chatbot.js for backend communication
- [ ] T078 [US3] Add global CSS via book/src/css/custom.css for chatbot styling
- [ ] T079 [US3] Update chat API to accept highlighted text context parameter
- [ ] T080 [US3] Test highlight → query → chat response flow with ROS2 topics example
- [ ] T081 [US3] Verify context-specific answers are properly grounded in highlighted text

## Phase 6: Integration & Deployment

Connect frontend to backend and prepare for deployment.

- [ ] T082 Connect frontend to backend API with environment-based configuration
- [ ] T083 Test message → backend RAG → citation → UI flow
- [ ] T084 Add fallback handling when backend is sleeping (Railway/Render)
- [ ] T085 Display sources with clickable chapter links in chat responses
- [ ] T086 Configure GitHub Pages deployment workflow: .github/workflows/deploy-book.yml
- [ ] T087 Set correct baseUrl in docusaurus.config.js for production
- [ ] T088 Deploy FastAPI backend to Railway or Render with environment variables
- [ ] T089 Test production RAG responses and UTF-8 support
- [ ] T090 Test CORS for Docusaurus → API communication

## Phase 7: Testing & Quality Assurance

Implement testing to ensure quality and reliability.

- [ ] T091 Create tests folder: chatbot-backend/tests/
- [ ] T092 Add: test_chunker.py for chunking functionality
- [ ] T093 Add: test_embeddings.py for embedding generation
- [ ] T094 Add: test_retriever.py for content retrieval
- [ ] T095 Add: test_chat_endpoint.py for chat API
- [ ] T096 Create QA prompt set for hallucination testing
- [ ] T097 Benchmark retrieval accuracy (top-k = 3, 5, 7)
- [ ] T098 Test load performance for 100+ queries
- [ ] T099 Verify 80%+ accuracy for book-related questions
- [ ] T100 Verify 100% citation accuracy in responses

## Phase 8: Polish & Cross-Cutting Concerns

Final touches and release preparation.

- [ ] T101 Final proofreading of all chapters for technical accuracy
- [ ] T102 Add acknowledgements page to book
- [ ] T103 Add About the Author page to book
- [ ] T104 Verify all 80+ sources with proper APA citations
- [ ] T105 Add all required diagrams (40+) and code examples (20+) to content
- [ ] T106 Tag repo as v1.0.0
- [ ] T107 Create release notes in GitHub
- [ ] T108 Publish final site + chatbot with full functionality

## Dependencies

- **US1 (P1)** → No dependencies (foundational content)
- **US2 (P1)** → Depends on Phase 1 (backend setup), Phase 2 (content structure)
- **US3 (P2)** → Depends on US1 (content exists), US2 (RAG functionality)

## Parallel Execution Examples

**US1 Parallel Tasks**: T015-T044 can run in parallel as they create independent documentation files in different directories.

**US2 Parallel Tasks**: T049-T057 can run in parallel as they create independent backend modules.

**US3 Parallel Tasks**: T068-T073 can run in parallel as they create independent frontend components.

## Test Cases

**US1 Acceptance Scenarios**:
- Given a user visits the book website, When they browse the table of contents, Then they can access all 4 course modules with detailed content covering ROS2, digital twins, NVIDIA Isaac, and Vision-Language-Action systems.
- Given a user is reading a chapter, When they encounter a code example, Then they can view properly formatted code with explanations and context.

**US2 Acceptance Scenarios**:
- Given a user asks a question about ROS2 nodes from the book, When they submit the query to the chatbot, Then they receive an answer grounded in book content with a citation to the relevant chapter/section.
- Given a user asks a question not covered in the book, When they submit the query to the chatbot, Then they receive a response stating "This topic is not covered in the book."

**US3 Acceptance Scenarios**:
- Given a user highlights a paragraph about ROS2 topics, When they ask a question related to that text, Then the chatbot provides an answer based only on the highlighted content and immediate context.