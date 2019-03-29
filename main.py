#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from args import ArgsProcessing

assert sys.version_info >= (3, 6, 0), 'btm-net-analysis requires Python 3.6+'  # 检查Python版本


if __name__ == '__main__':
    args_info = ArgsProcessing(sys.argv[1:])  # 处理命令行参数
    work_mode = args_info.current_mode

    if work_mode == 1:
        pass
    elif work_mode == 2:
        pass
    elif work_mode == 3:
        pass
    elif work_mode == 4:
        pass
    else:
        ArgsProcessing.__exit(-1)