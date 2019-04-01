#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta

from log import LogProcessing


def calc_time_interval(earliest_time, latest_time):
    latest_time = LogProcessing.logtime_to_millisecondtimestamp(latest_time)
    earliest_time = LogProcessing.logtime_to_millisecondtimestamp(earliest_time)
    millisecond_interval = abs(latest_time - earliest_time)
    second_interval = int(millisecond_interval / 1000)
    millisecond = str(millisecond_interval)[-3:]
    time_interval = '%s.%s' %(timedelta(seconds=second_interval), millisecond)
    return time_interval