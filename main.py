#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from args import ArgsProcessing
from analysis import Analysis

assert sys.version_info >= (3, 6, 0), 'btm-net-analysis requires Python 3.6+'  # 检查Python版本


if __name__ == '__main__':
    args_info = ArgsProcessing(sys.argv[1:])  # 处理命令行参数
    work_mode = args_info.current_mode
    log_file_list = args_info.log_file_list
    start_time = time.time()
    # 模式1:分析单笔交易 模式2:分析所有交易 模式3:分析单个区块 模式4:分析所有区块
    if work_mode == 1:
        tx_hash = args_info.tx_hash # 交易hash
        for item in log_file_list:
            tx = Analysis(item, tx_hash, type='transaction')
            tx.start()
            # 线程同步
            tx.join()
    elif work_mode == 2:
        pass
    elif work_mode == 3:
        height = args_info.height # 区块高度
        for item in log_file_list:
            block = Analysis(item, height, type='block')
            block.start()
            block.join()
    elif work_mode == 4:
        pass

    print('用时：', time.time()-start_time)