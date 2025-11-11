description: Orchestrated workflow for: Add payment and email tracking database models
argument-hint: "<task_path>"
---
# Context
This workflow command was dynamically created to orchestrate agents for:

**Add payment and email tracking database models**

1. Add Payment model to database.py with fields: id, user_id, stripe_payment_id, amount, currency, status, payment_method, created_at
2. Add EmailReceipt model with fields: id, payment_id, recipient_email, sent_at, status (pending/sent/failed), retry_count, error_message
3. Add relationships between User, Payment, and EmailReceipt models
4. Create Alembic migration for new tables

Parent Task: Implement Email Receipt System

# Workflow
This command orchestrates the following agent sequence:

1. **senior-software-engineer** analyzes requirements and current codebase
2. **senior-software-engineer** executes: Add Payment model to database.py with fields: id, user_id, stripe_payment_id, amount, currency, status, payment_method, created_at
3. **code-reviewer** executes: Add EmailReceipt model with fields: id, payment_id, recipient_email, sent_at, status (pending/sent/failed), retry_count, error_message
4. **code-reviewer** executes: Add relationships between User, Payment, and EmailReceipt models
5. **code-reviewer** executes: Create Alembic migration for new tables

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
