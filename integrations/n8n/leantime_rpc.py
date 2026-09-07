"""Allowlisted ROOT → n8n → Leantime RPC contract.

Port of the Validate Request node in
integrations/n8n/workflows/root-leantime-rpc.json.
Do not invent a parallel request shape for Phase 4.
"""

from __future__ import annotations

from typing import Any, Mapping

DONE_STATUS = 0
WEBHOOK_PATH = "/webhook/root/leantime/rpc"
AUTH_HEADER = "x-root-api-key"
MAX_SAFE_INTEGER = 9007199254740991
BODY_KEYS = ("operation", "params", "requestId")
WRITE_OPERATIONS = frozenset({"create_task", "update_task", "complete_task"})

OPERATIONS: dict[str, dict[str, Any]] = {
    "list_projects": {
        "approval_level": 0,
        "credential": "read",
        "rpc_method": "leantime.rpc.Projects.Projects.getAll",
    },
    "get_project": {
        "approval_level": 0,
        "credential": "read",
        "rpc_method": "leantime.rpc.Projects.Projects.getProject",
    },
    "list_tasks": {
        "approval_level": 0,
        "credential": "read",
        "rpc_method": "leantime.rpc.Tickets.Tickets.getAll",
    },
    "get_task": {
        "approval_level": 0,
        "credential": "read",
        "rpc_method": "leantime.rpc.Tickets.Tickets.getTicket",
    },
    "create_task": {
        "approval_level": 1,
        "credential": "write",
        "rpc_method": "leantime.rpc.Tickets.Tickets.addTicket",
    },
    "update_task": {
        "approval_level": 1,
        "credential": "write",
        "rpc_method": "leantime.rpc.Tickets.Tickets.updateTicket",
    },
    "complete_task": {
        "approval_level": 1,
        "credential": "write",
        "rpc_method": "leantime.rpc.Tickets.Tickets.updateTicket",
    },
}

ALLOWED_OPERATIONS = frozenset(OPERATIONS)


def is_object(value: Any) -> bool:
    return isinstance(value, dict)


def own(obj: Mapping[str, Any], key: str) -> bool:
    return key in obj


def keys_allowed(obj: Mapping[str, Any], allowed: tuple[str, ...]) -> bool:
    return all(key in allowed for key in obj)


def positive_id(value: Any) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, int):
        return 0 < value <= MAX_SAFE_INTEGER
    if isinstance(value, float) and value.is_integer():
        return 0 < value <= MAX_SAFE_INTEGER
    return False


def as_id(value: Any) -> int:
    return int(value)


def validate_request(
    body: Mapping[str, Any] | None, *, execution_id: str = "local"
) -> dict[str, Any]:
    """Validate a webhook JSON body the same way n8n Validate Request does."""
    operation = (
        body.get("operation")
        if is_object(body) and isinstance(body.get("operation"), str)
        else None
    )
    if is_object(body) and own(body, "requestId"):
        request_id: Any = body["requestId"]
    else:
        request_id = f"root-{execution_id}"

    def fail(message: str) -> dict[str, Any]:
        return {
            "ok": False,
            "valid": False,
            "httpStatus": 400,
            "response": {
                "ok": False,
                "operation": operation,
                "requestId": request_id,
                "data": None,
                "error": {"code": "VALIDATION_ERROR", "message": message},
            },
        }

    if not (
        isinstance(request_id, str)
        and request_id.strip()
        and len(request_id) <= 128
    ):
        request_id = None
        return fail(
            "requestId, when supplied, must be a nonempty string of at most 128 characters."
        )

    if not is_object(body) or not keys_allowed(body, BODY_KEYS):
        return fail("Body must contain only operation, params, and optional requestId.")
    if operation not in OPERATIONS:
        return fail("Unsupported operation.")

    params_in = body.get("params")
    if not is_object(params_in):
        return fail("params must be a JSON object.")

    try:
        params = _rpc_params(operation, params_in)
    except ValueError as exc:
        return fail(str(exc))

    spec = OPERATIONS[operation]
    return {
        "ok": True,
        "valid": True,
        "operation": operation,
        "requestId": request_id,
        "write": operation in WRITE_OPERATIONS,
        "approval_level": spec["approval_level"],
        "credential": spec["credential"],
        "rpc_method": spec["rpc_method"],
        "params": params,
        "rpc": {
            "jsonrpc": "2.0",
            "method": spec["rpc_method"],
            "params": params,
            "id": request_id,
        },
    }


def needs_description_read(validated: Mapping[str, Any]) -> bool:
    """True when n8n reads the existing ticket before writing."""
    if not validated.get("ok"):
        return False
    operation = validated["operation"]
    values = validated.get("rpc", {}).get("params", {}).get("values", {})
    return operation == "complete_task" or (
        operation == "update_task" and "description" not in values
    )


def _rpc_params(operation: str, params: Mapping[str, Any]) -> dict[str, Any]:
    if operation == "list_projects":
        if not keys_allowed(params, ()):
            raise ValueError("list_projects requires params: {}.")
        return {}

    if operation in {"get_project", "get_task"}:
        if not keys_allowed(params, ("id",)) or not positive_id(params.get("id")):
            raise ValueError("Requires only a positive integer id.")
        return {"id": as_id(params["id"])}

    if operation == "list_tasks":
        criteria = params.get("searchCriteria")
        if (
            not keys_allowed(params, ("searchCriteria",))
            or not is_object(criteria)
            or not keys_allowed(criteria, ("projectId",))
            or not positive_id(criteria.get("projectId"))
        ):
            raise ValueError(
                "Requires only searchCriteria.projectId as a positive integer."
            )
        return {"searchCriteria": {"projectId": as_id(criteria["projectId"])}}

    if operation in {"create_task", "update_task", "complete_task"}:
        return _write_params(operation, params)

    raise AssertionError(f"unhandled operation: {operation}")


def _write_params(operation: str, params: Mapping[str, Any]) -> dict[str, Any]:
    create = operation == "create_task"
    complete = operation == "complete_task"
    if complete:
        allowed = ("id", "projectId")
    elif create:
        allowed = ("projectId", "headline", "description")
    else:
        allowed = ("id", "projectId", "headline", "description")

    if not keys_allowed(params, allowed):
        raise ValueError(
            "Unsupported parameter; raw RPC, status, userId and other fields are forbidden."
        )
    if not positive_id(params.get("projectId")) or (
        not create and not positive_id(params.get("id"))
    ):
        raise ValueError(
            "projectId and, for update/complete, id must be positive integers."
        )
    if (create or own(params, "headline")) and (
        not isinstance(params.get("headline"), str) or not params["headline"].strip()
    ):
        raise ValueError("headline must be a nonempty string.")
    if own(params, "description") and not isinstance(params.get("description"), str):
        raise ValueError("description must be a string; use an empty string to clear it.")
    if (
        not create
        and not complete
        and not own(params, "headline")
        and not own(params, "description")
    ):
        raise ValueError("update_task requires headline or description.")

    values: dict[str, Any] = {"projectId": as_id(params["projectId"])}
    if not create:
        values["id"] = as_id(params["id"])
    if complete:
        values["status"] = DONE_STATUS
    else:
        for key in ("headline", "description"):
            if own(params, key):
                values[key] = params[key]
    return {"values": values}


build_leantime_rpc = validate_request
