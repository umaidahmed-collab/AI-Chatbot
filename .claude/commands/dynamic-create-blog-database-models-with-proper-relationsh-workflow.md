description: Orchestrated workflow for: Create blog database models with proper relationships and indexes
argument-hint: "<task_path>"
---
# Context
This workflow command was dynamically created to orchestrate agents for:

**Create blog database models with proper relationships and indexes**

1. Add Author model to backend/app/models/database.py with fields: id, name, email, bio, profile_picture_url, created_at, updated_at
2. Add Post model to backend/app/models/database.py with fields: id, title, content, author_id (foreign key), published_at, updated_at, status (draft/published), tags, category
3. Define relationship between Author and Post models (one-to-many)
4. Add indexes on author_id, published_at, and status fields in Post model
5. Add unique constraint on Author email field

Parent Task: Create database schema for blog system

# Workflow
This command orchestrates the following agent sequence:

1. **senior-software-engineer** analyzes requirements and current codebase
2. **senior-software-engineer** executes: Add Author model to backend/app/models/database.py with fields: id, name, email, bio, profile_picture_url, created_at, updated_at
3. **code-reviewer** executes: Add Post model to backend/app/models/database.py with fields: id, title, content, author_id (foreign key), published_at, updated_at, status (draft/published), tags, category
4. **code-reviewer** executes: Define relationship between Author and Post models (one-to-many)
5. **code-reviewer** executes: Add indexes on author_id, published_at, and status fields in Post model
6. **code-reviewer** executes: Add unique constraint on Author email field

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
