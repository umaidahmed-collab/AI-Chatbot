description: Orchestrated workflow for: Create comprehensive backend README.md with architecture, setup, and API documentation
argument-hint: "<task_path>"
---
# Context
This workflow command was dynamically created to orchestrate agents for:

**Create comprehensive backend README.md with architecture, setup, and API documentation**

1. Add project overview and technology stack section
2. Document architecture patterns (layered structure, dependency injection, RAG pipeline)
3. Create detailed setup and installation instructions with prerequisites
4. Document all environment variables with descriptions and example values
5. Document authentication and authorization flow with JWT implementation
6. Document all API endpoints organized by router (auth, users, documents, chat) with request/response examples
7. Document database schema with all models, fields, relationships, and ERD description
8. Document document processing pipeline (upload, text extraction, chunking, embeddings, ChromaDB)
9. Document chat service and RAG integration (vector search, context injection, OpenAI integration)
10. Document error handling patterns and HTTP status codes used
11. Create testing guidelines with pytest examples and fixture usage
12. Add code structure and organization section explaining directory layout
13. Document all dependencies with their purposes organized by category
14. Add development workflow section (running locally, Docker setup, common commands)
15. Include contributing guidelines for backend development (coding standards, PR process)

Parent Task: Create detailed backend programming README

# Workflow
This command orchestrates the following agent sequence:

1. **documentation-analyst-writer** analyzes requirements and current codebase
2. **documentation-analyst-writer** executes: Add project overview and technology stack section
3. **code-reviewer** executes: Document architecture patterns (layered structure, dependency injection, RAG pipeline)
4. **code-reviewer** executes: Create detailed setup and installation instructions with prerequisites
5. **code-reviewer** executes: Document all environment variables with descriptions and example values
6. **code-reviewer** executes: Document authentication and authorization flow with JWT implementation
7. **code-reviewer** executes: Document all API endpoints organized by router (auth, users, documents, chat) with request/response examples
8. **code-reviewer** executes: Document database schema with all models, fields, relationships, and ERD description
9. **code-reviewer** executes: Document document processing pipeline (upload, text extraction, chunking, embeddings, ChromaDB)
10. **code-reviewer** executes: Document chat service and RAG integration (vector search, context injection, OpenAI integration)
11. **code-reviewer** executes: Document error handling patterns and HTTP status codes used
12. **code-reviewer** executes: Create testing guidelines with pytest examples and fixture usage
13. **code-reviewer** executes: Add code structure and organization section explaining directory layout
14. **code-reviewer** executes: Document all dependencies with their purposes organized by category
15. **code-reviewer** executes: Add development workflow section (running locally, Docker setup, common commands)
16. **code-reviewer** executes: Include contributing guidelines for backend development (coding standards, PR process)

# Agents Orchestrated
- **documentation-analyst-writer**: Technical documentation creation
- **code-reviewer**: Quality assurance and code review

**Note**: This command coordinates the agents - it doesn't do the implementation itself.
Each agent brings their specialized expertise to their part of the workflow.

# Artifacts
- Implementation code (from implementation agent)
- Tests (from implementation agent)
- Code review notes (from code-reviewer)
- Documentation updates (if applicable)

# Execution
The workflow runs agents in sequence, with each agent's output feeding into the next step.
Review checkpoints occur between major phases to ensure quality.
