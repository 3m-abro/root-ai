#!/usr/bin/env python3

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date


N8N_URL = os.getenv(
    "ROOT_N8N_LEANTIME_URL",
    "https://n8n.maqsoodabro.com/webhook/root/leantime/rpc",
)

API_KEY = os.getenv("ROOT_N8N_API_KEY")


def fail(message, code=1):
    print(
        json.dumps(
            {
                "ok": False,
                "error": message,
            }
        )
    )
    sys.exit(code)


def positive_int(value):
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return value


def priority_int(value):
    value = int(value)
    if value < 1 or value > 5:
        raise argparse.ArgumentTypeError("must be an integer from 1 to 5")
    return value


def date_to_finish(value):
    if value == "":
        return value
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "must be YYYY-MM-DD or empty to clear"
        ) from exc
    if parsed.isoformat() != value:
        raise argparse.ArgumentTypeError("must be YYYY-MM-DD or empty to clear")
    return value


def call_api(operation, params):
    if not API_KEY:
        fail("ROOT_N8N_API_KEY is not configured.")

    parsed_url = urllib.parse.urlparse(N8N_URL)
    if parsed_url.scheme != "https" or not parsed_url.netloc:
        fail("ROOT_N8N_LEANTIME_URL must be an https URL.")

    payload = json.dumps(
        {
            "operation": operation,
            "params": params,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        N8N_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-root-api-key": API_KEY,
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            result = json.loads(body)
        except json.JSONDecodeError:
            fail(f"n8n returned HTTP {exc.code}")
        print(json.dumps(result, indent=2))
        sys.exit(2)
    except urllib.error.URLError as exc:
        fail(f"Unable to reach ROOT n8n integration: {exc.reason}")
    except TimeoutError:
        fail("ROOT n8n integration timed out.")

    try:
        result = json.loads(body)
    except json.JSONDecodeError:
        fail("ROOT n8n integration returned invalid JSON.")

    print(json.dumps(result, indent=2))

    if not result.get("ok", False):
        sys.exit(2)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Controlled ROOT → n8n → Leantime interface"
    )
    subparsers = parser.add_subparsers(dest="operation", required=True)

    subparsers.add_parser("list_projects")

    get_project = subparsers.add_parser("get_project")
    get_project.add_argument("--id", type=positive_int, required=True)

    list_tasks = subparsers.add_parser("list_tasks")
    list_tasks.add_argument("--project-id", type=positive_int, required=True)

    get_task = subparsers.add_parser("get_task")
    get_task.add_argument("--id", type=positive_int, required=True)

    create_task = subparsers.add_parser("create_task")
    create_task.add_argument("--project-id", type=positive_int, required=True)
    create_task.add_argument("--headline", required=True)
    create_task.add_argument("--description")
    create_task.add_argument("--priority", type=priority_int)
    create_task.add_argument("--tags")
    create_task.add_argument("--date-to-finish", type=date_to_finish)

    update_task = subparsers.add_parser("update_task")
    update_task.add_argument("--id", type=positive_int, required=True)
    update_task.add_argument("--project-id", type=positive_int, required=True)
    update_task.add_argument("--headline")
    update_task.add_argument("--description")
    update_task.add_argument("--priority", type=priority_int)
    update_task.add_argument("--tags")
    update_task.add_argument("--date-to-finish", type=date_to_finish)

    complete_task = subparsers.add_parser("complete_task")
    complete_task.add_argument("--id", type=positive_int, required=True)
    complete_task.add_argument("--project-id", type=positive_int, required=True)

    return parser


def params_for(args):
    if args.operation == "list_projects":
        return {}

    if args.operation == "get_project":
        return {"id": args.id}

    if args.operation == "list_tasks":
        return {"searchCriteria": {"projectId": args.project_id}}

    if args.operation == "get_task":
        return {"id": args.id}

    if args.operation == "create_task":
        if not args.headline.strip():
            fail("headline must not be empty.")
        params = {
            "projectId": args.project_id,
            "headline": args.headline,
        }
        if args.description is not None:
            params["description"] = args.description
        if args.priority is not None:
            params["priority"] = args.priority
        if args.tags is not None:
            params["tags"] = args.tags
        if args.date_to_finish is not None:
            params["dateToFinish"] = args.date_to_finish
        return params

    if args.operation == "update_task":
        params = {
            "id": args.id,
            "projectId": args.project_id,
        }
        optional = {
            "headline": args.headline,
            "description": args.description,
            "priority": args.priority,
            "tags": args.tags,
            "dateToFinish": args.date_to_finish,
        }
        changes = {
            key: value for key, value in optional.items() if value is not None
        }
        if not changes:
            fail(
                "update_task requires at least one of headline, description, priority, tags, dateToFinish."
            )
        params.update(changes)
        return params

    if args.operation == "complete_task":
        return {
            "id": args.id,
            "projectId": args.project_id,
        }

    fail("Unsupported operation.")


def main(argv=None):
    args = build_parser().parse_args(argv)
    call_api(args.operation, params_for(args))


if __name__ == "__main__":
    main()
