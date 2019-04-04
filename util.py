# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta

from log import LogProcessing


def calc_millisecond_interval(earliest_time, latest_time):
    """计算两个日志时间格式的毫秒间隔

    Args:
        earliest_time: 最早的时间
        earliest_time: 最晚的时间

    Returns:
        返回毫秒级的时间间隔
    """
    if earliest_time and latest_time:
        latest_time = LogProcessing.logtime_to_millisecondtimestamp(latest_time)
        earliest_time = LogProcessing.logtime_to_millisecondtimestamp(earliest_time)
        millisecond_interval = abs(latest_time - earliest_time)
        return millisecond_interval
    return None


def millisecond2time_format(millisecond):
    """将毫秒级时间差转为时:分:秒.毫秒的时间格式

    Args:
        millisecond: 毫秒级的时间间隔

    Returns:
        返回时:分:秒.毫秒的时间格式
    """
    second_interval = int(millisecond / 1000)
    millisecond = str(millisecond)[-3:]
    time_interval = '%s.%s' % (timedelta(seconds=second_interval), millisecond)
    return time_interval


def get_average_median(lst):
    """获取有序列表的整数类型的平均值和中位数

    Args:
        lst: 有序列表

    Returns:
        average: 平均值
        median: 中位数
    """
    lst_size = len(lst)
    # 将列表的值累加
    lst_sum = sum(lst)
    average = lst_sum // lst_size
    half = lst_size // 2
    # half取反为负数 负数使用补码表示 补码求原码:取反+1 half取反过程为~half = -(half+1)
    # 列表长度为奇数时 正负索引同指向中间的元素
    # 列表长度为偶数时 正负索引分别指向中间的两个元素
    median = (lst[half] + lst[~half]) // 2
    return average, median


def split_list(lst, num):
    """将列表尽量平均分成指定份数

    Args:
        lst: 一个长列表
        num: 指定的分割份数

    Returns:
        返回一个num个子列表尽量等长的嵌套列表
    """
    avg = len(lst) / float(num)
    out = []
    last = 0.0
    while last < len(lst):
        out.append(lst[int(last):int(last + avg)])
        last += avg
    return out
