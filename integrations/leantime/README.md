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

| ROOT operation | Leantime method | Credential | Approval |
| --- | --- | --- | --- |
| `list_projects` | `leantime.rpc.projects.getAll` | read | 0 |
| `get_project` | `leantime.rpc.projects.getProject` | read | 0 |
| `list_tasks` | `leantime.rpc.tickets.getAll` | read | 0 |
| `get_task` | `leantime.rpc.tickets.getTicket` | read | 0 |
| `create_task` | `leantime.rpc.tickets.addTicket` | write | 1 |
| `update_task` | `leantime.rpc.tickets.updateTicket` | write | 1 |
| `complete_task` | `leantime.rpc.tickets.updateTicket` | write | 1 |

Contract: `config/integrations/leantime.yaml`

## Status mapping

| ROOT meaning | Leantime field | Value |
| --- | --- | --- |
| done / complete | `status` | `0` |

`complete_task` forces `status: 0`. Callers cannot pass `status`, `userId`, or `rpc_method`.

## Not yet exposed

- update milestone
- arbitrary Leantime service methods
- user / permission administration
