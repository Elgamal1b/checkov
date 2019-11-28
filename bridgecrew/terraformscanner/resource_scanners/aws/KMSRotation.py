from bridgecrew.terraformscanner.models.enums import ScanResult, ScanCategories
from bridgecrew.terraformscanner.resource_scanner import ResourceScanner


class KMSRotation(ResourceScanner):
    def __init__(self):
        name = "Ensure rotation for customer created CMKs is enabled"
        scan_id = "BC_AWS_LOGGING_8"
        supported_resources = ['aws_kms_key']
        categories = [ScanCategories.ENCRYPTION]
        super().__init__(name=name, scan_id=scan_id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        """
            validates kms rotation
            https://www.terraform.io/docs/providers/aws/r/kms_key.html
        :param conf: aws_kms_key configuration
        :return: <ScanResult>
        """
        key = 'enable_key_rotation'
        if key in conf.keys():
            if conf[key]:
                return ScanResult.SUCCESS
        return ScanResult.FAILURE


scanner = KMSRotation()
