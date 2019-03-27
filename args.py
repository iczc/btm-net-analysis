#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import logging
import sys


class ProcessArgs:
    def __init__(self, argv):
        self.__argv = argv # 设置命令行设置
        self.__parse_args()  # 解析参数
    
    def __parse_args(self):
        try:
            opts, args = getopt.getopt(self.__argv, 'hb:t:', ['help', 'block=', 'transaction='])
        except getopt.GetoptError as err:
            logging.error('%s', str(err))
            self.__exit(-1)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.__exit(0)
            elif opt in ('-b', '--block'):
                print('block')
            elif opt in ('-t', '--transaction'):
                print('transaction')
            else:
                logging.error('unhandled option')
                self.__exit(-1)
        self.__print_args()

    @staticmethod
    def __exit(exit_code):
        print("\nUsage: main.py "
            "[-h/--help] "
            "[-b/--block <block_height>/all] "
            "[-t/--transaction <tx_hash>/all]")
        sys.exit(exit_code)

    def __print_args(self):
        pass
