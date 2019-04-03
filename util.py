#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta

from log import LogProcessing


def calc_millisecond_interval(earliest_time, latest_time):
    if earliest_time and latest_time:
        latest_time = LogProcessing.logtime_to_millisecondtimestamp(latest_time)
        earliest_time = LogProcessing.logtime_to_millisecondtimestamp(earliest_time)
        millisecond_interval = abs(latest_time - earliest_time)
        return millisecond_interval

def millisecond2time_format(millisecond):
    second_interval = int(millisecond / 1000)
    millisecond = str(millisecond)[-3:]
    time_interval = '%s.%s' %(timedelta(seconds=second_interval), millisecond)
    return time_interval

def get_average_median(list):
    list_size = len(list)
    list_sum = sum(list)
    average = list_sum / list_size
    half = list_size // 2
    # half取反为负数 负数使用补码表示 补码求原码:取反+1 half取反过程为~half = -(half+1)
    # 列表长度为奇数时 正负索引同指向中间的元素
    # 列表长度为偶数时 正负索引分别指向中间的两个元素
    median = (list[half] + list[~half]) / 2
    return int(average), int(median)

def split_list(lst, num):
    avg = len(lst) / float(num)
    out = []
    last = 0.0
    while last < len(lst):
        out.append(lst[int(last):int(last + avg)])
        last += avg
    return out
