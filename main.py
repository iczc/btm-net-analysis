#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from queue import Queue

from args import ArgsProcessing
from log import LogProcessing
from analysis import AnalysisThread

from util import calc_time_interval

assert sys.version_info >= (3, 6, 0), 'btm-net-analysis requires Python 3.6+'  # 检查Python版本


def analyze_single(log_file_list, parameter, type):
    overall_earliest_msg = []
    overall_latest_msg = []
    q = Queue(len(log_file_list) * 2)
    for file in log_file_list:
        tx = AnalysisThread(q, file, parameter, type=type)
        tx.start()
        tx.join()
    if q.empty():
        print('The %s %s was not found in log file!' %(type, parameter))
        sys.exit(0)
    while True:
        # 队列长度为偶数时队列头部为最早的时间
        if (q.qsize() % 2 == 0):
            earliest_msg = q.get()
            print('Earliest_msg: %s' %earliest_msg)
            # 如果全局的最早时间为空或大于队列中的时间则更新
            if not overall_earliest_msg or LogProcessing.logtime_to_millisecondtimestamp(earliest_msg[0]) \
                < LogProcessing.logtime_to_millisecondtimestamp(overall_earliest_msg[0]):
                overall_earliest_msg = earliest_msg
        else:
            latest_msg = q.get()
            print('Latest_msg:   %s' %latest_msg)
            if not overall_latest_msg or LogProcessing.logtime_to_millisecondtimestamp(latest_msg[0]) \
                > LogProcessing.logtime_to_millisecondtimestamp(overall_latest_msg[0]):
                overall_latest_msg = latest_msg
        if q.empty():
            break
    print('最早: %s' %overall_earliest_msg)
    print('最晚: %s' %overall_latest_msg)
    print('间隔: %s' %calc_time_interval(overall_latest_msg[0], overall_earliest_msg[0]))

def main():
    args_info = ArgsProcessing(sys.argv[1:])  # 处理命令行参数
    work_mode = args_info.current_mode
    log_file_list = args_info.log_file_list
    start_time = time.time()
    # 模式1:分析单笔交易 模式2:分析所有交易 模式3:分析单个区块 模式4:分析所有区块
    if work_mode == 1:
        tx_hash = args_info.tx_hash # 交易hash
        analyze_single(log_file_list, tx_hash, type='transaction')
    elif work_mode == 2:
        pass
    elif work_mode == 3:
        height = args_info.height # 区块高度
        analyze_single(log_file_list, height, type='block')
    elif work_mode == 4:
        pass
    print('分析用时: ', time.time()-start_time)

if __name__ == '__main__':
    main()