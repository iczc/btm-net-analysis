#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from data import DataThread
from log import LogProcessing

from util import calc_millisecond_interval


def get_all_log_dict(log_file_list, type):
    threads = []
    all_log_dict = []
    for log_file in log_file_list:
        data = DataThread(log_file, all_log_dict, type=type)
        data.start()
        threads.append(data)
    for thread in threads:
        thread.join()
    return all_log_dict

def retrieve_earliest_latest_msg(all_log_dict, dict_key):
    # 所有日志文件中最早的消息
    overall_earliest_msg = []
    # 所有日志文件中最晚的消息
    overall_latest_msg = []
    for log_dict in all_log_dict:
        if dict_key in log_dict:
            data_list = log_dict[dict_key]
            earliest_msg = data_list[0]
            latest_msg = data_list[-1]
            # print('Earliest_msg: %s' %earliest_msg)
            # print('Latest_msg:   %s' %latest_msg)
            # 如果全局的最早的消息为空或消息时间比当前字典中的时间晚则更新
            if not overall_earliest_msg or LogProcessing.logtime_to_millisecondtimestamp(earliest_msg[0]) \
                < LogProcessing.logtime_to_millisecondtimestamp(overall_earliest_msg[0]):
                overall_earliest_msg = earliest_msg
            if not overall_latest_msg or LogProcessing.logtime_to_millisecondtimestamp(latest_msg[0]) \
                > LogProcessing.logtime_to_millisecondtimestamp(overall_latest_msg[0]):
                overall_latest_msg = latest_msg
    return overall_earliest_msg, overall_latest_msg

def calc_broadcasting_time(work_queue, broadcasting_time_queue, all_log_dict):
    while True:
        dict_key = work_queue.get()
        overall_earliest_msg, overall_latest_msg = retrieve_earliest_latest_msg(all_log_dict, dict_key)
        millisecond_interval = calc_millisecond_interval(overall_latest_msg[0], overall_earliest_msg[0])
        broadcasting_time_queue.put(millisecond_interval)
        if work_queue.empty():
            break