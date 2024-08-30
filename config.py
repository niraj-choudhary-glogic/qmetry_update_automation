# KEY: 68747470733a2f2f74696e7975726c2e636f6d2f6e6b63686f756468617279646576
# Author: Niraj Choudhary
# Email: niraj.choudhary@wbdcontractor.com
# Date: 26 JUL 2024

""""Configuration File"""


class MainConfig:
    LOGGER_FILENAME = False
    LOGGER_LEVEL = 'DEBUG'

    # Reporting FILEPATHS
    STBT_SUMMARY_FILEPATH = 'dump/temp/stbt_summary.json'
    STBT_FILEPATH = 'dump/temp/stbt.json'
    QMETRY_SUMMARY_FILEPATH = 'dump/temp/qmetry_summary.json'
    QMETRY_FILEPATH = 'dump/temp/qmetry.json'
    MATCHED_REPORT_QMETRY_STBT = 'dump/temp/matched_summaries.json'


