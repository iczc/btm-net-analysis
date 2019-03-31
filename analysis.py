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
        self.__log_info = LogProcessing(self.__log_file)
    
    def run(self):
        self.find_earliest_latest_msg()
        # 判断所有的最早的消息列表和最晚的消息列表不为空
        if self.earliest_msg and self.latest_msg:
            print('The earliest msg and latest msg in %s:' %self.__log_file)
            print(self.earliest_msg)
            print(self.latest_msg)
    
    def find_earliest_latest_msg(self):
        """查找区块或交易中的最早和最晚的消息，根据type
        参数的不同，parameter分别为交易id或区块高度"""
        if self.__type == 'transaction':
            tx_hash = self.__parameter
            self.__log_info.generate_transaction_dictionary()
            # 判断transaction字典中是否有交易id的key
            if tx_hash in self.__log_info.transaction_dict:
                transaction_info_list = self.__log_info.transaction_dict[tx_hash]
                # 根据转为为毫秒时间戳的时间为key排序
                transaction_info_list.sort(key=lambda msg: self.__log_info.logtime_to_millisecondtimestamp(msg[0]))
                self.earliest_msg = transaction_info_list[0]
                self.latest_msg = transaction_info_list[-1]
            else:
                print('The transaction %s was not found in %s' %(tx_hash, self.__log_file))
        elif self.__type == 'block':
            height = self.__parameter
            self.__log_info.generate_block_dictionary()
            # block字典中是否有区块高度的key
            if height in self.__log_info.block_dict:
                blcok_info_list = self.__log_info.block_dict[height]
                # 根据转为为毫秒时间戳的时间为key排序
                blcok_info_list.sort(key=lambda msg: self.__log_info.logtime_to_millisecondtimestamp(msg[0]))
                self.earliest_msg = blcok_info_list[0]
                self.latest_msg = blcok_info_list[-1]
            else:
                print('The height %s was not found in %s' %(height, self.__log_file))
