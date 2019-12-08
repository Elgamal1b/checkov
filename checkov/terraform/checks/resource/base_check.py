import logging
from abc import ABC, abstractmethod

from checkov.terraform.models.enums import CheckResult
from checkov.terraform.checks.resource.registry import resource_registry
from colorama import init
from termcolor import colored

init(autoreset=True)


class BaseResourceCheck(ABC):
    id = ""
    name = ""
    categories = []

    def __init__(self, name, id, categories, supported_resources):
        self.name = name
        self.id = id
        self.categories = categories
        self.supported_resources = supported_resources
        self.logger = logging.getLogger("{}".format(self.__module__))
        resource_registry.register(self)

    def run(self, scanned_file, resource_configuration, resource_name, resource_type):
        result = self.scan_resource_conf(resource_configuration)
        message = "File {}, Resource \"{}.{}\" Scan \"{}\" Result: {} ".format(scanned_file, resource_type,
                                                                               resource_name,
                                                                               self.name,
                                                                               result)
        if result == CheckResult.FAILURE:
            print(colored(message,'red'))
            self.logger.warning(message)
        else:
            print(colored(message,'green'))
            self.logger.info(message)
        return result

    @abstractmethod
    def scan_resource_conf(self, conf):
        raise NotImplementedError()
