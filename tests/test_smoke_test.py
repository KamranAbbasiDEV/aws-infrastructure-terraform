import importlib.util
from pathlib import Path
from unittest.mock import patch
import io
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("smoke_test", ROOT / "scripts" / "smoke_test.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return None

    def read(self, _):
        return b"<h1>CloudOps Infrastructure Lab</h1>"


class SmokeTestTests(unittest.TestCase):
    def test_valid_mocked_http(self):
        with patch.object(module.urllib.request, "urlopen", return_value=FakeResponse()):
            result = module.smoke_test("http://example.com/demo?token=hidden")
        self.assertEqual(result["status"], "passed")
        self.assertTrue(result["contains_lab_marker"])
        self.assertNotIn("hidden", result["url"])

    def test_invalid_url_rejected(self):
        with self.assertRaises(ValueError):
            module.smoke_test("file:///etc/passwd")

    def test_embedded_credentials_rejected(self):
        with self.assertRaises(ValueError):
            module.smoke_test("https://user:password@example.com/")

    def test_timeout_rejected(self):
        with self.assertRaises(ValueError):
            module.smoke_test("https://example.com/", timeout=-2)


if __name__ == "__main__":
    unittest.main()
