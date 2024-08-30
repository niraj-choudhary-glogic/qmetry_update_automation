# KEY: 68747470733a2f2f74696e7975726c2e636f6d2f6e6b63686f756468617279646576
# Author: Niraj Choudhary
# Email: niraj.choudhary@wbdcontractor.com
# Date: 26 JUL 2024

"""This file contains the definition for the Logger class"""

import logging
import sys

from colorama import Fore, Style, init

from config import MainConfig

# Applications should initialise Colorama using
init()

LOG_FORMAT = [
    '%(asctime)s.%(msecs)03d',
    '%(name)s',
    '%(levelname)s',
    '%(message)s',
]

LOG_DATE_FORMAT = '%m-%d-%Y %H:%M:%S'

COLORS = {
    'RESET': Style.RESET_ALL,
    logging.DEBUG: Fore.CYAN + Style.BRIGHT,
    logging.INFO: Fore.GREEN + Style.BRIGHT,
    logging.WARN: Fore.YELLOW + Style.BRIGHT,
    logging.ERROR: Fore.RED + Style.BRIGHT,
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
}


class Logger(logging.Logger):
    INFO = logging.INFO
    WARN = logging.WARN
    DEBUG = logging.DEBUG
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self, name):
        """Initializes the logger"""
        log_format = LOG_FORMAT

        # Set console handler
        if MainConfig.LOGGER_FILENAME:
            console_handler = logging.FileHandler(MainConfig.LOGGER_FILENAME)
        else:
            console_handler = logging.StreamHandler(sys.stdout)

        # Set log level, default will be INFO
        level = MainConfig.LOGGER_LEVEL
        level = getattr(logging, level if level else 'INFO')

        formatter = logging.Formatter(' - '.join(log_format), LOG_DATE_FORMAT)
        console_handler.setFormatter(formatter)

        super(Logger, self).__init__(name, level)
        self.addHandler(console_handler)

    @staticmethod
    def colorize(color, message):
        return '%s%s%s' % (color, message, COLORS['RESET'])

    def _log(self, level, msg, args, exc_info=None, extra=None, color=None,
             **kwargs):

        if color is None:
            color = COLORS[level]

        msg = self.colorize(color=color, message=msg)
        super(Logger, self)._log(level, msg, args, exc_info, extra)

    def debug(self, msg, *args, **kwargs):
        return super(Logger, self).debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return super(Logger, self).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return super(Logger, self).warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return super(Logger, self).error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        return super(Logger, self).critical(msg, *args, **kwargs)

    def setLevel(self, level):
        return super(Logger, self).setLevel(level)
