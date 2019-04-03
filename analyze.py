"""
数据分析中使用到的方法
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from array import array

from data import DataThread
from log import LogProcessing
from util import calc_millisecond_interval


def get_all_log_dict(log_file_list, analysis_type):
    """创建与日志文件数量子进程并获取所有交易或区块的字典格式的数据

    Args:
        log_file_list: 存储日志文件路径的列表
        analysis_type: 需要的数据类型，transaction或block

    Returns:
        返回列表列表嵌套字典的所有日志文件交易或区块字典格式的数据
    """
    threads = []
    all_log_dict = []
    for log_file in log_file_list:
        data = DataThread(log_file, all_log_dict, analysis_type)
        data.start()
        threads.append(data)
    for thread in threads:
        thread.join()
    return all_log_dict


def retrieve_earliest_latest_msg(all_log_dict, dict_key):
    """检索交易或区块最早出现时间和最晚出现时间的消息

    Args:
        all_log_dict: 所有的交易或区块字典格式的数据
        dict_key: 用于检索的字典key，为交易Hash或区块高度

    Returns:
        返回交易或区块在所有日志文件中最早出现时间和最晚出现
        时间的消息，每个消息由列表存储，包括时间和节点ip:端口
    """
    # 所有日志文件中最早的消息
    overall_earliest_msg = []
    # 所有日志文件中最晚的消息
    overall_latest_msg = []
    for log_dict in all_log_dict:
        if dict_key in log_dict:
            data_list = log_dict[dict_key]
            earliest_msg = data_list[0]
            latest_msg = data_list[-1]
            # print('Earliest_msg: %s' % earliest_msg)
            # print('Latest_msg:   %s' % latest_msg)
            # 如果全局的最早的消息为空或消息时间比当前字典中的时间晚则更新
            if not overall_earliest_msg or LogProcessing.logtime_to_millisecondtimestamp(earliest_msg[0]) \
                    < LogProcessing.logtime_to_millisecondtimestamp(overall_earliest_msg[0]):
                overall_earliest_msg = earliest_msg
            if not overall_latest_msg or LogProcessing.logtime_to_millisecondtimestamp(latest_msg[0]) \
                    > LogProcessing.logtime_to_millisecondtimestamp(overall_latest_msg[0]):
                overall_latest_msg = latest_msg
    return overall_earliest_msg, overall_latest_msg


def calc_broadcasting_time(work_list, broadcasting_time_queue, all_log_dict):
    """子进程执行的方法，用于计算最早出现时间与最晚出现时间的时间差，即广播时间

    Args:
        work_list: 任务列表，为交易Hash或区块高度
        broadcasting_time_queue: 存储广播时间的队列，用于父子进程通信(管道加互斥锁实现)
        all_log_dict: 所有的交易或区块字典格式的数据
    """
    # 无符号的长整型数组 用于存储毫秒表示的广播时间
    broadcasting_time_array = array('L')
    for dict_key in work_list:
        overall_earliest_msg, overall_latest_msg = retrieve_earliest_latest_msg(all_log_dict, dict_key)
        millisecond_interval = calc_millisecond_interval(overall_latest_msg[0], overall_earliest_msg[0])
        broadcasting_time_array.append(millisecond_interval)
    # 将该子进程中的分析结果通过queue发送给父进程
    broadcasting_time_queue.put(broadcasting_time_array)
