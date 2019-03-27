#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from datetime import datetime


def get_current_millisecondtimestamp():
    """获取当前时间的毫秒级的时间戳"""
    millisecondtimestamp = int(round(time.time() * 1000))
    return millisecondtimestamp

def logtime_to_millisecondtimestamp(log_time):
    """将日志中的日期格式转换为毫秒级的时间戳"""
    year_str = str(datetime.now().year)
    # 将年份与日志中的时间拼接
    time_str = f'{year_str} {log_time}'
    # 将时间字符串转为格式化的时间
    d = datetime.strptime(time_str, "%Y %b %d %H:%M:%S.%f")
    # 记录3位的毫秒时间
    microsecend = int(d.microsecond / 1000)
    # 生成秒级时间戳
    timestamp = int(time.mktime(d.timetuple()))
    # 生成毫秒级时间戳
    millisecondtimestamp = timestamp * 1000 + microsecend
    return millisecondtimestamp
