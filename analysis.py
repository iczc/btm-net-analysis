#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

from log import LogProcessing


class AnalysisThread(threading.Thread):
    def __init__(self, queue, log_file, parameter, type):
        super().__init__()
        self.__queue = queue
        # self.__log_dict = log_dict
        self.__log_dict = dict()
        self.__log_file = log_file
        self.__parameter = parameter
        self.__type = type
        self.earliest_msg = []
        self.latest_msg = []
    
    def run(self):
        if not self.__log_dict:
            self.__get_log_dictionary()
        self.__get_both_ends_msg()
        # 判断所有的最早的消息列表和最晚的消息列表不为空
        if self.earliest_msg and self.latest_msg:
            self.__queue.put(self.earliest_msg)
            self.__queue.put(self.latest_msg)

    def __get_log_dictionary(self):
        """调用日志处理类生成字典格式的交易区块日志数据"""
        self.__log_info = LogProcessing(self.__log_file)
        if self.__type == 'transaction':
            self.__log_info.generate_transaction_dictionary()
            self.__log_dict = self.__log_info.transaction_dict
        elif self.__type == 'block':
            self.__log_info.generate_block_dictionary()
            self.__log_dict = self.__log_info.block_dict

    def __get_both_ends_msg(self):
        """获取区块或交易在日志中最早和最迟的数据"""
        # 判断数据字典中是否有交易id或区块高度的key
        if self.__parameter in self.__log_dict:
            data_list = self.__log_dict[self.__parameter]
            self.earliest_msg = data_list[0]
            self.latest_msg = data_list[-1]
