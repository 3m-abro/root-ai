# n8n Integration

n8n is ROOT's deterministic automation layer and the Leantime RPC gateway.

Use n8n for:

- scheduled workflows
- API integrations
- notifications
- data movement
- repetitive deterministic operations
- external service orchestration
- allowlisted Leantime JSON-RPC

ROOT should not reproduce deterministic workflows inside the agent.

## Direction

```text
ROOT / Hermes → n8n → Leantime
```

ROOT decides when an automation should run.

n8n performs the deterministic workflow.

n8n reports the result back to ROOT.

## Leantime RPC workflow

Live name: `ROOT - Leantime RPC`

Export (no credential secrets): `integrations/n8n/workflows/root-leantime-rpc.json`

The sticky note in that export is stale. Trust `Validate Request`, not the note.

Webhook path (host is environment-specific):

```text
POST /webhook/root/leantime/rpc
```

### Auth

- Header: `x-root-api-key`
- Value: n8n credential `ROOT Webhook Header Auth`
- Missing or wrong token: n8n rejects before the workflow runs
- Token is never committed

### Request

```json
{
  "operation": "list_tasks",
  "params": { "searchCriteria": { "projectId": 12 } },
  "requestId": "optional-string-max-128"
}
```

Body may contain only `operation`, `params`, and optional `requestId`.

| Operation | `params` |
| --- | --- |
| `list_projects` | `{}` |
| `get_project` | `{ "id": <positive int> }` |
| `list_tasks` | `{ "searchCriteria": { "projectId": <positive int> } }` |
| `get_task` | `{ "id": <positive int> }` |
| `create_task` | `{ "projectId", "headline", "description?", "priority?", "tags?", "dateToFinish?" }` |
| `update_task` | `{ "id", "projectId" }` plus at least one of `headline`, `description`, `priority`, `tags`, `dateToFinish` |
| `complete_task` | `{ "id", "projectId" }` |

IDs must be JSON integers (`Number.isSafeInteger && n > 0`). Strings are rejected. Field names are Leantime's (`headline`, `projectId`, `id`, `dateToFinish`), not ROOT task-schema aliases.

`priority` is an integer `1`–`5`. `tags` is a string. `dateToFinish` is `YYYY-MM-DD`, or `""` to clear `tags` / `dateToFinish`.

### Response

Success:

```json
{
  "ok": true,
  "operation": "list_tasks",
  "requestId": "root-…",
  "data": {},
  "error": null
}
```

Failure:

```json
{
  "ok": false,
  "operation": "delete_project",
  "requestId": "root-…",
  "data": null,
  "error": { "code": "VALIDATION_ERROR", "message": "Unsupported operation." }
}
```

Validation failures are HTTP 400 with `error.code = VALIDATION_ERROR`. Upstream Leantime failures use 404/502 codes from `Normalize Response`.

### Allowlist

Only the seven operations above. n8n maps `operation` → Leantime method internally. Arbitrary `rpc_method` / `method` / `status` / `userId` are rejected.

| Operation | Method |
| --- | --- |
| `list_projects` | `leantime.rpc.Projects.Projects.getAll` |
| `get_project` | `leantime.rpc.Projects.Projects.getProject` |
| `list_tasks` | `leantime.rpc.Tickets.Tickets.getAll` |
| `get_task` | `leantime.rpc.Tickets.Tickets.getTicket` |
| `create_task` | `leantime.rpc.Tickets.Tickets.addTicket` |
| `update_task` | `leantime.rpc.Tickets.Tickets.updateTicket` |
| `complete_task` | `leantime.rpc.Tickets.Tickets.updateTicket` |

### Credentials

| n8n credential | Used for |
| --- | --- |
| `Leantime Read Header Auth` | list/get, plus the pre-write ticket read |
| `Leantime Write Header Auth` | create/update/complete |

Read and write keys are separate. Neither belongs in Git or in Hermes.

The export hardcodes the Leantime JSON-RPC URL. That is environment-specific, not a secret. Credential *values* stay in n8n.

### Fail-closed rules

- Unsupported or missing operation → rejected
- Extra body/param keys → rejected
- Invalid IDs → rejected
- `complete_task` writes `status: 0` itself
- `complete_task` and `update_task` without `description` read the existing ticket first so the write cannot clobber description
- `userId`, `status`, and `rpc_method` from the caller are not forwarded

Executable contract: `integrations/n8n/leantime_rpc.py`
