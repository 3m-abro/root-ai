---
name: leantime
description: Manage ROOT projects and tasks in Leantime through the controlled n8n integration.
version: 1.0.0
platforms: [linux]
metadata:
  hermes:
    tags:
      - root
      - leantime
      - project-management
      - tasks
      - n8n
    category: productivity
    requires_toolsets:
      - terminal
required_environment_variables:
  - name: ROOT_N8N_API_KEY
    prompt: ROOT n8n webhook API key
    help: Header value for x-root-api-key on POST /webhook/root/leantime/rpc. Store in the chief profile .env, never in Git.
    required_for: all Leantime operations
  - name: ROOT_N8N_LEANTIME_URL
    prompt: ROOT n8n Leantime webhook URL
    help: Defaults to https://n8n.maqsoodabro.com/webhook/root/leantime/rpc if unset.
    required_for: overriding the default webhook URL
---

# ROOT Leantime

Use this skill whenever the user asks ROOT to inspect or manage projects and tasks stored in Leantime.

Leantime is the source of truth for project and task state.

Do not maintain a parallel project database.

## Architecture

ROOT must access Leantime only through the controlled n8n integration:

ROOT / Hermes
→ `scripts/root_leantime.py`
→ n8n
→ Leantime JSON-RPC API

Never access the Leantime MySQL database directly.

Never invoke arbitrary Leantime JSON-RPC methods.

## Supported Operations

Read operations:

- list_projects
- get_project
- list_tasks
- get_task

Write operations:

- create_task
- update_task
- complete_task

Only these operations are permitted.

## Approval Policy

Read operations are ROOT approval level 0:

- list_projects
- get_project
- list_tasks
- get_task

Task-management writes are ROOT approval level 1:

- create_task
- update_task
- complete_task

These are internal and reversible operations. Level 1 does not require interactive approval in ROOT policy. Still do not invent extra operations or fields.

## Procedure

Run from this skill directory (`skills/productivity/leantime`):

```bash
python3 scripts/root_leantime.py OPERATION [arguments]
```

### List projects

```bash
python3 scripts/root_leantime.py list_projects
```

### Get project

```bash
python3 scripts/root_leantime.py get_project --id 3
```

### List tasks

```bash
python3 scripts/root_leantime.py list_tasks --project-id 3
```

### Get task

```bash
python3 scripts/root_leantime.py get_task --id 20
```

### Create task

```bash
python3 scripts/root_leantime.py create_task \
  --project-id 3 \
  --headline "Task title" \
  --description "Optional description" \
  --priority 2 \
  --tags "root,integration" \
  --date-to-finish 2026-09-21
```

`--description`, `--priority`, `--tags`, and `--date-to-finish` are optional on create.

### Update task

```bash
python3 scripts/root_leantime.py update_task \
  --id 21 \
  --project-id 3 \
  --headline "Updated title" \
  --priority 1 \
  --tags "clearstack" \
  --date-to-finish 2026-10-01
```

`update_task` requires `--id`, `--project-id`, and at least one of `--headline`, `--description`, `--priority`, `--tags`, `--date-to-finish`.

### Complete task

```bash
python3 scripts/root_leantime.py complete_task \
  --id 21 \
  --project-id 3
```

## Field rules

- IDs (`--id`, `--project-id`) are positive integers, not strings.
- `priority` is an integer `1`–`5` (`1` = Critical, `5` = Lowest).
- `tags` is a string. Use `""` to clear.
- `dateToFinish` / `--date-to-finish` is `YYYY-MM-DD`, or `""` to clear.
- Do not send `status`, `userId`, RPC method names, or any other ticket field.

`complete_task` is mapped by n8n to Leantime status `0` (`Done`). Callers cannot pass status.

Writes that omit `description` re-read the ticket first in n8n so description is not blanked. That includes `update_task` when you only change priority, tags, or due date.

## Safety Rules

Never:

- send arbitrary RPC method names
- accept or forward arbitrary status values
- accept or forward userId
- expose ROOT_N8N_API_KEY
- print credentials
- access Leantime database directly
- bypass n8n validation
- use write operations outside the user's requested project/task context

## Error Handling

n8n returns JSON `{ ok, operation, requestId, data, error }`. Validation failures are HTTP 400 with `error.code = VALIDATION_ERROR`. Upstream Leantime failures use 404/502.

If the API returns:

- `VALIDATION_ERROR`: correct the input. Do not retry with another method or extra fields
- authentication failure: report integration authentication failure without exposing credentials
- task/project not found: report that clearly
- network failure: report n8n/Leantime integration unavailable

Do not attempt to work around capability restrictions.

## Verification

After a write operation, use the corresponding read operation to verify the resulting project/task state.
