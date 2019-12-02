from checkov.terraformscanner.models.enums import ScanResult, ScanCategories
from checkov.terraformscanner.resource_scanner import ResourceScanner


class RDSPubliclyAccessible(ResourceScanner):
    def __init__(self):
        name = "Ensure all data stored in the RDS bucket is not public accessible"
        scan_id = "BC_AWS_RDS_2"
        supported_resources = ['aws_db_instance','aws_rds_cluster_instance']
        categories = [ScanCategories.NETWORKING]
        super().__init__(name=name, scan_id=scan_id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        """
            Looks for publicly_accessible configuration at aws_db_instance:
            https://www.terraform.io/docs/providers/aws/d/db_instance.html
        :param conf: publicly_accessible configuration
        :return: <ScanResult>
        """
        if 'publicly_accessible' in conf.keys():
            key = conf['publicly_accessible'][0]
            if key:
                return ScanResult.FAILURE
        return ScanResult.SUCCESS


scanner = RDSPubliclyAccessible()
