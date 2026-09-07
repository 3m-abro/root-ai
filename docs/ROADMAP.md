# ROADMAP

```text
Phase 0   Foundation
Phase 1   Runtime contracts/policies
Phase 2   Hermes + private dashboard
Phase 3   n8n + Leantime integration
Phase 4   Hermes skill → n8n
Phase 5   Worker profiles and delegation
Phase 6   Engineering workforce
Phase 7   Local PC Agent
Phase 8   Event-driven automation
Phase 9   Voice
Phase 10  Autonomous operating loop
```

## Status

| Phase | State |
| --- | --- |
| 0 Foundation | complete |
| 1 Runtime contracts/policies | complete |
| 2 Hermes + private dashboard | complete |
| 3 n8n + Leantime integration | complete |
| 4 Hermes skill → n8n | in progress |
| 5 Worker profiles and delegation | complete |
| 6 Engineering workforce | next |
| 7–10 | not started |

Phase 4 wires the live `chief` profile to the existing n8n Leantime RPC contract. Do not bypass that contract for a demo.

## Phase 5 — Worker Profiles and Delegation

Status: Complete

Implemented:

- research profile
- engineering profile
- marketing profile
- operations profile
- ROOT worker routing
- Hermes child-agent delegation
- delegation output limits
- max-depth policy
- ROOT synthesis responsibility

Design principle:

Use a small number of durable high-level worker profiles.

Use temporary child agents for narrow specialist tasks.

Do not create dozens of permanent Hermes profiles.

## Phase 6 — Engineering Workforce

Status: Next

Goals:

- connect engineering profile to Claude Code
- integrate cursor-ai-dev-agents
- define Git workflow
- define testing workflow
- define code review workflow
- define approval gates
- prepare controlled local PC execution
