import unittest

from bridgecrew.terraformscanner.models.enums import ScanResult
from bridgecrew.terraformscanner.resource_scanners.S3PublicACL import scanner


class TestS3PublicACL(unittest.TestCase):

    def test_failure(self):
        resource_conf = {"region": ["us-west-2"],
                         "bucket": ["my_bucket"],
                         "acl": ["public-read"],
                         "force_destroy": [True],
                         "tags": [{"Name": "my-bucket"}],
                         }
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.FAILURE, scan_result)

    def test_success(self):
        resource_conf = {"region": ["us-west-2"],
                         "bucket": ["my_bucket"],
                         "force_destroy": [True],
                         "tags": [{"Name": "my-bucket"}]
                         }
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.SUCCESS, scan_result)


if __name__ == '__main__':
    unittest.main()
