from bridgecrew.terraformscanner.models.enums import ScanResult, ScanCategories
from bridgecrew.terraformscanner.resource_scanner import ResourceScanner


class AzureInstancePassword(ResourceScanner):
    def __init__(self):
        name = "Ensure Azure Instance does not use basic authentication(Use SSH Key Instead)"
        scan_id = "BC_AZURE_INSTANCE_1"
        supported_resource = 'azurerm_virtual_machine'
        categories = [ScanCategories.GENERAL_SECURITY]
        super().__init__(name=name, scan_id=scan_id, categories=categories, supported_resource=supported_resource)

    def scan_resource_conf(self, conf):
        """
            Looks for password configuration at azure_instance:
            https://www.terraform.io/docs/providers/azure/r/instance.html
        :param conf: azure_instance configuration
        :return: <ScanResult>
        """
        if 'os_profile_linux_config' in conf.keys():
            linux_config = conf['os_profile_linux_config'][0]
            if 'disable_password_authentication' in linux_config.keys():
                disable_password_authentication = linux_config['disable_password_authentication']
                if disable_password_authentication == [False]:
                    return ScanResult.FAILURE
        return ScanResult.SUCCESS


scanner = AzureInstancePassword()
