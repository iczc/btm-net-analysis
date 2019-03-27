#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import logging
import sys


from args import ProcessArgs

assert sys.version_info >= (3, 6, 0), 'btm-net-analysis requires Python 3.6+'  # check Python version


if __name__ == '__main__':
    input_args = ProcessArgs(sys.argv[1:])  # 处理命令行参数