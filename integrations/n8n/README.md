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

Workflow name: `root-leantime-rpc`

Webhook path (host is environment-specific, not in Git):

```text
POST /webhook/root-leantime-rpc
```

### Auth

- Header: `X-ROOT-TOKEN`
- Value: environment / n8n credential (`ROOT_N8N_WEBHOOK_TOKEN`)
- Missing or wrong token: reject
- Token is never committed

### Request

```json
{
  "operation": "list_tasks",
  "project_id": 12
}
```

`operation` is required. Additional fields are per-operation only:

| Operation | Fields |
| --- | --- |
| `list_projects` | — |
| `get_project` | `project_id` |
| `list_tasks` | `project_id` |
| `get_task` | `task_id` |
| `create_task` | `project_id`, `title`, `description?` |
| `update_task` | `task_id`, `title?`, `description?` |
| `complete_task` | `task_id` |

### Response

Success:

```json
{
  "ok": true,
  "operation": "list_tasks",
  "result": {}
}
```

Failure:

```json
{
  "ok": false,
  "error": "unsupported_operation",
  "operation": "delete_project"
}
```

Error codes: `missing_operation`, `unsupported_operation`, `invalid_id`, `forbidden_passthrough`.

### Allowlist

Only the seven operations above. Arbitrary `rpc_method` / `method` values are rejected. n8n maps `operation` → Leantime method internally.

### Credentials

| Credential | Used for |
| --- | --- |
| `leantime_read` | list/get |
| `leantime_write` | create/update/complete |

Read and write keys are separate. Neither belongs in Git or in Hermes.

### Fail-closed rules

- Unsupported operation → rejected
- Missing operation → rejected
- Invalid IDs → rejected
- `complete_task` writes `status: 0` itself
- `userId`, `status`, and `rpc_method` from the caller are not forwarded

Executable contract: `integrations/n8n/leantime_rpc.py`
