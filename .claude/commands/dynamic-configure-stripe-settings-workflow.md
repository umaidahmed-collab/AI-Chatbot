description: Orchestrated workflow for: Configure Stripe settings
argument-hint: "<task_path>"
---
# Context
This workflow command was dynamically created to orchestrate agents for:

**Configure Stripe settings**

1. Add STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY to backend/app/utils/config.py Settings class
2. Add STRIPE_WEBHOOK_SECRET to config for webhook signature verification
3. Add frontend environment variable for publishable key

Parent Task: Build Stripe Checkout Flow

# Workflow
This command orchestrates the following agent sequence:

1. **senior-software-engineer** analyzes requirements and current codebase
2. **senior-software-engineer** executes: Add STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY to backend/app/utils/config.py Settings class
3. **code-reviewer** executes: Add STRIPE_WEBHOOK_SECRET to config for webhook signature verification
4. **code-reviewer** executes: Add frontend environment variable for publishable key

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
