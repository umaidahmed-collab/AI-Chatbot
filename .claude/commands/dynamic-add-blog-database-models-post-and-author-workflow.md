description: Orchestrated workflow for: Add blog database models (Post and Author)
argument-hint: "<task_path>"
---
# Context
This workflow command was dynamically created to orchestrate agents for:

**Add blog database models (Post and Author)**

1. Add Author model to database.py with fields: id, name, email, bio, created_at
2. Add Post model to database.py with fields: id, author_id, title, content, status, created_at, updated_at
3. Add relationship between Author and Post models
4. Add status enum values: draft, published, archived

Parent Task: Build REST API endpoints for blog posts

# Workflow
This command orchestrates the following agent sequence:

1. **senior-software-engineer** analyzes requirements and current codebase
2. **senior-software-engineer** executes: Add Author model to database.py with fields: id, name, email, bio, created_at
3. **code-reviewer** executes: Add Post model to database.py with fields: id, author_id, title, content, status, created_at, updated_at
4. **code-reviewer** executes: Add relationship between Author and Post models
5. **code-reviewer** executes: Add status enum values: draft, published, archived

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
