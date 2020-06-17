from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_negative_value_check import BaseResourceNegativeValueCheck


class S3PublicACLRead(BaseResourceNegativeValueCheck):
    def __init__(self):
        name = "S3 Bucket has an ACL defined which allows public READ access."
        id = "CKV_AWS_20"
        supported_resources = ['aws_s3_bucket']
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        """
            Looks for ACL configuration at aws_s3_bucket:
            https://www.terraform.io/docs/providers/aws/r/s3_bucket.html
        :param conf: aws_s3_bucket configuration
        :return: <CheckResult>
        """
        if 'acl' in conf.keys():
            acl_block = conf['acl']
            if acl_block in [["public-read"], ["public-read-write"], ["website"]]:
                return CheckResult.FAILED
        return CheckResult.PASSED

    def get_inspected_key(self):
        return 'acl'

    def get_vulnerable_values(self):
        return ["public-read", "public-read-write", "website"]


check = S3PublicACLRead()
