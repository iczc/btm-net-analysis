#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from args import ArgsProcessing

from analyze import get_all_log_dict
from analyze import retrieve_earliest_latest_msg
from util import calc_millisecond_interval
from util import millisecond2time_format
from util import get_average_median

assert sys.version_info >= (3, 6, 0), 'btm-net-analysis requires Python 3.6+'  # 检查Python版本


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
            interval_time = millisecond2time_format(calc_millisecond_interval(overall_latest_msg[0], overall_earliest_msg[0]))
            print('间隔: %s' %interval_time)
        else:
            print('The transaction %s was not found in log file!' %tx_hash)
    elif work_mode == 2:
        all_tx_dict_list = get_all_log_dict(log_file_list, type='transaction')
        broadcasting_time = []
        all_tx_hash = []
        for tx_dict in all_tx_dict_list:
            all_tx_hash.extend(list(tx_dict.keys()))
        # 去除重复元素
        all_tx_hash = list(set(all_tx_hash))
        for tx_hash in all_tx_hash:
            overall_earliest_msg, overall_latest_msg = retrieve_earliest_latest_msg(all_tx_dict_list, tx_hash)
            millisecond_interval = calc_millisecond_interval(overall_latest_msg[0], overall_earliest_msg[0])
            # print('tx %s : %s' %(tx_hash, millisecond_interval))
            broadcasting_time.append(millisecond_interval)
        broadcasting_time.sort()
        average, median = get_average_median(broadcasting_time)
        print('最短时间: %s' %millisecond2time_format(broadcasting_time[0]))
        print('最长时间: %s' %millisecond2time_format(broadcasting_time[-1]))
        print('平均值:   %s' %millisecond2time_format(average))
        print('中位数:   %s' %millisecond2time_format(median))
    elif work_mode == 3:
        height = args_info.height # 区块高度
        all_block_dict_list = get_all_log_dict(log_file_list, type='block')
        overall_earliest_msg, overall_latest_msg = retrieve_earliest_latest_msg(all_block_dict_list, height)
        if overall_earliest_msg and overall_latest_msg:
            print('最早: %s' %overall_earliest_msg)
            print('最晚: %s' %overall_latest_msg)
            interval_time = millisecond2time_format(calc_millisecond_interval(overall_latest_msg[0], overall_earliest_msg[0]))
            print('间隔: %s' %interval_time)
        else:
            print('The block height %s was not found in log file!' %height)
    elif work_mode == 4:
        all_block_dict_list = get_all_log_dict(log_file_list, type='block')
        broadcasting_time = []
        all_block_height = []
        for block_dict in all_block_dict_list:
            all_block_height.extend(list(block_dict.keys()))
        all_block_height = list(set(all_block_height))
        for height in all_block_height:
            overall_earliest_msg, overall_latest_msg = retrieve_earliest_latest_msg(all_block_dict_list, height)
            millisecond_interval = calc_millisecond_interval(overall_latest_msg[0], overall_earliest_msg[0])
            # print('height %s : %s' %(height, millisecond2time_format(millisecond_interval)))
            broadcasting_time.append(millisecond_interval)
        broadcasting_time.sort()
        average, median = get_average_median(broadcasting_time)
        print('最短时间: %s' %millisecond2time_format(broadcasting_time[0]))
        print('最长时间: %s' %millisecond2time_format(broadcasting_time[-1]))
        print('平均值:   %s' %millisecond2time_format(average))
        print('中位数:   %s' %millisecond2time_format(median))

    print('分析用时:', time.time()-start_time)

if __name__ == '__main__':
    main()
