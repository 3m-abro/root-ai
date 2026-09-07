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
- skills (runtime copies)
- scheduling
- gateway / dashboard process
- model calls

## What Git owns

- ROOT contracts and policies
- prompts
- worker profile definitions
- integration code

Runtime state stays outside Git. Do not commit `HERMES_HOME`, session DBs, or dashboard secrets.

## Phase 4

Phase 4 adds a Hermes skill/tool on `chief` that calls the n8n Leantime RPC webhook (`POST /webhook/root/leantime/rpc`, header `x-root-api-key`). Hermes still must not receive Leantime API keys or an arbitrary RPC escape hatch.
