#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from args import ArgsProcessing
from analyze.block import BlockAnalysis
from analyze.transaction import TransactionAnalysis
from util import logtime_to_millisecondtimestamp

assert sys.version_info >= (3, 6, 0), 'btm-net-analysis requires Python 3.6+'  # 检查Python版本


if __name__ == '__main__':
    args_info = ArgsProcessing(sys.argv[1:])  # 处理命令行参数
    work_mode = args_info.current_mode
    log_file_list = args_info.log_file_list
    # 模式1:分析单笔交易 模式2:分析所有交易 模式3:分析单个区块 模式4:分析所有区块
    if work_mode == 1:
        all_earliest_msg = []
        all_latest_msg = []
        tx_hash = args_info.tx_hash # 交易hash
        for item in log_file_list:
            tx = TransactionAnalysis(item)
            if tx.analyze_transaction(tx_hash):
                print('The earliest msg and latest msg in %s:' %item)
                print(tx.earliest_msg)
                print(tx.latest_msg)
                all_earliest_msg.append(tx.earliest_msg)
                all_latest_msg.append(tx.latest_msg)
            else:
                print('The transaction %s was not found in %s' %(tx_hash, item))
        # 判断所有的最早的消息列表和最晚的消息列表不为空
        if all_earliest_msg and all_latest_msg:
            overall_earliest_msg = min(all_earliest_msg, key=lambda msg: logtime_to_millisecondtimestamp(msg[0]))
            overall_latest_msg = max(all_latest_msg, key=lambda msg: logtime_to_millisecondtimestamp(msg[0]))
            print(overall_earliest_msg)
            print(overall_latest_msg)
        else:
            print('The transaction %s was not found in all log file' %tx_hash)
    elif work_mode == 2:
        pass
    elif work_mode == 3:
        all_earliest_msg = []
        all_latest_msg = []
        height = args_info.height # 区块高度
        for item in log_file_list:
            block = BlockAnalysis(item)
            if block.analyze_block(height):
                print('The earliest msg and latest msg in %s:' %item)
                print(block.earliest_msg)
                print(block.latest_msg)
                all_earliest_msg.append(block.earliest_msg)
                all_latest_msg.append(block.latest_msg)
            else:
                print('The height %s was not found in %s' %(height, item))
        if all_earliest_msg and all_latest_msg:
            overall_earliest_msg = min(all_earliest_msg, key=lambda msg: logtime_to_millisecondtimestamp(msg[0]))
            overall_latest_msg = max(all_latest_msg, key=lambda msg: logtime_to_millisecondtimestamp(msg[0]))
            print(overall_earliest_msg)
            print(overall_latest_msg)
        else:
            print('The height %s was not found in all log file' %height)
    elif work_mode == 4:
        pass