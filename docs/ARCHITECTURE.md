# ROOT Architecture

## System

YOU
  |
  +-- Web (Hermes dashboard, Tailscale private)
  +-- Voice (not implemented)
  +-- CLI
  |
  v
ROOT / Hermes (`chief`)
  |
  +-- Personal Execution
  +-- Business Operations
  +-- Research
  +-- Engineering
  +-- Marketing
  +-- Operations
  |
  v
n8n  (allowlisted Leantime RPC + other automations)
  |
  v
Leantime  (projects / tasks source of truth)

Also:

  +-- Git (configuration source of truth)
  +-- Claude Code / Local ROOT Agent (not yet wired)

## Runtime Path (Phase 3)

```text
ROOT / Hermes (`chief`)
        |
        |  POST /webhook/root/leantime/rpc
        |  header: x-root-api-key
        |  body: { operation, params, requestId? }
        v
       n8n
        |
        |  read credential  → list/get + pre-write ticket read
        |  write credential → create/update/complete
        |  unknown operations / arbitrary RPC → rejected
        v
    Leantime JSON-RPC
```

The dashboard binds to `127.0.0.1:9119` and is exposed only on the tailnet via Tailscale Serve. It is not a public internet service.

## Responsibilities

ROOT
- Decision layer
- Prioritization
- Delegation
- Approval management
- Proactive monitoring
- User execution management

Hermes
- Agent runtime
- Sessions
- Profiles (`chief` is the live ROOT profile)
- Skills
- Delegation
- Memory
- Scheduling
- Web dashboard / gateway

Leantime
- Goals
- Projects
- Tasks
- Milestones
- Business planning

n8n
- Deterministic automation
- External integrations
- Scheduled workflows
- Notifications
- Allowlisted Leantime RPC gateway

Git
- ROOT configuration
- Prompts
- Skills
- Integration code
- Deployment configuration

Runtime state and secrets must remain outside Git.
