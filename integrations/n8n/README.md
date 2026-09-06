# n8n Integration

n8n is ROOT's deterministic automation layer.

Use n8n for:

- scheduled workflows
- API integrations
- notifications
- data movement
- repetitive deterministic operations
- external service orchestration

ROOT should not reproduce deterministic workflows inside the agent.

## Direction

ROOT -> n8n

ROOT decides when an automation should run.

n8n performs the deterministic workflow.

n8n reports the result back to ROOT.
