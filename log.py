#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
import sys
import time


from datetime import datetime


class LogProcessing(object):
    """日志处理类

    将单个日志文件中的交易日志和区块日志存为[时间, 交易id/区块高度, 节点ip:端口]
    构成的嵌套列表，并可通过generate_transaction_dictionary或
    generate_block_dictionary类方法生成交易id或区块高度为key，
    存在嵌套列表中的时间和节点ip:端口为value的字典以方便分析数据。

    Attributes:
        all_tx_hash: 记录所有的交易id.
        all_block_height: 记录所有的区块高度.
        transaction_dict: 字典格式的交易日志.
        block_dict: 字典格式的交易日志.
    """
    def __init__(self, log_path):
        """初始化类属性并执行日志清洗"""
        self.__log_path = log_path # 日志文件路径
        self.__transaction_log_list = [] # 清洗后的交易日志列表 [['时间', '交易id', '节点ip:端口']]
        self.__block_log_list = [] # 清洗后的交易日志列表 [['时间', '区块高度', '节点ip:端口']]
        self.all_tx_hash = [] # 所有的交易id
        self.all_block_height = [] # 所有的区块高度
        self.transaction_dict = None # 字典格式的交易信息 {'交易id': [['时间','节点ip:端口']]}
        self.block_dict = None # 字典格式的区块信息 {'区块高度': [['时间','节点ip:端口']]}
        self.__execution_clean_log() # 执行日志清洗
    
    def __execution_clean_log(self):
        """执行日志清洗 将日志中的有用数据存为列表"""
        try:
            with open(self.__log_path, 'r') as f:
                # 将日志文件以行为单位拆分并放入列表
                log_list = f.readlines()
        except IOError as err:
            logging.error('%s', str(err))
            print('Log file "%s" is not accessible!' %self.__log_path)
            sys.exit(-1)
        for i in range(0, len(log_list)):
            # 使用正则表达式匹配双引号中的内容并存为列表
            # 格式为:['Mar 17 00:00:00.486', 'receive message from peer', '{height: 197197}', '115.54.192.9:52618', '*netsync.GetBlockMessage']
            divided_log = re.findall(r'\"([^\"]*)\"', log_list[i])
            # 日志类型
            log_type = divided_log[-1]
            if log_type == '*netsync.TransactionMessage':
                # 截取交易message中的交易id
                divided_log[2] = divided_log[2][-65:-1]
                # 删除列表中的type属性
                del(divided_log[-1])
                # 删除列表中的msg属性
                del(divided_log[1])
                self.__transaction_log_list.append(divided_log)
            elif log_type == '*netsync.MineBlockMessage':
                # 截取区块message中的区块高度
                divided_log[2] = int(divided_log[2][15:-79])
                del(divided_log[-1])
                del(divided_log[1])
                self.__block_log_list.append(divided_log)

    def generate_transaction_dictionary(self):
        """生产字典格式的交易数据"""
        # 取transaction_log_list中的第二列即交易id 包含重复元素
        self.all_tx_hash = list(zip(*self.__transaction_log_list))[1]
        # 从all_tx_hash元组中创建字典 key为交易id 同时去处重复元素
        self.transaction_dict = dict().fromkeys(self.all_tx_hash, [])
        self.all_tx_hash = self.transaction_dict.keys()
        for i in range(0, len(self.__transaction_log_list)):
            # 设置交易字典的key为交易id
            transaction_dict_key = self.__transaction_log_list[i][1]
            # 设置交易字典的value为['时间', '节点ip:端口']
            transaction_dict_value = [self.__transaction_log_list[i][0], self.__transaction_log_list[i][2]]
            # 构建字典
            self.transaction_dict[transaction_dict_key].append(transaction_dict_value)

    def generate_block_dictionary(self):
        """生产字典格式的区块数据"""
        self.all_block_height = list(zip(*self.__block_log_list))[1]
        self.block_dict = dict().fromkeys(self.all_block_height, [])
        self.all_block_height = self.block_dict.keys()
        for i in range(0, len(self.__block_log_list)):
            # 设置区块字典的key为区块高度
            block_dict_key = self.__block_log_list[i][1]
            block_dict_value = [self.__block_log_list[i][0], self.__block_log_list[i][2]]
            self.block_dict[block_dict_key].append(block_dict_value)
    
    @staticmethod
    def logtime_to_millisecondtimestamp(log_time):
        """将日志中的日期格式转换为毫秒级的时间戳

        Args:
            log_time: bytomd日志中的时间格式如：Mar 17 00:00:56.009

        Returns:
            返回当前年份加上日志中时间的毫秒级的时间戳，如：1552752056009
        """
        year_str = str(datetime.now().year)
        # 将年份与日志中的时间拼接
        time_str = '%s %s' %(year_str, log_time)
        # 将时间字符串转为格式化的时间
        d = datetime.strptime(time_str, "%Y %b %d %H:%M:%S.%f")
        # 记录3位的毫秒时间
        millisecond = int(d.microsecond / 1000)
        # 生成秒级时间戳
        timestamp = int(time.mktime(d.timetuple()))
        # 生成毫秒级时间戳
        millisecondtimestamp = timestamp * 1000 + millisecond
        return millisecondtimestamp