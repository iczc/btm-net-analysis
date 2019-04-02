#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time


from args import ArgsProcessing
from log import LogProcessing
from data import DataThread

from util import calc_time_interval

assert sys.version_info >= (3, 6, 0), 'btm-net-analysis requires Python 3.6+'  # 检查Python版本


def get_all_log_dict(log_file_list, type):
    all_log_dict = []
    for log_file in log_file_list:
        data = DataThread(log_file, all_log_dict, type=type)
        data.start()
        data.join()
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
            print('Earliest_msg: %s' %earliest_msg)
            print('Latest_msg:   %s' %latest_msg)
            # 如果全局的最早的消息为空或消息时间比当前字典中的时间晚则更新
            if not overall_earliest_msg or LogProcessing.logtime_to_millisecondtimestamp(earliest_msg[0]) \
                < LogProcessing.logtime_to_millisecondtimestamp(overall_earliest_msg[0]):
                overall_earliest_msg = earliest_msg
            if not overall_latest_msg or LogProcessing.logtime_to_millisecondtimestamp(latest_msg[0]) \
                > LogProcessing.logtime_to_millisecondtimestamp(overall_latest_msg[0]):
                overall_latest_msg = latest_msg
    return overall_earliest_msg, overall_latest_msg


def main():
    args_info = ArgsProcessing(sys.argv[1:])  # 处理命令行参数
    work_mode = args_info.current_mode
    log_file_list = args_info.log_file_list
    start_time = time.time()
    # 模式1:分析单笔交易 模式2:分析所有交易 模式3:分析单个区块 模式4:分析所有区块
    if work_mode == 1:
        tx_hash = args_info.tx_hash # 交易hash
        all_tx_dict_list = get_all_log_dict(log_file_list, type='transaction')
        overall_earliest_msg, overall_latest_msg = retrieve_earliest_latest_msg(all_tx_dict_list, tx_hash)
        if overall_earliest_msg and overall_latest_msg:
            print('最早: %s' %overall_earliest_msg)
            print('最晚: %s' %overall_latest_msg)
            print('间隔: %s' %calc_time_interval(overall_latest_msg[0], overall_earliest_msg[0]))
        else:
            print('The transaction %s was not found in log file!' %tx_hash)
    elif work_mode == 2:
        all_tx_dict_list = get_all_log_dict(log_file_list, type='transaction')
    elif work_mode == 3:
        height = args_info.height # 区块高度
        all_block_dict_list = get_all_log_dict(log_file_list, type='block')
        overall_earliest_msg, overall_latest_msg = retrieve_earliest_latest_msg(all_block_dict_list, height)
        if overall_earliest_msg and overall_latest_msg:
            print('最早: %s' %overall_earliest_msg)
            print('最晚: %s' %overall_latest_msg)
            print('间隔: %s' %calc_time_interval(overall_latest_msg[0], overall_earliest_msg[0]))
        else:
            print('The block height %s was not found in log file!' %height)
    elif work_mode == 4:
        all_block_dict_list = get_all_log_dict(log_file_list, type='block')

    print('分析用时: ', time.time()-start_time)

if __name__ == '__main__':
    main()