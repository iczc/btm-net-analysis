#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import LogProcessing
from util import logtime_to_millisecondtimestamp


class BlockAnalysis:
    def __init__(self, log_file):
        self.__log_info = LogProcessing(log_file)
        self.__log_info.generate_block_dictionary()
        self.earliest_time = ''
        self.latest_time = ''
    
    def analyze_block(self, height):
        # block字典中是否有区块高度的key
        if height in self.__log_info.block_dict:
            blcok_info_list = self.__log_info.block_dict[height]
            # 根据转为为毫秒时间戳的时间为key排序
            blcok_info_list.sort(key=lambda msg: logtime_to_millisecondtimestamp(msg[0]))
            self.earliest_time = blcok_info_list[0]
            self.latest_time = blcok_info_list[-1]
            return True
        else:
            return False