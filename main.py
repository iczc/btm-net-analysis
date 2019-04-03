#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from multiprocessing import Process, Queue, cpu_count

from args import ArgsProcessing

from analyze import get_all_log_dict
from analyze import retrieve_earliest_latest_msg
from analyze import calc_broadcasting_time
from util import calc_millisecond_interval
from util import millisecond2time_format
from util import get_average_median
from util import split_list

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
        all_tx_hash = []
        for tx_dict in all_tx_dict_list:
            all_tx_hash.extend(list(tx_dict.keys()))
        # 去除重复元素
        all_tx_hash = list(set(all_tx_hash))
        broadcasting_time_queue = Queue()
        processes = []
        processor_num = cpu_count()
        split_all_tx_hash = split_list(all_tx_hash, processor_num)
        for work_list in split_all_tx_hash:
            p = Process(target=calc_broadcasting_time, args=(work_list, broadcasting_time_queue, all_tx_dict_list))
            p.start()
            processes.append(p)
        for process in processes:
            process.join()
        broadcasting_time_list = []
        while True:
            broadcasting_time_list.extend(broadcasting_time_queue.get())
            if broadcasting_time_queue.empty():
                break
        broadcasting_time_list.sort()
        average, median = get_average_median(broadcasting_time_list)
        print('最短时间: %s' %millisecond2time_format(broadcasting_time_list[0]))
        print('最长时间: %s' %millisecond2time_format(broadcasting_time_list[-1]))
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
        all_block_height = []
        for block_dict in all_block_dict_list:
            all_block_height.extend(list(block_dict.keys()))
        all_block_height = list(set(all_block_height))
        broadcasting_time_queue = Queue()
        processes = []
        processor_num = cpu_count()
        split_all_block_height = split_list(all_block_height, processor_num)
        for work_list in split_all_block_height:
            p = Process(target=calc_broadcasting_time, args=(work_list, broadcasting_time_queue, all_block_dict_list))
            p.start()
            processes.append(p)
        for process in processes:
            process.join()
        broadcasting_time_list = []
        while True:
            broadcasting_time_list.extend(broadcasting_time_queue.get())
            if broadcasting_time_queue.empty():
                break
        broadcasting_time_list.sort()
        average, median = get_average_median(broadcasting_time_list)
        print('最短时间: %s' %millisecond2time_format(broadcasting_time_list[0]))
        print('最长时间: %s' %millisecond2time_format(broadcasting_time_list[-1]))
        print('平均值:   %s' %millisecond2time_format(average))
        print('中位数:   %s' %millisecond2time_format(median))

    print('分析用时:', time.time()-start_time)

if __name__ == '__main__':
    main()
