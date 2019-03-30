#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import datetime


def logtime_to_millisecondtimestamp(log_time):
    """将日志中的日期格式转换为毫秒级的时间戳

    Args:
        log_time: bytomd日志中的时间格式如：Mar 17 00:00:56.009

    Returns:
        返回当前年份加上日志中时间的毫秒级的时间戳，如：1552752056009
    """
    year_str = str(datetime.datetime.now().year)
    # 将年份与日志中的时间拼接
    time_str = year_str + ' ' + log_time
    # 将时间字符串转为格式化的时间
    d = datetime.datetime.strptime(time_str, "%Y %b %d %H:%M:%S.%f")
    # 记录3位的毫秒时间
    millisecond = int(d.microsecond / 1000)
    # 生成秒级时间戳
    timestamp = int(time.mktime(d.timetuple()))
    # 生成毫秒级时间戳
    millisecondtimestamp = timestamp * 1000 + millisecond
    return millisecondtimestamp

def calc_time_interval(earliest_time, latest_time):
    latest_time = logtime_to_millisecondtimestamp(latest_time)
    earliest_time = logtime_to_millisecondtimestamp(earliest_time)
    millisecond_interval = abs(latest_time - earliest_time)
    second_interval = int(millisecond_interval / 1000)
    millisecond = str(millisecond_interval)[-3:]
    time_interval = str(datetime.timedelta(seconds=second_interval)) + '.' + millisecond
    return time_interval