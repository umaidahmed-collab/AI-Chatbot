description: Orchestrated workflow for: Extend User model with social media profile fields
argument-hint: "<task_path>"
---
# Context
This workflow command was dynamically created to orchestrate agents for:

**Extend User model with social media profile fields**

1. Add profile_picture and bio columns to existing User model in backend/app/models/database.py
2. Add soft delete support with deleted_at column to User model
3. Update relationships to include posts, likes, and comments

Parent Task: Create database schema for social media feed

# Workflow
This command orchestrates the following agent sequence:

1. **senior-software-engineer** analyzes requirements and current codebase
2. **senior-software-engineer** executes: Add profile_picture and bio columns to existing User model in backend/app/models/database.py
3. **code-reviewer** executes: Add soft delete support with deleted_at column to User model
4. **code-reviewer** executes: Update relationships to include posts, likes, and comments

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
