# Hermes Integration

Hermes is ROOT's agent runtime. ROOT does not implement a competing agent framework.

## Live runtime

- Profile: `chief`
- Role mapping: `agents/profiles/root.yaml`
- Gateway: running
- Dashboard: `127.0.0.1:9119`
- Remote access: Tailscale Serve (private tailnet only)

## What Hermes owns

- sessions
- memory
- agent-created / hub-installed skills under `~/.hermes/skills/`
- scheduling
- gateway / dashboard process
- model calls

## What Git owns

- ROOT contracts and policies
- prompts
- worker profile definitions
- integration code
- ROOT Hermes skills under `skills/` (point `chief` at them with `skills.external_dirs`)

Runtime state stays outside Git. Do not commit `HERMES_HOME`, session DBs, or dashboard secrets.

## Phase 4

The Git-owned `leantime` skill is `skills/productivity/leantime/`. `chief` should load it via:

```yaml
skills:
  external_dirs:
    - /home/maqsood/root/root-ai/skills
```

The skill CLI posts `{ operation, params }` to `/webhook/root/leantime/rpc` with header `x-root-api-key` from `ROOT_N8N_API_KEY`. Hermes still must not receive Leantime API keys or an arbitrary RPC escape hatch.
