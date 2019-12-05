import unittest

from checkov.terraform.models.enums import ScanResult
from checkov.terraform.checks.resource.aws.PasswordPolicyReuse import scanner


class TestPasswordPolicyReuse(unittest.TestCase):

    def test_success(self):
        resource_conf = {
            "minimum_password_length": 14,
            "require_lowercase_characters": True,
            "require_numbers": True,
            "require_uppercase_characters": True,
            "require_symbols": True,
            "allow_users_to_change_password": True,
            "password_reuse_prevention" : 24
        }
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.SUCCESS, scan_result)

    def test_failure(self):
        resource_conf = {
            "minimum_password_length": 8,
            "require_lowercase_characters": False,
            "require_numbers": True,
            "require_uppercase_characters": True,
            "require_symbols": True,
            "allow_users_to_change_password": True,
            "password_reuse_prevention": 4
        }
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.FAILURE, scan_result)

    def test_failure_on_missing_property(self):
        resource_conf = {
            "require_numbers": True,
            "require_symbols": True,
            "allow_users_to_change_password": True,
        }
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.FAILURE, scan_result)


if __name__ == '__main__':
    unittest.main()
