# ROOT

ROOT is a personal AI operating system and Chief of Staff.

## Current Status

- Phase 0 — repository foundation: complete
- Phase 1 — runtime contracts and policies: complete
- Phase 2 — Hermes runtime: complete (`chief` profile, gateway, dashboard on `127.0.0.1:9119`, private Tailscale Serve)
- Phase 3 — Leantime + n8n integration: complete (allowlisted 7-operation RPC)
- Phase 4 — Hermes skill ? n8n: in progress
- Phase 5 — Worker profiles and delegation: complete
- Phase 6 — Engineering workforce: next

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Core Responsibilities

- Personal execution management
- Business/project orchestration
- AI workforce coordination
- Automation orchestration
- Software development coordination
- Local computer execution
- Proactive monitoring and reporting

## Architecture

- Hermes — agent runtime (`chief` profile)
- Leantime — project/business source of truth
- n8n — deterministic automation and Leantime RPC gateway
- Cursor Agentic Team — organizational/role model
- Cursor AI Dev Agents — engineering workforce
- Claude Code — coding execution
- Local ROOT Agent — local machine execution
- Git — source of truth for ROOT configuration

Live project access path:

`ROOT / Hermes ? n8n (allowlisted RPC) ? Leantime`

Read and write Leantime credentials are separated. Secrets stay in environment / n8n credentials, not Git.

## Design Principle

ROOT decides what should happen.

Workers and tools execute it.

The user remains the final authority for consequential actions.
