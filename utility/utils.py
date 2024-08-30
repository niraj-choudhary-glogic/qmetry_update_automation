# KEY: 68747470733a2f2f74696e7975726c2e636f6d2f6e6b63686f756468617279646576
# Author: Niraj Choudhary
# Email: niraj.choudhary@wbdcontractor.com
# Date: 26 JUL 2024
import difflib
import json
import os
import platform
import random
import re
import subprocess
import sys
import time
from datetime import date, timedelta, datetime
from importlib import reload
from io import BytesIO
from pathlib import Path

import pytz
import requests
from PIL import Image
from dotenv import load_dotenv

from common.logger import Logger
from common.loop import Loop
from config import MainConfig

load_dotenv()

log = Logger(name='Utility')


def pause(wait=None):
    if wait is not None:
        # Only log if waiting time is longer then 10 seconds
        if wait > 10:
            log.info('Waiting for {} seconds'.format(wait))
            loop = Loop(max_elapsed_time=wait, log_freq=True)

            while (loop.loop() is True):
                continue

        else:
            # log.debug('Waiting for {} seconds'.format(wait))
            time.sleep(wait)
    else:
        time.sleep(0.5)


def read_from_json_file(filepath, default=False):
    """
    if json is present then return json data else bool
    :return:
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
        return data
    except Exception as exc:
        log.warning(f"Exception occur during reading file: %s", exc)
        return dict() if default else False


def write_to_json_file(filepath, data):
    """
    write dictionary data to json file
    :param data: json formatted data
    :param filepath: dictionary format
    :return: bool
    """

    try:
        if not os.path.exists(filepath):
            path = Path(filepath)
            dirname = str(path.parent) if '.' in path.name else filepath
            log.info('Creating: %s', filepath)
            os.makedirs(dirname, exist_ok=True)

        with open(filepath, 'w') as file:
            file.write(json.dumps(data, indent=4))

        # print(f"Configuration file successfully modified!")
        return True
    except Exception as exc:
        print(f"Unable to write data {exc}")
        return False


def quantity_progress_bar(process, total, tag='Unknown'):
    percent = "{0:.1f}".format(100 * (process / total))
    fill_len = int(50 * process / total) + 1
    bar = "*" * fill_len + '-' * (50 - fill_len)

    print('\rProgress |%s| %s%% | %s ' % (bar, percent, tag), end="\r")


def get_similarity_ratio(str1, str2):
    """Calculate the similarity ratio between two strings."""
    return difflib.SequenceMatcher(None, str1, str2).ratio()


def generate_qmetry_comparison_json(qmetry_filepath, stbt_filepath, threshold=0.85):
    qmetry_summaries = read_from_json_file(qmetry_filepath)
    stbt_summaries = read_from_json_file(stbt_filepath)

    # Create a list to store matched results
    matched_summaries = []

    # Set the similarity threshold (70% match)
    similarity_threshold = threshold

    # Iterate through each item in stbt_summaries
    for stbt_item in stbt_summaries:
        stbt_summary = stbt_item.get('summary')

        # Find the corresponding item in qmetry_summaries based on the summary/qmetry_summary match
        for qmetry_item in qmetry_summaries:
            qmetry_summary = qmetry_item.get('qmetry_summary')
            similarity = get_similarity_ratio(stbt_summary, qmetry_summary)

            if similarity >= similarity_threshold:
                # Create a dictionary to store the matched summary with additional details
                matched_summary = {
                    'stbt_result': stbt_item.get('result'),
                    'stbt_summary': stbt_summary,
                    'qmetry_summary': qmetry_summary,
                    'qmetry_testcase_execution_id': qmetry_item.get('qmetry_testcase_execution_id'),
                    'similarity': round(similarity, 2)
                }
                matched_summaries.append(matched_summary)
                break  # Exit the inner loop once a match is found

    log.info('Matched: [%s]', len(matched_summaries))

    write_to_json_file(MainConfig.MATCHED_REPORT_QMETRY_STBT, matched_summaries)








