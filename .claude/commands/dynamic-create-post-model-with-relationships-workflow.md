description: Orchestrated workflow for: Create Post model with relationships
argument-hint: "<task_path>"
---
# Context
This workflow command was dynamically created to orchestrate agents for:

**Create Post model with relationships**

1. Define Post model class with id, user_id, content, image_url fields
2. Add created_at, updated_at, deleted_at timestamp columns
3. Set up foreign key constraint to users table with proper indexing
4. Add relationship back to User and forward to likes/comments

Parent Task: Create database schema for social media feed

# Workflow
This command orchestrates the following agent sequence:

1. **senior-software-engineer** analyzes requirements and current codebase
2. **senior-software-engineer** executes: Define Post model class with id, user_id, content, image_url fields
3. **code-reviewer** executes: Add created_at, updated_at, deleted_at timestamp columns
4. **code-reviewer** executes: Set up foreign key constraint to users table with proper indexing
5. **code-reviewer** executes: Add relationship back to User and forward to likes/comments

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
