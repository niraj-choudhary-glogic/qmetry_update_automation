# KEY: 68747470733a2f2f74696e7975726c2e636f6d2f6e6b63686f756468617279646576
# Author: Niraj Choudhary
# Email: niraj.choudhary@wbdcontractor.com
# Date: 24 AUG 2024
import json
import os

import requests
from dotenv import load_dotenv

from common.logger import Logger
from config import MainConfig
from utility.utils import write_to_json_file

load_dotenv()
QMETRY_OPEN_API = os.getenv('QMETRY_OPEN_API')


class QMetry:
    def __init__(self, execution_page_id):
        self.log = Logger('QMetry')
        self.execution_page_id = execution_page_id

    def api_call(self, request_type, uri, payload=None, params=None):
        url = f'https://qtmcloud.qmetry.com/rest/api/latest/testcycles/{self.execution_page_id}/{uri}'
        headers = {
            'apiKey': QMETRY_OPEN_API,
            'Content-Type': 'application/json'
        }
        response = requests.request(request_type, url, params=params, headers=headers, data=payload)
        return response

    def get_qmetry_testcases(self, data=None, start_at=0):

        self.log.debug('QMetry: Testcase Fetch from %s', start_at)

        uri = 'testcases/search'
        params = {
            "startAt": start_at,
            "maxResults": 100,
            "fields": "id,summary,versionNo,priority,precondition,testCycleTestCaseMapId,testCaseExecutionId,executionResult,hasDefect,status,created,updated,assignee,seqNo,key,versionNo,summary,priority,status,assignee,executionResult"
        }
        payload = json.dumps({
            "filter": {
                "testCaseStatus": "all"
            }
        })

        response = self.api_call('POST', uri, params=params, payload=payload)
        metadata = response.json()
        if data is None:
            data = metadata
        else:
            data['data'].extend(metadata['data'])
            data['maxResults'] += len(metadata['data'])

        if not metadata['data']:
            self.log.debug('Found [%s] Qmetry Testcases', len(data.get('data', [])))
            return data
        else:
            return self.get_qmetry_testcases(data, start_at=start_at + 100)

    def create_summary_report(self):
        data = []
        testcases = self.get_qmetry_testcases()
        for testcase in testcases['data']:
            meta = {
                "qmetry_testcase_execution_id": testcase['testCaseExecutionId'],
                "qmetry_summary": testcase['summary']
            }
            data.append(meta)

        write_to_json_file(MainConfig.QMETRY_SUMMARY_FILEPATH, data)
        write_to_json_file(MainConfig.QMETRY_FILEPATH, testcases)

    def pass_testcase_by_id(self, testcase_id):
        uri = f"testcase-executions/{testcase_id}"

        payload = json.dumps({
            "executionResultId": 179624  # for Automation Pass result
        })

        response = self.api_call("PUT", uri=uri, payload=payload)

        if response.status_code == 204:
            self.log.debug('Successfully updated the testcase: %s', testcase_id)
        else:
            self.log.warning('Unable to update the testcase')





