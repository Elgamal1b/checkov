import unittest

from bridgecrew.terraformscanner.models.enums import ScanResult
from bridgecrew.terraformscanner.scanners.KMSRotation import KMSRotation


class TestKMSRotation(unittest.TestCase):

    def test_success(self):
        scanner = KMSRotation()
        resource_conf = {
            "description": "KMS key 1",
            "deletion_window_in_days": 10,
            "enable_key_rotation": True
        }
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.SUCCESS, scan_result)

    def test_failure(self):
        scanner = KMSRotation()
        resource_conf = {
            "description": "KMS key 1",
            "deletion_window_in_days": 10,
            "enable_key_rotation": False
        }
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.FAILURE, scan_result)

    def test_failure_on_missing_property(self):
        scanner = KMSRotation()
        resource_conf = {
            "description": "KMS key 1",
            "deletion_window_in_days": 10,
        }
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.FAILURE, scan_result)


if __name__ == '__main__':
    unittest.main()
