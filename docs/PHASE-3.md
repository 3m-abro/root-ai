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
| `list_projects` | 0 | read | `leantime.rpc.Projects.Projects.getAll` |
| `get_project` | 0 | read | `leantime.rpc.Projects.Projects.getProject` |
| `list_tasks` | 0 | read | `leantime.rpc.Tickets.Tickets.getAll` |
| `get_task` | 0 | read | `leantime.rpc.Tickets.Tickets.getTicket` |
| `create_task` | 1 | write | `leantime.rpc.Tickets.Tickets.addTicket` |
| `update_task` | 1 | write | `leantime.rpc.Tickets.Tickets.updateTicket` |
| `complete_task` | 1 | write | `leantime.rpc.Tickets.Tickets.updateTicket` |

`complete_task` always writes `status: 0` (`done_status`). Caller-supplied `status` is rejected, not forwarded. Writes that omit `description` re-read the ticket first so n8n cannot blank it.

## Contract rules

- Body is `{ operation, params, requestId? }` only
- Missing or unknown `operation` is rejected
- Invalid integer `id` / `projectId` values are rejected
- Arbitrary `rpc_method`, `userId`, and `status` are not passed through
- Read operations use `Leantime Read Header Auth`; writes use `Leantime Write Header Auth`

Webhook: `POST /webhook/root/leantime/rpc`  
Auth header: `x-root-api-key`

Contract source: `config/integrations/leantime.yaml`  
Executable mirror: `integrations/n8n/leantime_rpc.py`  
Tests: `tests/integrations/test_leantime_rpc_contract.py`  
Export: `integrations/n8n/workflows/root-leantime-rpc.json`

```text
python -m unittest tests.integrations.test_leantime_rpc_contract
```

The export contains n8n credential *names/ids*, not secret values. It also contains the Leantime JSON-RPC URL. Do not re-export if the dump includes header values or `pinData` payloads.

The sticky note inside the export is stale (`list_projects` only / HTTP 501). The live `Validate Request` node implements all seven operations.

## Not in this phase

- Hermes skill/tool that calls the webhook (Phase 4)
- Milestone RPC
- Arbitrary Leantime method proxy
