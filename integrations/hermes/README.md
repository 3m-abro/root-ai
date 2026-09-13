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

## Engineering MCP phase

Engineering now uses this model section in its live profile, as recorded in the
[Phase 6 report](../../docs/PHASE-6.md):

```yaml
model:
  provider: custom:freellmapi
  default: auto:tools
```

This is a partial configuration; preserve the runtime's provider endpoint,
secret handling, and other settings. Session-only model switches do not persist;
verify the restarted profile banner after an authorized configuration change.

Engineering uses native Context7, GitHub read-only, and Playwright MCPs. Keep
GitHub read-only mode plus a narrow read-tool allowlist and least-privilege token.
Do not copy credentials into Git or assume arbitrary YAML environment interpolation.
Use [Engineering SOUL](../../prompts/engineering/SOUL.md) as the Git-owned role source;
live synchronization is a separate deployment step.

The [curated skills directory](../../skills/curated/README.md) contains metadata
only, no loadable SKILL.md files. Do not add unreviewed upstream checkouts to
`skills.external_dirs` or Hermes's auto-loaded skill directories.
