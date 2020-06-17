import logging
from yaml import YAMLError

from checkov.cloudformation.parser import cfn_yaml
from checkov.cloudformation.context_parser import ContextParser

logger = logging.getLogger(__name__)


def parse(filename):
    template = None
    template_lines = None
    try:
        (template, template_lines) = cfn_yaml.load(filename)
        if not template or not is_checked_sls_template(template):
            return
    except IOError as e:
        if e.errno == 2:
            logger.error('Template file not found: %s', filename)
            return
        elif e.errno == 21:
            logger.error('Template references a directory, not a file: %s',
                         filename)
            return
        elif e.errno == 13:
            logger.error('Permission denied when accessing template file: %s',
                         filename)
            return
    except UnicodeDecodeError as err:
        logger.error('Cannot read file contents: %s', filename)
        return
    except YAMLError as err:
        return

    return template, template_lines


def is_checked_sls_template(template):
    if template.__contains__('provider'):
        # support AWS provider serverless templates
        if template['provider'].get('name').lower() == 'aws':
            if template_contains_cf_resources(template) or template_contains_iam_policies(template):
                return True
    return False


def template_contains_cf_resources(template):
    if template.__contains__('resources'):
        if template['resources'].get('Resources'):
            return True
    return False


def template_contains_iam_policies(template):
    if ContextParser.search_deep_keys('iamRoleStatements', template, []):
        return True
    return False
