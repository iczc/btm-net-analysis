#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta

from log import LogProcessing


class Analysis:
    def __init__(self, log_file):
        self.__log_info = LogProcessing(log_file)
        self.earliest_msg = ''
        self.latest_msg = ''
    
    def find_earliest_latest_msg(self, parameter, type):
        if type == 'transaction':
            tx_hash = parameter
            self.__log_info.generate_transaction_dictionary()
            # 判断transaction字典中是否有交易id的key
            if tx_hash in self.__log_info.transaction_dict:
                transaction_info_list = self.__log_info.transaction_dict[tx_hash]
                # 根据转为为毫秒时间戳的时间为key排序
                transaction_info_list.sort(key=lambda msg: self.__log_info.logtime_to_millisecondtimestamp(msg[0]))
                self.earliest_msg = transaction_info_list[0]
                self.latest_msg = transaction_info_list[-1]
                return True
        elif type == 'block':
            height = parameter
            self.__log_info.generate_block_dictionary()
            # block字典中是否有区块高度的key
            if height in self.__log_info.block_dict:
                blcok_info_list = self.__log_info.block_dict[height]
                # 根据转为为毫秒时间戳的时间为key排序
                blcok_info_list.sort(key=lambda msg: self.__log_info.logtime_to_millisecondtimestamp(msg[0]))
                self.earliest_msg = blcok_info_list[0]
                self.latest_msg = blcok_info_list[-1]
                return True
        # 如果type错误或者未找到区块高度或交易id返回false
        return False

    @staticmethod
    def calc_time_interval(earliest_time, latest_time):
        latest_time = LogProcessing.logtime_to_millisecondtimestamp(latest_time)
        earliest_time = LogProcessing.logtime_to_millisecondtimestamp(earliest_time)
        millisecond_interval = abs(latest_time - earliest_time)
        second_interval = int(millisecond_interval / 1000)
        millisecond = str(millisecond_interval)[-3:]
        time_interval = '%s.%s' %(timedelta(seconds=second_interval), millisecond)
        return time_interval