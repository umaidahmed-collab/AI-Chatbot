description: Orchestrated workflow for: Create Pydantic schemas for blog API
argument-hint: "<task_path>"
---
# Context
This workflow command was dynamically created to orchestrate agents for:

**Create Pydantic schemas for blog API**

1. Add AuthorBase, AuthorCreate, Author schemas to schemas.py
2. Add PostBase, PostCreate, PostUpdate, Post schemas to schemas.py
3. Add PostStatus enum to schemas.py
4. Add pagination and filtering request/response schemas

Parent Task: Build REST API endpoints for blog posts

# Workflow
This command orchestrates the following agent sequence:

1. **senior-software-engineer** analyzes requirements and current codebase
2. **senior-software-engineer** executes: Add AuthorBase, AuthorCreate, Author schemas to schemas.py
3. **code-reviewer** executes: Add PostBase, PostCreate, PostUpdate, Post schemas to schemas.py
4. **code-reviewer** executes: Add PostStatus enum to schemas.py
5. **code-reviewer** executes: Add pagination and filtering request/response schemas

# Agents Orchestrated
- **senior-software-engineer**: Primary implementation and coding
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
