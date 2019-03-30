#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import LogProcessing
from util import logtime_to_millisecondtimestamp


class TransactionAnalysis:
    def __init__(self, log_file):
        self.__log_info = LogProcessing(log_file)
        self.__log_info.generate_transaction_dictionary()
        self.earliest_msg = ''
        self.latest_msg = ''
    
    def analyze_transaction(self, tx_hash):
        # block字典中是否有区块高度的key
        if tx_hash in self.__log_info.transaction_dict:
            transaction_info_list = self.__log_info.transaction_dict[tx_hash]
            # 根据转为为毫秒时间戳的时间为key排序
            transaction_info_list.sort(key=lambda msg: logtime_to_millisecondtimestamp(msg[0]))
            self.earliest_msg = transaction_info_list[0]
            self.latest_msg = transaction_info_list[-1]
            return True
        else:
            return False
    