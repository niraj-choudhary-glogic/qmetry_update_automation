# KEY: 68747470733a2f2f74696e7975726c2e636f6d2f6e6b63686f756468617279646576
# Author: Niraj Choudhary
# Email: niraj.choudhary@wbdcontractor.com
# Date: 24 AUG 2024
import os
import re

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from common.logger import Logger
from config import MainConfig
from utility.utils import write_to_json_file, quantity_progress_bar

load_dotenv()
STBT_API_TOKEN = os.getenv('STBT_API_TOKEN')


class STBT:
    def __init__(self, job_category):
        self.log = Logger('STBT')
        self.job_category = job_category.strip()

    def api_call(self, request_type, uri, params=None, payload=None):
        url = f"https://hbo.stb-tester.com/api/v2{uri}"
        # Set up the headers with the API key
        headers = {
            "Authorization": f"token {STBT_API_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.request(request_type, url, params=params, headers=headers, data=payload)
        return response

    def api_get_testcases_run(self):

        url = f"/results?filter=category:{self.job_category}"
        response = self.api_call("GET", url)

        return response.json()

    def _api_get_each_testcase(self, url):
        """This method use internally for getting url from job_category and then individually fetch result for each test
        """
        url = f"/results{url}?private_fields=1"
        response = self.api_call("GET", url)

        return response.json()

    def _get_scenario_text(self, steps_html):
        """This will only get text of scenario so that it can use in different method for comparison"""

        try:

            soup = BeautifulSoup(steps_html, "html.parser")
            scenario_text = soup.find("span", class_="keyword", string="Scenario:").find_next_sibling("span", class_="name").text

            return scenario_text
        except Exception as exc:
            self.log.warning('Unable to process Scenario due to %s', exc)

    def _get_testcaseid_text(self, steps_html):
        """This will only get text of scenario so that it can use in different method for comparison"""

        try:

            soup = BeautifulSoup(steps_html, "html.parser")
            # Find the first occurrence of the pattern @C followed by digits
            match = re.search(r'@C\d+', soup.get_text())

            # Print the first match if found
            if match:
                return match.group()

        except Exception as exc:
            self.log.warning('Unable to process testcaseid due to %s', exc)

    def create_summary_report(self):
        testcases_run = self.api_get_testcases_run()

        _pass, _fail, _error = 0, 0, 0
        data = []

        for index, urls in enumerate(testcases_run):
            if urls['result'] == "pass":
                _pass += 1

                quantity_progress_bar(index, len(testcases_run), urls['result_id'])

                each_testcase = self._api_get_each_testcase(urls['result_id'])
                meta = {
                    "result": each_testcase['result'],
                    "summary": self._get_scenario_text(each_testcase['steps_html']),
                    "testcaseid": self._get_testcaseid_text(each_testcase['steps_html'])
                }

                data.append(meta)

            elif urls['result'] == "fail":
                _fail += 1
            else:
                _error += 1

        write_to_json_file(MainConfig.STBT_SUMMARY_FILEPATH, data)
        write_to_json_file(MainConfig.STBT_FILEPATH, testcases_run)

        self.log.info("Results: Pass: %s, Fail: %s, Error: %s", _pass, _fail, _error)
        return data
