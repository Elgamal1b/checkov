import unittest

from checkov.terraformscanner.models.enums import ScanResult
from checkov.terraformscanner.resource_scanners.aws.SQSQueueEncryption import scanner


class TestS3Encryption(unittest.TestCase):

    def test_failure(self):
        resource_conf = {'name': ['terraform-example-queue']}
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.FAILURE, scan_result)

    def test_success(self):
        resource_conf = {'name': ['terraform-example-queue'], 'kms_master_key_id': ['alias/aws/sqs'],
                         'kms_data_key_reuse_period_seconds': [300]}
        scan_result = scanner.scan_resource_conf(conf=resource_conf)
        self.assertEqual(ScanResult.SUCCESS, scan_result)


if __name__ == '__main__':
    unittest.main()
