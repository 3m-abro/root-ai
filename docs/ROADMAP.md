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
| 4 Hermes skill → n8n | complete |
| 5 Worker profiles and delegation | complete |
| 6 Engineering workforce | in progress: MCP complete; curated skills review next |
| 7–10 | not started |

Phase 4 wired the live `chief` profile to the existing n8n Leantime RPC contract. Do not bypass that contract.

## Phase 4 — Hermes skill → n8n

Status: Complete

Live path: `chief` → Git-owned `leantime` skill → n8n allowlisted RPC → Leantime.

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

Status: In progress. See [Phase 6](PHASE-6.md).

1. Native Hermes MCPs: Context7, GitHub read-only, Playwright — complete per runtime report.
2. Curated skills: manifest and review plan prepared; sources and trust review pending.
3. Define temporary Architect, Implementer, Reviewer, QA, Security, DevOps roles.
4. Integrate an approved task-selected executor, potentially DeepSeek Harness.
5. Validate isolated Git, testing, review, approval, and local PC boundaries.

Engineering Head is executor-agnostic. Claude Code, Codex, OpenCode, and Hermes
specialists are possible approved runtimes, not installed or preferred by this plan.
