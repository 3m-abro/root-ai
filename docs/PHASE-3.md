# Phase 3 — n8n + Leantime RPC

## Objective

Give ROOT a deterministic, allowlisted path to Leantime without putting Leantime credentials in the agent or inventing a parallel task database.

## Runtime path

```text
ROOT / Hermes → n8n → Leantime
```

n8n is the only component that holds Leantime API credentials. Hermes does not call Leantime directly.

## Completed operations

| Operation | Approval | Credential | Leantime RPC |
| --- | --- | --- | --- |
| `list_projects` | 0 | read | `leantime.rpc.projects.getAll` |
| `get_project` | 0 | read | `leantime.rpc.projects.getProject` |
| `list_tasks` | 0 | read | `leantime.rpc.tickets.getAll` |
| `get_task` | 0 | read | `leantime.rpc.tickets.getTicket` |
| `create_task` | 1 | write | `leantime.rpc.tickets.addTicket` |
| `update_task` | 1 | write | `leantime.rpc.tickets.updateTicket` |
| `complete_task` | 1 | write | `leantime.rpc.tickets.updateTicket` |

`complete_task` always writes `status: 0` (`done_status`). Caller-supplied `status` is rejected, not forwarded.

## Contract rules

- Missing `operation` is rejected
- Operations outside the allowlist are rejected
- Invalid `project_id` / `task_id` values are rejected
- Arbitrary `rpc_method`, `userId`, and `status` are not passed through
- Read operations use the read credential; writes use the write credential

Contract source: `config/integrations/leantime.yaml`  
Executable mirror: `integrations/n8n/leantime_rpc.py`  
Tests: `tests/integrations/test_leantime_rpc_contract.py`

```text
python -m unittest tests.integrations.test_leantime_rpc_contract
```

## Workflow export

A live n8n workflow JSON is **not** committed here. n8n credential exports can contain secrets (`docs/SECURITY.md`). Re-export only after stripping credentials, then place it at `integrations/n8n/workflows/root-leantime-rpc.json`.

## Not in this phase

- Hermes skill/tool that calls the webhook (Phase 4)
- Milestone RPC
- Arbitrary Leantime method proxy
