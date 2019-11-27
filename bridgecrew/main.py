import logging

# set up logging to file - see previous section for more details
from bridgecrew.terraformscanner.parser import Parser
from bridgecrew.terraformscanner.scanner_registry import ScannerRegistry
from bridgecrew.terraformscanner.scanners.S3AccessLogs import S3AccessLogsScanner

logging.basicConfig(level=logging.INFO)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# tell the handler to use this format
console.setFormatter(formatter)

scanner_registry = ScannerRegistry()

s3 = S3AccessLogsScanner()



tf_defenitions = {}
param = "/Users/barak/Documents/dev/platform2/src/stacks/baseStack"
Parser().hcl2(directory=param, tf_defenitions=tf_defenitions)
for definition in tf_defenitions.items():
    scanned_file = definition[0].split(param)[1]
    logging.info("Scanning file: %s", scanned_file)
    if 'resource' in definition[1]:
        for resource in definition[1]['resource']:
            scanner_registry.scan(resource, scanned_file)
