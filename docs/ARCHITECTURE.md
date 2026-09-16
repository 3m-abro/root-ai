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
  +-- Durable profiles
  |     research
  |     engineering
  |     marketing
  |     operations
  |
  +-- Temporary delegate_task children
        narrow specialist tasks
        parallel research
        reviews
        isolated subtasks
  |
  v
n8n  (allowlisted Leantime RPC + other automations)
  |
  v
Leantime  (projects / tasks source of truth)

Also:

  +-- Git (configuration source of truth)
  +-- Engineering Head → approved skills + native Hermes MCPs → task-selected executor
  +-- DeepSeek Harness / other coding runtimes / Local ROOT Agent (not yet wired)

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
- Durable worker profiles (`research`, `engineering`, `marketing`, `operations`)
- Skills
- Delegation (`delegate_task` children are temporary and isolated)
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

## Engineering routing and capabilities

FreeLLMAPI supplies logical routing independently of the coding executor. Engineering
uses `custom:freellmapi` with `auto:tools` for coordination and MCP operations;
`auto:coding` remains the route for coding-focused work. Neither alias grants tools
or approvals. No executor is always available or preferred.

Context7, GitHub read-only, and Playwright are the completed Engineering MCP phase
(see [evidence and next steps](PHASE-6.md)). Temporary Architect, Implementer,
Reviewer, QA, Security, and DevOps roles are mapped in
[the specialist pilot](ENGINEERING-SPECIALISTS.md). They remain bounded children,
not new durable profiles. ROOT dispatches them when Engineering is already a
depth-one child; no nested delegation or permission increase is authorized.

## Organizational Model

Portfolio ownership and shared-department responsibilities are defined in:

prompts/root/PORTFOLIO.md

This document describes runtime architecture only.
