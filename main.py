import argparse

from bin.QMetry.qmetry import QMetry
from bin.STBT.stbt import STBT
from common.logger import Logger
from config import MainConfig
from utility.utils import read_from_json_file, write_to_json_file, generate_qmetry_comparison_json

parser = argparse.ArgumentParser(description="Script to interact with QMetry and STBT job categories.")
parser.add_argument('--qmetry_exec_id', type=str, default=None, help='The execution ID in QMetry.')
parser.add_argument('--stbt_job_category', type=str, default=None, help='The category of the STBT job.')
parser.add_argument('--qmetry_update', type=str, default=None, help='The update to be made in QMetry.')
parser.add_argument('--compare_file', type=bool, default=False, help='Will create comparison file with STBT and QMetry')


args = parser.parse_args()
log = Logger('Main')

if args.qmetry_exec_id:
    execution_id = args.qmetry_exec_id
    obj = QMetry(execution_id)
    obj.create_summary_report()

if args.stbt_job_category:
    job_category = args.stbt_job_category
    meta = []
    for job_category in job_category.split(','):
        log.debug('Running for STBT for job category: %s!', job_category)
        stbt_obj = STBT(job_category)
        data = stbt_obj.create_summary_report()
        meta.extend(data)
    write_to_json_file(MainConfig.STBT_SUMMARY_FILEPATH, meta)

if args.compare_file:
    generate_qmetry_comparison_json(MainConfig.QMETRY_SUMMARY_FILEPATH, MainConfig.STBT_SUMMARY_FILEPATH)

if args.qmetry_update:
    execution_id = args.qmetry_update
    obj = QMetry(execution_id)

    data = read_from_json_file(MainConfig.MATCHED_REPORT_QMETRY_STBT)
    for testcase in data:
        testid = testcase['qmetry_testcase_execution_id']
        obj.pass_testcase_by_id(testid)

