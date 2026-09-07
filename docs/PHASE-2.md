# Phase 2 — Hermes Runtime

## Objective

Run ROOT on Hermes as the agent runtime, with a private dashboard. Hermes is not replaced; ROOT configuration sits on top of it.

## Completed

- Hermes installed on the VPS
- Live profile: `chief` (ROOT role; see `agents/profiles/root.yaml`)
- Hermes gateway running
- Web dashboard bound to `127.0.0.1:9119`
- Private exposure via Tailscale Serve (tailnet only, not Funnel / public internet)
- Runtime state, sessions, and memory kept outside Git

## Dashboard

Hermes' web dashboard defaults to port `9119`.

Local bind:

```text
http://127.0.0.1:9119
```

Remote access is Tailscale Serve → that loopback port. The dashboard must not be opened on the public internet.

## What stays out of Git

- `~/.hermes` / `HERMES_HOME`
- session databases
- memory stores
- dashboard auth secrets
- model API keys

Git holds ROOT contracts, prompts, and policies. Hermes holds live runtime state.

## Not in this phase

- Leantime/n8n skill on Hermes (Phase 4)
- Worker profile execution (Phase 5)
- Public browser UI
- Voice
