#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re

from util import logtime_to_millisecondtimestamp


class LogProcessing:
    def __init__(self, log_path):
        self.__log_path = log_path
        self.transaction_log_list = []
        self.block_log_list = []
        self.__execution_clean_log()

    def __clean_divided_log(self, divided_log):
        # 在list中删除单条日志中msg和type
        del(divided_log[4])
        del(divided_log[1])
        # 将日志中的时间格式转换为毫秒级的时间戳
        # divided_log[0] = logtime_to_millisecondtimestamp(divided_log[0])
        # 交换列表元素位置
        # divided_log[0], divided_log[1] = divided_log[1], divided_log[0]
        return divided_log
    
    def __execution_clean_log(self):
        with open(self.__log_path, 'r') as f:
            # 将日志文件以行为单位拆分并放入list
            log_list = f.readlines()
        for i in range(0, len(log_list)):
            # 使用正则表达式匹配双引号中的内容并存为list
            # 格式为:['Mar 17 00:00:00.486', 'receive message from peer', '{height: 197197}', '115.54.192.9:52618', '*netsync.GetBlockMessage']
            divided_log = re.findall(r'\"([^\"]*)\"', log_list[i])
            # 日志类型
            log_type = divided_log[-1]
            if log_type == '*netsync.TransactionMessage':
                # 截取交易message中的交易id
                divided_log[2] = divided_log[2][-65:-1]
                divided_log = self.__clean_divided_log(divided_log)
                self.transaction_log_list.append(divided_log)
            elif log_type == '*netsync.MineBlockMessage':
                # 截取区块message中的区块高度
                divided_log[2] = int(divided_log[2][15:-79])
                divided_log = self.__clean_divided_log(divided_log)
                self.block_log_list.append(divided_log)

    def generate_transaction_dictionary(self):
        # 取transaction_log_list中的第二列即交易id 包含重复元素
        all_tx_hash = list(zip(*self.transaction_log_list))[1]
        # 从all_tx_hash元组中创建字典 key为交易id 同时去处重复元素
        transaction_dict = dict().fromkeys(all_tx_hash, [])
        print(transaction_dict)

    def generate_block_dictionary(self):
        # 取block_log_list中的第二列即区块高度 包含重复元素
        all_block_height = list(zip(*self.block_log_list))[1]
        # 从all_block_height元组中创建字典 key为区块高度 同时去处重复元素
        block_dict = dict().fromkeys(all_block_height, [])
        print(block_dict)

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    log_file = 'log_data/bytomd_20190304183016.log'
    log = LogProcessing(log_file)
    log.generate_transaction_dictionary()
    log.generate_block_dictionary()
    # print(log.block_log_list)
    # print(log.transaction_log_list)
    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
    print((endtime - starttime).microseconds)