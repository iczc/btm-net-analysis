#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re

from util import logtime_to_millisecondtimestamp


def clean_divided_log(divided_log, type):
    """清洗列表格式的单条日志

    删除传入列表中的的msg、type等无用信息并把日志
    中的时间格式转换为毫秒级的时间戳以便比较。

    Args:
        divided_log:使用正则分割后的列表格式的单条日志。
        type:日志类型，1为交易消息，2为区块消息

    Returns:
        清洗后的列表格式的单条日志, 
        交易消息为[毫秒级时间戳, 交易id, 节点ip和端口]
        区块消息为[毫秒级时间戳, 区块高度, 节点ip和端口]
    """
    # 在list中删除单条日志中msg和type
    del(divided_log[4])
    del(divided_log[1])
    # 将日志中的时间格式转换为毫秒级的时间戳
    divided_log[0] = logtime_to_millisecondtimestamp(divided_log[0])
    if type == 1:
        # 截取交易message中的交易id
        divided_log[1] = divided_log[1][-65:-1]
    elif type == 2:
        # 截取区块message中的区块高度
        divided_log[1] = int(divided_log[1][15:-79])
    return divided_log

def process_log(log_path):
    transaction_log_list = []
    block_log_list = []
    with open(log_file,'r') as f:
        # 将日志文件以行为单位拆分并放入list
        log_list = f.readlines()
    for i in range(0, len(log_list)):
        # 使用正则表达式匹配双引号中的内容并存为list
        # 格式为:['Mar 17 00:00:00.486', 'receive message from peer', '{height: 197197}', '115.54.192.9:52618', '*netsync.GetBlockMessage']
        divided_log = re.findall(r'\"([^\"]*)\"', log_list[i])
        # 日志类型
        log_type = divided_log[4]
        if log_type == '*netsync.TransactionMessage':
            divided_log = clean_divided_log(divided_log, 1)
            transaction_log_list.append(divided_log)
        elif log_type == '*netsync.MineBlockMessage':
            divided_log = clean_divided_log(divided_log, 2)
            block_log_list.append(divided_log)
    return transaction_log_list, block_log_list

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    log_file = 'log_data/bytomd_20190304183016.log'
    transaction_log_list, block_log_list = process_log(log_file)
    # print(transaction_log_list)
    # print(block_log_list)
    endtime = datetime.datetime.now()
    print((endtime - starttime).microseconds)