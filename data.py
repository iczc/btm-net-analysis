#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread

from log import LogProcessing


class DataThread(Thread):
    def __init__(self, log_file, log_dict_list, type):
        super().__init__()
        self.__log_file = log_file
        # 列表当作参数传递给线程会当作全局变量
        self.log_dict_list = log_dict_list
        self.__type = type
        self.__log_dict = dict()
        self.__log = LogProcessing(self.__log_file)

    def run(self):
        if self.__type == 'transaction':
            self.__create_transaction_dict()
        elif self.__type == 'block':
            self.__create__block_dict()
        # append为线程安全方法无需互斥锁
        self.log_dict_list.append(self.__log_dict)

    def __create_transaction_dict(self):
        self.__log.generate_transaction_dictionary()
        self.__log_dict = self.__log.transaction_dict
    
    def __create__block_dict(self):
        self.__log.generate_block_dictionary()
        self.__log_dict = self.__log.block_dict
