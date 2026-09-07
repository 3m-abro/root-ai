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


class LeantimeRpcContractTests(unittest.TestCase):
    def test_unsupported_operation_rejected(self):
        result = rpc.build_leantime_rpc({"operation": "delete_project"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "unsupported_operation")

    def test_missing_operation_rejected(self):
        self.assertEqual(rpc.build_leantime_rpc({}).get("error"), "missing_operation")
        self.assertEqual(rpc.build_leantime_rpc(None).get("error"), "missing_operation")
        self.assertEqual(
            rpc.build_leantime_rpc({"operation": ""}).get("error"),
            "missing_operation",
        )

    def test_invalid_ids_rejected(self):
        invalid_ids = [None, "", "abc", 0, -1, 1.5, True, False]
        for value in invalid_ids:
            with self.subTest(value=value):
                result = rpc.build_leantime_rpc(
                    {"operation": "get_task", "task_id": value}
                )
                self.assertFalse(result["ok"])
                self.assertEqual(result["error"], "invalid_id")

        result = rpc.build_leantime_rpc({"operation": "get_project", "project_id": 0})
        self.assertEqual(result["error"], "invalid_id")

    def test_complete_task_forces_done_status(self):
        result = rpc.build_leantime_rpc({"operation": "complete_task", "task_id": 42})
        self.assertTrue(result["ok"])
        self.assertEqual(result["credential"], "write")
        self.assertEqual(result["rpc_method"], "leantime.rpc.tickets.updateTicket")
        self.assertEqual(result["params"]["values"]["id"], 42)
        self.assertEqual(result["params"]["values"]["status"], rpc.DONE_STATUS)
        self.assertEqual(result["params"]["values"]["status"], 0)

    def test_no_arbitrary_userid_status_rpc_method_passthrough(self):
        attacks = [
            {
                "operation": "list_projects",
                "rpc_method": "leantime.rpc.users.getAll",
            },
            {
                "operation": "complete_task",
                "task_id": 9,
                "status": 3,
            },
            {
                "operation": "update_task",
                "task_id": 9,
                "title": "ok",
                "userId": 1,
            },
            {
                "operation": "create_task",
                "project_id": 1,
                "title": "ok",
                "method": "leantime.rpc.tickets.addTicket",
            },
        ]
        for payload in attacks:
            with self.subTest(payload=payload):
                result = rpc.build_leantime_rpc(payload)
                self.assertFalse(result["ok"])
                self.assertEqual(result["error"], "forbidden_passthrough")
                self.assertNotIn("rpc_method", result.get("params", {}))

        allowed = rpc.build_leantime_rpc(
            {"operation": "update_task", "task_id": 9, "title": "rename"}
        )
        self.assertTrue(allowed["ok"])
        self.assertNotIn("status", allowed["params"]["values"])
        self.assertNotIn("userId", allowed["params"]["values"])

    def test_allowlisted_operations_build(self):
        payloads = {
            "list_projects": {"operation": "list_projects"},
            "get_project": {"operation": "get_project", "project_id": 1},
            "list_tasks": {"operation": "list_tasks", "project_id": 1},
            "get_task": {"operation": "get_task", "task_id": 9},
            "create_task": {
                "operation": "create_task",
                "project_id": 1,
                "title": "Draft",
            },
            "update_task": {
                "operation": "update_task",
                "task_id": 9,
                "title": "Rename",
            },
            "complete_task": {"operation": "complete_task", "task_id": 9},
        }
        self.assertEqual(set(payloads), rpc.ALLOWED_OPERATIONS)
        for operation, payload in payloads.items():
            with self.subTest(operation=operation):
                result = rpc.build_leantime_rpc(payload)
                self.assertTrue(result["ok"], result)
                self.assertEqual(
                    result["rpc_method"], rpc.OPERATIONS[operation]["rpc_method"]
                )
                serialized = str(result["params"])
                self.assertNotIn("userId", serialized)
                if operation != "complete_task":
                    self.assertNotIn("status", serialized)

    def test_update_task_requires_a_field(self):
        result = rpc.build_leantime_rpc({"operation": "update_task", "task_id": 9})
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "missing_update_fields")

    def test_yaml_contract_matches_allowlist(self):
        self.assertTrue(CONTRACT_YAML.is_file(), CONTRACT_YAML)
        yaml_text = CONTRACT_YAML.read_text(encoding="utf-8")
        self.assertIn("done_status: 0", yaml_text)
        self.assertIn("reject_arbitrary_rpc: true", yaml_text)
        for operation in rpc.ALLOWED_OPERATIONS:
            self.assertIn(f"{operation}:", yaml_text)

    def test_read_write_credential_split(self):
        reads = ["list_projects", "get_project", "list_tasks", "get_task"]
        writes = ["create_task", "update_task", "complete_task"]
        for operation in reads:
            self.assertEqual(rpc.OPERATIONS[operation]["credential"], "read")
        for operation in writes:
            self.assertEqual(rpc.OPERATIONS[operation]["credential"], "write")


if __name__ == "__main__":
    unittest.main()
