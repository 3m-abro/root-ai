# Phase 4 — Hermes skill → n8n

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

## Still on the VPS

1. Import/update the live n8n workflow from the Git export. Git JSON does nothing until n8n has the new `Validate Request` node.
2. Clone or `git pull` `root-ai` to `/home/maqsood/root/root-ai`.
3. Merge into `~/.hermes/profiles/chief/config.yaml`:

```yaml
skills:
  external_dirs:
    - /home/maqsood/root/root-ai/skills
```

4. Put secrets only in `~/.hermes/profiles/chief/.env`:

```bash
ROOT_N8N_LEANTIME_URL=https://n8n.maqsoodabro.com/webhook/root/leantime/rpc
ROOT_N8N_API_KEY=<rotated webhook key>
```

```bash
chmod 600 ~/.hermes/profiles/chief/.env
```

5. Verify reads first (`/leantime` or “List my Leantime projects.”). Do not test writes until reads return ClearStack Studio.

If the clone is writable by Hermes, `skill_manage` can dirty Git. Make that tree read-only for the Hermes process if you want the repo immutable at runtime.
