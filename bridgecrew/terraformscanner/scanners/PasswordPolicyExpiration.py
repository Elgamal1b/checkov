from bridgecrew.terraformscanner.models.enums import ScanResult, ScanCategories
from bridgecrew.terraformscanner.scanner import Scanner


class PasswordPolicyExpiration(Scanner):
    def __init__(self):
        name = "Ensure IAM password policy expires passwords within 90 days or less"
        scan_id = "BC_AWS_IAM_11"
        supported_resource = 'aws_iam_account_password_policy'
        categories = [ScanCategories.IAM]
        super().__init__(name=name, scan_id=scan_id, categories=categories, supported_resource=supported_resource)

    def scan_resource_conf(self, conf):
        """
            validates iam password policy
            https://www.terraform.io/docs/providers/aws/r/iam_account_password_policy.html
        :param conf: aws_iam_account_password_policy configuration
        :return: <ScanResult>
        """
        key = 'max_password_age'
        if key in conf.keys():
            if conf[key] >= 90:
                return ScanResult.SUCCESS
        return ScanResult.FAILURE
