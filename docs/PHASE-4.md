# Phase 4 — Hermes skill → n8n

Status: Complete

## Objective

Give the live `chief` profile a Git-owned Leantime skill that calls the existing n8n RPC contract. Do not bypass that contract.

## In Git

- Skill: `skills/productivity/leantime/SKILL.md`
- CLI: `skills/productivity/leantime/scripts/root_leantime.py`
- Contract: `config/integrations/leantime.yaml` plus `integrations/n8n/leantime_rpc.py`
- Workflow export: `integrations/n8n/workflows/root-leantime-rpc.json`

Allowlisted writes now include optional `priority` (1–5), `tags` (string), and `dateToFinish` (`YYYY-MM-DD` or `""` to clear). `status` and `userId` stay forbidden.

```text
python -m unittest tests.integrations.test_leantime_rpc_contract tests.skills.test_root_leantime
```

## Live on the VPS

`chief` loads the Git-owned skill and calls n8n RPC.

```yaml
skills:
  external_dirs:
    - /home/maqsood/root/root-ai/skills
```

Secrets stay in `~/.hermes/profiles/chief/.env` (`ROOT_N8N_LEANTIME_URL`, `ROOT_N8N_API_KEY`). Not Git.

If the clone is writable by Hermes, `skill_manage` can dirty Git. Make that tree read-only for the Hermes process if you want the repo immutable at runtime.
