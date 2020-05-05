from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class S3PublicACLWrite(BaseResourceCheck):
    def __init__(self):
        name = "S3 Bucket has an ACL defined which allows public WRITE access."
        id = "CKV_AWS_57"
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
            if acl_block[0] == "public-read-write":
                return CheckResult.FAILED
        return CheckResult.PASSED


check = S3PublicACLWrite()
