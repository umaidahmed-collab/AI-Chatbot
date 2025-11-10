description: Orchestrated workflow for: Set up Alembic for database migrations
argument-hint: "<task_path>"
---
# Context
This workflow command was dynamically created to orchestrate agents for:

**Set up Alembic for database migrations**

1. Initialize Alembic in backend directory
2. Configure alembic.ini with database URL from settings
3. Update env.py to import Base and models for autogeneration
4. Create initial migration file for blog schema (Author and Post tables)
5. Update README or create migration documentation with setup and run instructions

Parent Task: Create database schema for blog system

# Workflow
This command orchestrates the following agent sequence:

1. **senior-software-engineer** analyzes requirements and current codebase
2. **senior-software-engineer** executes: Initialize Alembic in backend directory
3. **code-reviewer** executes: Configure alembic.ini with database URL from settings
4. **code-reviewer** executes: Update env.py to import Base and models for autogeneration
5. **code-reviewer** executes: Create initial migration file for blog schema (Author and Post tables)
6. **code-reviewer** executes: Update README or create migration documentation with setup and run instructions

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
