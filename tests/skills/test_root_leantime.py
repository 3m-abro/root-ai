import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = (
    ROOT / "skills" / "productivity" / "leantime" / "scripts" / "root_leantime.py"
)
CONTRACT_PATH = ROOT / "integrations" / "n8n" / "leantime_rpc.py"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


rpc = load_module(CONTRACT_PATH, "leantime_rpc")


def skill_mod():
    return load_module(SKILL_PATH, "root_leantime")


class RootLeantimeSkillTests(unittest.TestCase):
    def setUp(self):
        self.skill = skill_mod()

    def params(self, argv):
        args = self.skill.build_parser().parse_args(argv)
        return args.operation, self.skill.params_for(args)

    def assert_contract_ok(self, operation, params):
        result = rpc.validate_request({"operation": operation, "params": params})
        self.assertTrue(result["ok"], result)
        return result

    def test_read_operations_match_contract(self):
        cases = [
            (["list_projects"], {}),
            (["get_project", "--id", "3"], {"id": 3}),
            (
                ["list_tasks", "--project-id", "3"],
                {"searchCriteria": {"projectId": 3}},
            ),
            (["get_task", "--id", "20"], {"id": 20}),
        ]
        for argv, expected in cases:
            with self.subTest(argv=argv):
                operation, params = self.params(argv)
                self.assertEqual(params, expected)
                self.assert_contract_ok(operation, params)

    def test_create_and_complete_match_contract(self):
        operation, params = self.params(
            [
                "create_task",
                "--project-id",
                "3",
                "--headline",
                "Task title",
                "--description",
                "Optional description",
                "--priority",
                "2",
                "--tags",
                "root",
                "--date-to-finish",
                "2026-09-21",
            ]
        )
        self.assertEqual(
            params,
            {
                "projectId": 3,
                "headline": "Task title",
                "description": "Optional description",
                "priority": 2,
                "tags": "root",
                "dateToFinish": "2026-09-21",
            },
        )
        self.assert_contract_ok(operation, params)

        operation, params = self.params(
            ["complete_task", "--id", "21", "--project-id", "3"]
        )
        self.assertEqual(params, {"id": 21, "projectId": 3})
        result = self.assert_contract_ok(operation, params)
        self.assertEqual(result["rpc"]["params"]["values"]["status"], 0)

    def test_update_task_optional_fields_match_contract(self):
        operation, params = self.params(
            [
                "update_task",
                "--id",
                "21",
                "--project-id",
                "3",
                "--priority",
                "1",
                "--tags",
                "clearstack",
                "--date-to-finish",
                "2026-10-01",
            ]
        )
        self.assertEqual(
            params,
            {
                "id": 21,
                "projectId": 3,
                "priority": 1,
                "tags": "clearstack",
                "dateToFinish": "2026-10-01",
            },
        )
        self.assert_contract_ok(operation, params)

    def test_update_task_without_fields_fails_locally(self):
        with mock.patch("sys.stdout", new_callable=io.StringIO):
            with self.assertRaises(SystemExit):
                self.params(["update_task", "--id", "21", "--project-id", "3"])

    def test_cli_rejects_invalid_due_date(self):
        parser = self.skill.build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(
                [
                    "update_task",
                    "--id",
                    "21",
                    "--project-id",
                    "3",
                    "--date-to-finish",
                    "2026-13-01",
                ]
            )

    def test_http_url_is_rejected(self):
        with mock.patch.object(self.skill, "API_KEY", "test-key"):
            with mock.patch.object(self.skill, "N8N_URL", "http://n8n.example/webhook"):
                with mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
                    with self.assertRaises(SystemExit) as raised:
                        self.skill.call_api("list_projects", {})
        self.assertEqual(raised.exception.code, 1)
        self.assertIn("https URL", stdout.getvalue())
        self.assertNotIn("test-key", stdout.getvalue())

    def test_http_error_body_is_printed(self):
        payload = {
            "ok": False,
            "operation": "update_task",
            "requestId": "root-1",
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Unsupported operation.",
            },
        }
        error = HTTPError(
            "https://n8n.example/webhook/root/leantime/rpc",
            400,
            "Bad Request",
            hdrs=None,
            fp=io.BytesIO(json.dumps(payload).encode("utf-8")),
        )
        with mock.patch.object(self.skill, "API_KEY", "test-key"):
            with mock.patch("urllib.request.urlopen", side_effect=error):
                with mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
                    with self.assertRaises(SystemExit) as raised:
                        self.skill.call_api("list_projects", {})
        self.assertEqual(raised.exception.code, 2)
        printed = json.loads(stdout.getvalue())
        self.assertEqual(printed["error"]["code"], "VALIDATION_ERROR")
        self.assertNotIn("test-key", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
