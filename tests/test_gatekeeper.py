import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from gatekeeper import REQUIRED_JOBS, failures


class GatekeeperTests(unittest.TestCase):
    def success(self):
        return {name: {"result": "success"} for name in REQUIRED_JOBS}

    def test_all_success(self):
        self.assertEqual(failures(self.success()), [])

    def test_rejects_failure_skip_cancel_and_missing_status(self):
        for name in REQUIRED_JOBS:
            for result in ("failure", "skipped", "cancelled", "pending", None):
                with self.subTest(name=name, result=result):
                    needs = self.success()
                    needs[name] = {"result": result}
                    self.assertTrue(failures(needs))

    def test_rejects_missing_or_unexpected_job(self):
        self.assertTrue(failures({}))
        needs = self.success()
        needs["unreviewed-job"] = {"result": "success"}
        self.assertTrue(failures(needs))

    def test_rejects_invalid_input(self):
        for value in (None, [], "success"):
            self.assertTrue(failures(value))
