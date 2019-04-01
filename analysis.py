#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

from queue import Queue

from log import LogProcessing


class Analysis(threading.Thread):
    def __init__(self, log_file, parameter, type):
        super(Analysis, self).__init__()
        self.__log_file = log_file
        self.__parameter = parameter
        self.__type = type
        self.earliest_msg = ''
        self.latest_msg = ''
    
    def run(self):
        self.__log_info = LogProcessing(self.__log_file)
        if self.__type == 'transaction':
            self.__analyze_single_transaction()
        elif self.__type == 'block':
            self.__analyze_single_transaction()
        # 判断所有的最早的消息列表和最晚的消息列表不为空
        if self.earliest_msg and self.latest_msg:
            print('The earliest msg and latest msg in %s:' %self.__log_file)
            print(self.earliest_msg)
            print(self.latest_msg)
        
    def __analyze_single_transaction(self):
        tx_hash = self.__parameter
        self.__log_info.generate_transaction_dictionary()
        # 判断transaction字典中是否有交易id的key
        if tx_hash in self.__log_info.transaction_dict:
            transaction_info_list = self.__log_info.transaction_dict[tx_hash]
            # 日志文件时间即为有序无需排序 根据转为为毫秒时间戳的时间为key排序
            # transaction_info_list.sort(key=lambda msg: LogProcessing.logtime_to_millisecondtimestamp(msg[0]))
            self.earliest_msg = transaction_info_list[0]
            self.latest_msg = transaction_info_list[-1]
        else:
            print('The transaction %s was not found in %s' %(tx_hash, self.__log_file))
        
    def __analyze_single_block(self):
        height = self.__parameter
        self.__log_info.generate_block_dictionary()
        # block字典中是否有区块高度的key
        if height in self.__log_info.block_dict:
            blcok_info_list = self.__log_info.block_dict[height]
            # 根据转为为毫秒时间戳的时间为key排序
            # blcok_info_list.sort(key=lambda msg: LogProcessing.logtime_to_millisecondtimestamp(msg[0]))
            self.earliest_msg = blcok_info_list[0]
            self.latest_msg = blcok_info_list[-1]
        else:
            print('The height %s was not found in %s' %(height, self.__log_file))
    
    def find_earliest_latest_msg(self, compared_list):
        pass