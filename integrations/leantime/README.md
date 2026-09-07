# Leantime Integration

Leantime is ROOT's source of truth for:

- goals
- projects
- milestones
- tasks
- business planning
- project status

ROOT must not create a parallel project database.

## Direction

```text
ROOT / Hermes → n8n → Leantime
```

Use ROOT to interpret, prioritize and orchestrate.

Use n8n to execute the allowlisted RPC.

Use Leantime to persist project/business state.

Hermes does not hold Leantime API keys.

## Verified RPC methods

From the live n8n workflow (`ROOT - Leantime RPC`):

| ROOT operation | Leantime method | Credential | Approval |
| --- | --- | --- | --- |
| `list_projects` | `leantime.rpc.Projects.Projects.getAll` | read | 0 |
| `get_project` | `leantime.rpc.Projects.Projects.getProject` | read | 0 |
| `list_tasks` | `leantime.rpc.Tickets.Tickets.getAll` | read | 0 |
| `get_task` | `leantime.rpc.Tickets.Tickets.getTicket` | read | 0 |
| `create_task` | `leantime.rpc.Tickets.Tickets.addTicket` | write | 1 |
| `update_task` | `leantime.rpc.Tickets.Tickets.updateTicket` | write | 1 |
| `complete_task` | `leantime.rpc.Tickets.Tickets.updateTicket` | write | 1 |

Contract: `config/integrations/leantime.yaml`

Callers send `{ operation, params, requestId? }` with Leantime field names (`id`, `projectId`, `headline`, `priority`, `tags`, `dateToFinish`). See `integrations/n8n/README.md`.

## Status mapping

| ROOT meaning | Leantime field | Value |
| --- | --- | --- |
| done / complete | `status` | `0` |

`complete_task` forces `status: 0`. Callers cannot pass `status`, `userId`, or `rpc_method`. `complete_task` also requires `projectId` and preserves the existing description via a read-before-write.

## Not yet exposed

- update milestone
- arbitrary Leantime service methods
- user / permission administration
