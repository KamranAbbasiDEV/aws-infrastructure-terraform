import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_source", ROOT / "scripts" / "validate_source.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class TerraformSourceTests(unittest.TestCase):
    def test_dedicated_vpc(self):
        self.assertTrue(module.inspect_source()["dedicated_vpc"])

    def test_gateway(self):
        self.assertTrue(module.inspect_source()["internet_gateway"])

    def test_ssm_role(self):
        self.assertTrue(module.inspect_source()["ssm_managed_instance"])

    def test_encrypted_ebs(self):
        self.assertTrue(module.inspect_source()["encrypted_ebs"])

    def test_imdsv2(self):
        self.assertTrue(module.inspect_source()["imdsv2_required"])

    def test_no_ssh_ingress(self):
        self.assertTrue(module.inspect_source()["no_ssh_ingress"])

    def test_cloudwatch_alarms(self):
        self.assertTrue(module.inspect_source()["cloudwatch_alarms"])

    def test_no_alarm_notifications(self):
        self.assertTrue(module.inspect_source()["no_automated_alarm_actions"])

    def test_nginx_bootstrap(self):
        self.assertTrue(module.inspect_source()["nginx_bootstrap"])

    def test_provider(self):
        self.assertTrue(module.inspect_source()["terraform_provider"])


if __name__ == "__main__":
    unittest.main()
