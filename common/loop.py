# KEY: 68747470733a2f2f74696e7975726c2e636f6d2f6e6b63686f756468617279646576
# Author: Niraj Choudhary
# Email: niraj.choudhary@wbdcontractor.com
# Date: 26 JUL 2024

import time
from datetime import timedelta

from common.logger import Logger


class Loop:
    """
    Loop to keep executing statement until maximum timeout or iteration encounter

    :param max_iterations: Number of iteration to keep loop running
    :param max_elapsed_time: Number of seconds to keep loop running
    :param time_log_freq: Frequency of logging remaining time
    :param log_freq: Enable logging remaining time or iteration
    """
    def __init__(self, max_iterations=None, max_elapsed_time=None,
                 time_log_freq=10, log_freq=False):

        self.max_iterations = max_iterations
        self.max_elapsed_time = max_elapsed_time

        self.start_time = None
        self.iterations = 0

        self.last_time_log = 0
        self.time_log_freq = time_log_freq

        # Only log Remaining time if log_freq=True
        self.log_freq = log_freq

        self.log = Logger(name='loop')

        if max_iterations is None and max_elapsed_time is None:
            raise Exception('max_iterations or max_elapsed_time must be specified')

    def _set_start_time(self):
        """Sets the start time for the loop"""
        self.start_time = time.time()
        self.log.debug('Setting start time to %s', self.start_time)

    @property
    def time_remaining(self):
        """Return remaining time with respect to max elapsed time

        :return time_remaining: timeout - now
        """

        time_remaining = 0
        if (self.max_elapsed_time is not None):
            time_remaining = self.start_time + self.max_elapsed_time - time.time()

            if time_remaining < 0:
                time_remaining = 0

        return time_remaining

    def loop(self):
        """looping statement until timeout

        return: boolean
        """

        if self.start_time is None:
            self._set_start_time()

        if (self.max_iterations is not None and self.iterations >= self.max_iterations):
            self.log.info('Max number of iterations {} exceeded'.format(self.iterations))
            return False

        if (
                self.max_elapsed_time is not None and
                time.time() >= self.start_time + self.max_elapsed_time
        ):
            self.log.info(
                'Max elapsed time ({} second{}) exceeded'.format(
                    self.max_elapsed_time,
                    's' if self.max_elapsed_time != 1 else ''
                )
            )
            return False

        if(
                self.max_elapsed_time is not None and
                self.last_time_log + self.time_log_freq < time.time() and
                self.log_freq is True
        ):
            self.log.info("Remaining time: {}".format(
                str(timedelta(seconds=int(self.time_remaining)))
            ))
            self.last_time_log = time.time()

        self.iterations += 1
        return True
