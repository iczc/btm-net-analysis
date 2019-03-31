#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import logging
import os
import sys


class ArgsProcessing(object):
    """
    处理命令行参数

    根据用户输入的命令行参数设置类属性中的工作模式、日志文件
    列表、区块高度或交易Hash并捕获用户输入的命令行参数的的错误

    Attributes:
        current_mode: 用户设置的工作模式.
        log_file_lis: 日志文件路径的列表.
        height: 用户通过命令行参数传入的区块高度.
        tx_hash: 用户通过命令行参数传入的交易Hash.
    """
    def __init__(self, argv):
        """初始化命令行参数、类属性并解析命令行参数"""
        self.__argv = argv # 设置命令行设置
        self.current_mode = 0 # 模式1:分析单笔交易 模式2:分析所有交易 模式3:分析单个区块 模式4:分析所有区块
        self.log_file_list = [] # 日志文件列表
        self.height = None # 区块高度
        self.tx_hash = None # 交易Hash
        self.__parse_args()  # 解析参数
    
    def __parse_args(self):
        """解析命令行参数并设置工作模式、日志文件列表、交易Hash或区块高度"""
        # 如果不存在命令行参数打印帮助后退出
        if not self.__argv:
            self.__exit(0)
        # 如果日志目录参数不存在打印帮助后退出
        if '-f' not in self.__argv and '--folder' not in self.__argv:
            print('Please set the log folder!')
            self.__exit(-1)
        # 如果使用了-t -b等多个命令行参数打印帮助后退出
        elif len(self.__argv) > 4:
            print('Only one of -t/--transaction and -b/--block can be used!')
            self.__exit(-1)
        # 解析命令行参数
        try:
            opts, args = getopt.getopt(self.__argv, 'hf:b:t:', ['help', 'folder=', 'block=', 'transaction='])
        except getopt.GetoptError as err:
            logging.error('%s', str(err))
            self.__exit(-1)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.__exit(0)
            elif opt in ('-f', '--folder'):
                log_folder_path = arg
                if os.path.exists(log_folder_path):
                    # 将文件夹内文件的.log文件保存到列表
                    self.log_file_list = [x for x in os.listdir(log_folder_path) if x.endswith('.log')]
                    for idx, item in enumerate(self.log_file_list):
                        # 将路径与文件名连接
                        self.log_file_list[idx] = os.path.join(log_folder_path, item)
                else:
                    print('Folder "%s" not found!' %log_folder_path)
                    self.__exit(-1)
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
        if self.current_mode == 0:
            print('Please set tx_hash or block height!')
            self.__exit(-1)
        self.__print_args()

    @staticmethod
    def __exit(exit_code):
        """打印使用帮助并使用传入的错误码退出程序"""
        print("\nUsage: main.py "
            "[-h/--help] "
            "[-f/--folder <relative path>/<absolute path>] "
            "[-t/--transaction <tx_hash>/all] "
            "[-b/--block <block_height>/all] ")
        sys.exit(exit_code)

    def __print_args(self):
        """打印参数信息"""
        print('log file list: %s' %self.log_file_list)
        mode_info = ['', 'Analyze a transaction', 'Analyze all transactions', 'Analyze a block', 'Analyze all blocks']
        print('current mode: %s' %(mode_info[self.current_mode]))
        if self.current_mode == 1:
            print('transaction id: %s\n' %self.tx_hash)
        elif self.current_mode == 3:
            print('block height: %s\n' %self.height)
