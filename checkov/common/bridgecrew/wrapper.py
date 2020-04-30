import logging
import os
import json
import itertools
import dpath.util
from checkov.common.models.consts import SUPPORTED_FILE_EXTENSIONS

logging.basicConfig(level=logging.INFO)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# tell the handler to use this format
console.setFormatter(formatter)

checkov_results_prefix = 'checkov_results'
check_reduced_keys = (
    'check_id', 'check_result', 'resource', 'file_path',
    'file_line_range')
check_metadata_keys = ('evaluations', 'code_block')


def _is_scanned_file(file):
    file_ending = os.path.splitext(file)[1]
    return file_ending in SUPPORTED_FILE_EXTENSIONS


def _put_json_object(s3_client, json_obj, bucket, object_path):
    try:
        s3_client.put_object(Bucket=bucket, Key=object_path, Body=json.dumps(json_obj))
    except Exception as e:
        logging.error(f"failed to persist object {json_obj} into S3 bucket {bucket}\n{e}")
        raise e


def _extract_checks_metadata(report, full_repo_object_key):
    return {check.check_id: dict({k: getattr(check, k) for k in check_metadata_keys},
                                 **{'file_object_path': full_repo_object_key + check.file_path}) for check in
            list(itertools.chain(report.passed_checks, report.failed_checks, report.skipped_checks))}


def reduce_scan_reports(scan_reports):
    """
    Transform checkov reports objects into compact dictionaries
    :param scan_reports: List of checkov output reports
    :return: dictionary of
    """
    reduced_scan_reports = {}
    for report in scan_reports:
        reduced_scan_reports[report.check_type] = \
            {
                "checks": {
                    "passed_checks": [
                        {k: getattr(check, k) for k in check_reduced_keys}
                        for check in report.passed_checks],
                    "failed_checks": [
                        {k: getattr(check, k) for k in check_reduced_keys}
                        for check in report.failed_checks],
                    "skipped_checks": [
                        {k: getattr(check, k) for k in check_reduced_keys}
                        for check in report.skipped_checks]}}
    return reduced_scan_reports


def persist_checks_results(reduced_scan_reports, s3_client, bucket, full_repo_object_key):
    """
    Save reduced scan reports into bridgecrew's platform
    :return: List of checks results path of all runners
    """
    checks_results_paths = {}
    for check_type, reduced_report in reduced_scan_reports.items():
        check_result_object_path = f'{full_repo_object_key}/{checkov_results_prefix}/{check_type}/checks_results.json'
        checks_results_paths[check_type] = check_result_object_path
        _put_json_object(s3_client, reduced_report, bucket, check_result_object_path)
    return checks_results_paths


def enrich_and_persist_checks_metadata(scan_reports, s3_client, bucket, full_repo_object_key):
    """
    Save checks metadata into bridgecrew's platform
    :return:
    """
    checks_metadata_paths = {}
    for scan_report in scan_reports:
        check_type = scan_report.check_type
        checks_metadata_object = _extract_checks_metadata(scan_report, full_repo_object_key)
        checks_metadata_object_path = f'{full_repo_object_key}/{checkov_results_prefix}/{check_type}/checks_metadata.json'
        dpath.new(checks_metadata_paths, f"{check_type}/checks_metadata_path", checks_metadata_object_path)
        _put_json_object(s3_client, checks_metadata_object, bucket, checks_metadata_object_path)
    return checks_metadata_paths
