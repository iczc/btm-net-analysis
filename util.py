#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from datetime import datetime


def get_current_millisecondtimestamp():
    """获取当前时间的毫秒级的时间戳

    Returns:
        返回整形的当前时间毫秒级的时间戳，如：1553752750058
    """
    millisecondtimestamp = int(round(time.time() * 1000))
    return millisecondtimestamp


def logtime_to_millisecondtimestamp(log_time):
    """将日志中的日期格式转换为毫秒级的时间戳

    Args:
        log_time: bytomd日志中的时间格式如：Mar 17 00:00:56.009

    Returns:
        返回当前年份加上日志中时间的毫秒级的时间戳，如：1552752056009
    """
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


def millisecondtimestamp_to_logtime(millisecondtimestamp):
    """将毫秒级的时间戳转换为日志中的日期格式

    Args:
        millisecondtimestamp: 毫秒级的时间戳，如：1552752056009

    Returns:
        返回bytomd日志中的时间格式，如：Mar 17 00:00:56.009
    """
    # 截取后三位为毫秒时间
    microsecend = str(millisecondtimestamp)[-3:]
    # 计算秒级时间戳
    timestamp = int(millisecondtimestamp / 1000)
    struct_time = time.localtime(timestamp)
    # 生成格式化的日志时间
    log_time = time.strftime("%b %d %H:%M:%S", struct_time)
    # 拼接毫秒
    log_time = log_time + '.' + microsecend
    return log_time
