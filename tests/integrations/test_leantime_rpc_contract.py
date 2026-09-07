import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_YAML = ROOT / "config" / "integrations" / "leantime.yaml"
MODULE_PATH = ROOT / "integrations" / "n8n" / "leantime_rpc.py"


def load_contract():
    spec = importlib.util.spec_from_file_location("leantime_rpc", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


rpc = load_contract()


def error_message(result):
    return result["response"]["error"]["message"]


def error_code(result):
    return result["response"]["error"]["code"]


class LeantimeRpcContractTests(unittest.TestCase):
    def test_unsupported_operation_rejected(self):
        result = rpc.validate_request(
            {"operation": "delete_project", "params": {}}
        )
        self.assertFalse(result["ok"])
        self.assertEqual(error_code(result), "VALIDATION_ERROR")
        self.assertEqual(error_message(result), "Unsupported operation.")

    def test_missing_operation_rejected(self):
        for body in (None, {}, {"params": {}}, {"operation": "", "params": {}}):
            with self.subTest(body=body):
                result = rpc.validate_request(body)
                self.assertFalse(result["ok"])
                self.assertEqual(error_code(result), "VALIDATION_ERROR")

    def test_invalid_ids_rejected(self):
        invalid_ids = [None, "", "abc", "12", 0, -1, 1.5, True, False]
        for value in invalid_ids:
            with self.subTest(value=value):
                result = rpc.validate_request(
                    {"operation": "get_task", "params": {"id": value}}
                )
                self.assertFalse(result["ok"])
                self.assertEqual(error_code(result), "VALIDATION_ERROR")
                self.assertIn("positive integer", error_message(result))

        result = rpc.validate_request(
            {"operation": "get_project", "params": {"id": 0}}
        )
        self.assertFalse(result["ok"])

    def test_complete_task_forces_done_status(self):
        result = rpc.validate_request(
            {
                "operation": "complete_task",
                "params": {"id": 42, "projectId": 7},
                "requestId": "complete-42",
            }
        )
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["credential"], "write")
        self.assertEqual(
            result["rpc_method"], "leantime.rpc.Tickets.Tickets.updateTicket"
        )
        values = result["rpc"]["params"]["values"]
        self.assertEqual(values["id"], 42)
        self.assertEqual(values["projectId"], 7)
        self.assertEqual(values["status"], rpc.DONE_STATUS)
        self.assertEqual(values["status"], 0)
        self.assertTrue(rpc.needs_description_read(result))

    def test_no_arbitrary_userid_status_rpc_method_passthrough(self):
        attacks = [
            {
                "operation": "list_projects",
                "params": {},
                "rpc_method": "leantime.rpc.users.getAll",
            },
            {
                "operation": "complete_task",
                "params": {"id": 9, "projectId": 1, "status": 3},
            },
            {
                "operation": "update_task",
                "params": {
                    "id": 9,
                    "projectId": 1,
                    "headline": "ok",
                    "userId": 1,
                },
            },
            {
                "operation": "create_task",
                "params": {
                    "projectId": 1,
                    "headline": "ok",
                    "method": "leantime.rpc.Tickets.Tickets.addTicket",
                },
            },
        ]
        for payload in attacks:
            with self.subTest(payload=payload):
                result = rpc.validate_request(payload)
                self.assertFalse(result["ok"])
                self.assertEqual(error_code(result), "VALIDATION_ERROR")
                self.assertNotIn("rpc", result)

        allowed = rpc.validate_request(
            {
                "operation": "update_task",
                "params": {"id": 9, "projectId": 1, "headline": "rename"},
            }
        )
        self.assertTrue(allowed["ok"], allowed)
        self.assertNotIn("status", allowed["rpc"]["params"]["values"])
        self.assertNotIn("userId", allowed["rpc"]["params"]["values"])

    def test_allowlisted_operations_build(self):
        payloads = {
            "list_projects": {"operation": "list_projects", "params": {}},
            "get_project": {
                "operation": "get_project",
                "params": {"id": 1},
            },
            "list_tasks": {
                "operation": "list_tasks",
                "params": {"searchCriteria": {"projectId": 1}},
            },
            "get_task": {"operation": "get_task", "params": {"id": 9}},
            "create_task": {
                "operation": "create_task",
                "params": {"projectId": 1, "headline": "Draft"},
            },
            "update_task": {
                "operation": "update_task",
                "params": {"id": 9, "projectId": 1, "headline": "Rename"},
            },
            "complete_task": {
                "operation": "complete_task",
                "params": {"id": 9, "projectId": 1},
            },
        }
        self.assertEqual(set(payloads), rpc.ALLOWED_OPERATIONS)
        for operation, payload in payloads.items():
            with self.subTest(operation=operation):
                result = rpc.validate_request(payload)
                self.assertTrue(result["ok"], result)
                self.assertEqual(
                    result["rpc"]["method"], rpc.OPERATIONS[operation]["rpc_method"]
                )
                serialized = str(result["rpc"]["params"])
                self.assertNotIn("userId", serialized)
                if operation != "complete_task":
                    self.assertNotIn("status", serialized)

    def test_update_task_requires_a_field(self):
        result = rpc.validate_request(
            {"operation": "update_task", "params": {"id": 9, "projectId": 1}}
        )
        self.assertFalse(result["ok"])
        self.assertEqual(
            error_message(result), "update_task requires headline or description."
        )

    def test_yaml_contract_matches_allowlist(self):
        self.assertTrue(CONTRACT_YAML.is_file(), CONTRACT_YAML)
        yaml_text = CONTRACT_YAML.read_text(encoding="utf-8")
        self.assertIn("done_status: 0", yaml_text)
        self.assertIn("reject_arbitrary_rpc: true", yaml_text)
        self.assertIn("/webhook/root/leantime/rpc", yaml_text)
        self.assertIn("x-root-api-key", yaml_text)
        for operation in rpc.ALLOWED_OPERATIONS:
            self.assertIn(f"{operation}:", yaml_text)
        self.assertIn("leantime.rpc.Tickets.Tickets.getTicket", yaml_text)

    def test_read_write_credential_split(self):
        reads = ["list_projects", "get_project", "list_tasks", "get_task"]
        writes = ["create_task", "update_task", "complete_task"]
        for operation in reads:
            self.assertEqual(rpc.OPERATIONS[operation]["credential"], "read")
        for operation in writes:
            self.assertEqual(rpc.OPERATIONS[operation]["credential"], "write")


if __name__ == "__main__":
    unittest.main()
