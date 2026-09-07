"""Allowlisted ROOT → n8n → Leantime RPC contract.

Mirrors the Phase 3 n8n workflow rules so Hermes/Phase 4 can reuse them
and so tests can lock the fail-closed behavior without talking to n8n.
"""

from __future__ import annotations

from typing import Any, Mapping

DONE_STATUS = 0
WEBHOOK_PATH = "/webhook/root-leantime-rpc"
AUTH_HEADER = "X-ROOT-TOKEN"

FORBIDDEN_PASSTHROUGH = frozenset({"rpc_method", "method", "userId", "userid", "status"})

OPERATIONS: dict[str, dict[str, Any]] = {
    "list_projects": {
        "approval_level": 0,
        "credential": "read",
        "rpc_method": "leantime.rpc.projects.getAll",
        "required": (),
        "optional": (),
    },
    "get_project": {
        "approval_level": 0,
        "credential": "read",
        "rpc_method": "leantime.rpc.projects.getProject",
        "required": ("project_id",),
        "optional": (),
    },
    "list_tasks": {
        "approval_level": 0,
        "credential": "read",
        "rpc_method": "leantime.rpc.tickets.getAll",
        "required": ("project_id",),
        "optional": (),
    },
    "get_task": {
        "approval_level": 0,
        "credential": "read",
        "rpc_method": "leantime.rpc.tickets.getTicket",
        "required": ("task_id",),
        "optional": (),
    },
    "create_task": {
        "approval_level": 1,
        "credential": "write",
        "rpc_method": "leantime.rpc.tickets.addTicket",
        "required": ("project_id", "title"),
        "optional": ("description",),
    },
    "update_task": {
        "approval_level": 1,
        "credential": "write",
        "rpc_method": "leantime.rpc.tickets.updateTicket",
        "required": ("task_id",),
        "optional": ("title", "description"),
    },
    "complete_task": {
        "approval_level": 1,
        "credential": "write",
        "rpc_method": "leantime.rpc.tickets.updateTicket",
        "required": ("task_id",),
        "optional": (),
    },
}

ALLOWED_OPERATIONS = frozenset(OPERATIONS)


def parse_positive_id(value: Any, field: str) -> int:
    if isinstance(value, bool) or value is None:
        raise ValueError(field)
    if isinstance(value, int):
        parsed = value
    elif isinstance(value, str) and value.strip().isdigit():
        parsed = int(value.strip())
    else:
        raise ValueError(field)
    if parsed <= 0:
        raise ValueError(field)
    return parsed


def build_leantime_rpc(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    """Validate a webhook body and return the outbound Leantime RPC call.

    Never forwards caller-supplied rpc_method, userId, or status.
    complete_task always writes status=DONE_STATUS.
    """
    if not payload or "operation" not in payload or payload.get("operation") in (None, ""):
        return {"ok": False, "error": "missing_operation"}

    operation = payload.get("operation")
    if operation not in OPERATIONS:
        return {"ok": False, "error": "unsupported_operation", "operation": operation}

    forbidden = FORBIDDEN_PASSTHROUGH.intersection(payload.keys())
    if forbidden:
        return {
            "ok": False,
            "error": "forbidden_passthrough",
            "operation": operation,
            "fields": sorted(forbidden),
        }

    spec = OPERATIONS[operation]
    allowed_keys = {"operation", *spec["required"], *spec["optional"]}
    unknown = set(payload.keys()) - allowed_keys
    if unknown:
        return {
            "ok": False,
            "error": "forbidden_passthrough",
            "operation": operation,
            "fields": sorted(unknown),
        }

    try:
        params = _params_for(operation, payload)
    except ValueError:
        return {"ok": False, "error": "invalid_id", "operation": operation}

    values = params.get("values") if isinstance(params, dict) else None
    if operation == "update_task" and isinstance(values, dict) and set(values) == {"id"}:
        return {"ok": False, "error": "missing_update_fields", "operation": operation}

    return {
        "ok": True,
        "operation": operation,
        "approval_level": spec["approval_level"],
        "credential": spec["credential"],
        "rpc_method": spec["rpc_method"],
        "params": params,
    }


def _params_for(operation: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    if operation == "list_projects":
        return {}

    if operation == "get_project":
        return {"id": parse_positive_id(payload.get("project_id"), "project_id")}

    if operation == "list_tasks":
        project_id = parse_positive_id(payload.get("project_id"), "project_id")
        return {"searchCriteria": {"currentProject": project_id}}

    if operation == "get_task":
        return {"id": parse_positive_id(payload.get("task_id"), "task_id")}

    if operation == "create_task":
        values: dict[str, Any] = {
            "projectId": parse_positive_id(payload.get("project_id"), "project_id"),
            "headline": str(payload.get("title") or "").strip(),
            "type": "task",
        }
        if not values["headline"]:
            raise ValueError("title")
        description = payload.get("description")
        if description not in (None, ""):
            values["description"] = str(description)
        return {"values": values}

    if operation == "update_task":
        values: dict[str, Any] = {
            "id": parse_positive_id(payload.get("task_id"), "task_id"),
        }
        if "title" in payload:
            headline = str(payload.get("title") or "").strip()
            if not headline:
                raise ValueError("title")
            values["headline"] = headline
        if "description" in payload:
            values["description"] = str(payload.get("description") or "")
        return {"values": values}

    if operation == "complete_task":
        return {
            "values": {
                "id": parse_positive_id(payload.get("task_id"), "task_id"),
                "status": DONE_STATUS,
            }
        }

    raise AssertionError(f"unhandled operation: {operation}")
