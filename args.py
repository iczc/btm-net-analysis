#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import logging
import sys


class ProcessArgs:
    """
    处理命令行参数
    """
    def __init__(self, argv):
        """初始化命令行参数、类属性并解析命令行参数"""
        self.__argv = argv # 设置命令行设置
        self.current_mode = 0 # 模式1:分析单笔交易 模式2:分析所有交易 模式3:分析单个区块 模式4:分析所有区块
        self.height = None # 区块高度
        self.tx_hash = None # 交易Hash
        self.__parse_args()  # 解析参数
    
    def __parse_args(self):
        """解析命令行参数并设置工作模式、交易Hash或区块高度"""
        # 如果不存在命令行参数打印帮助后退出
        if not self.__argv:
            self.__exit(0)
        # 如果使用了的命令行参数超过一个打印帮助后退出
        if len(self.__argv) > 2:
            print('Only one of -t/--transaction and -b/--block can be used!')
            self.__exit(-1)
        # 解析命令行参数
        try:
            opts, args = getopt.getopt(self.__argv, 'hb:t:', ['help', 'block=', 'transaction='])
        except getopt.GetoptError as err:
            logging.error('%s', str(err))
            self.__exit(-1)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.__exit(0)
            elif opt in ('-t', '--transaction'):
                if arg == 'all':
                    self.current_mode = 2
                # 判读传入的交易id是否为长度64的tx_hash
                elif len(arg) == 64:
                    self.current_mode = 1
                    self.tx_hash = arg
                else:
                    print('Please confirm the parameter is transaction hash!')
                    self.__exit(-1)
            elif opt in ('-b', '--block'):
                # 判读参数是否为all
                if arg == 'all':
                    self.current_mode = 4
                # 判断传入的区块高度的字符串是否是数字内容
                elif arg.isdigit():
                    self.current_mode = 3
                    self.height = int(arg)
                else:
                    print('Please confirm the parameter is block height!')
                    self.__exit(-1)
            else:
                logging.error('unhandled option')
                self.__exit(-1)
        self.__print_args()

    @staticmethod
    def __exit(exit_code):
        """打印使用帮助并使用传入的错误码退出程序"""
        print("\nUsage: main.py "
            "[-h/--help] "
            "[-t/--transaction <tx_hash>/all]"
            "[-b/--block <block_height>/all] ")
        sys.exit(exit_code)

    def __print_args(self):
        """打印参数信息"""
        mode_info = ['', 'Analyze a transaction', 'Analyze all transactions', 'Analyze a block', 'Analyze all blocks']
        print('current mode is %s' %(mode_info[self.current_mode]))
        if self.current_mode == 1:
            print('transaction id is %s' %self.tx_hash)
        elif self.current_mode == 3:
            print('block height is %s' %self.height)
