#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from queue import Queue

from args import ArgsProcessing
from log import LogProcessing
from data import DataThread

from util import calc_time_interval

assert sys.version_info >= (3, 6, 0), 'btm-net-analysis requires Python 3.6+'  # 检查Python版本


def main():
    args_info = ArgsProcessing(sys.argv[1:])  # 处理命令行参数
    work_mode = args_info.current_mode
    log_file_list = args_info.log_file_list
    start_time = time.time()
    # 模式1:分析单笔交易 模式2:分析所有交易 模式3:分析单个区块 模式4:分析所有区块
    if work_mode == 1:
        tx_hash = args_info.tx_hash # 交易hash
        # analyze_single(log_file_list, tx_hash, type='transaction')
        all_tx_dict_list = []
        # 所有日志文件中最早的消息
        overall_earliest_msg = []
        # 所有日志文件中最晚的消息
        overall_latest_msg = []
        for log_file in log_file_list:
            data = DataThread(log_file, all_tx_dict_list, type='transaction')
            data.start()
            data.join()
        for tx_dict in all_tx_dict_list:
            if tx_hash in tx_dict:
                data_list = tx_dict[tx_hash]
                earliest_msg = data_list[0]
                latest_msg = data_list[-1]
                print('Earliest_msg: %s' %earliest_msg)
                print('Latest_msg:   %s' %latest_msg)
                if not overall_earliest_msg or LogProcessing.logtime_to_millisecondtimestamp(earliest_msg[0]) \
                    < LogProcessing.logtime_to_millisecondtimestamp(overall_earliest_msg[0]):
                    overall_earliest_msg = earliest_msg
                if not overall_latest_msg or LogProcessing.logtime_to_millisecondtimestamp(latest_msg[0]) \
                    > LogProcessing.logtime_to_millisecondtimestamp(overall_latest_msg[0]):
                    overall_latest_msg = latest_msg
        print('最早: %s' %overall_earliest_msg)
        print('最晚: %s' %overall_latest_msg)
    elif work_mode == 2:
        pass
    elif work_mode == 3:
        height = args_info.height # 区块高度
        all_block_dict_list = []
        # 所有日志文件中最早的消息
        overall_earliest_msg = []
        # 所有日志文件中最晚的消息
        overall_latest_msg = []
        for log_file in log_file_list:
            data = DataThread(log_file, all_block_dict_list, type='block')
            data.start()
            data.join()
        for block_dict in all_block_dict_list:
            if height in block_dict:
                data_list = block_dict[height]
                earliest_msg = data_list[0]
                latest_msg = data_list[-1]
                print('Earliest_msg: %s' %earliest_msg)
                print('Latest_msg:   %s' %latest_msg)
                if not overall_earliest_msg or LogProcessing.logtime_to_millisecondtimestamp(earliest_msg[0]) \
                    < LogProcessing.logtime_to_millisecondtimestamp(overall_earliest_msg[0]):
                    overall_earliest_msg = earliest_msg
                if not overall_latest_msg or LogProcessing.logtime_to_millisecondtimestamp(latest_msg[0]) \
                    > LogProcessing.logtime_to_millisecondtimestamp(overall_latest_msg[0]):
                    overall_latest_msg = latest_msg
        print('最早: %s' %overall_earliest_msg)
        print('最晚: %s' %overall_latest_msg)
        print('间隔: %s' %calc_time_interval(overall_latest_msg[0], overall_earliest_msg[0]))
    elif work_mode == 4:
        pass

    print('分析用时: ', time.time()-start_time)

if __name__ == '__main__':
    main()