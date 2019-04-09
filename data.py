# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用于获取日志文件中字典格式的数据的线程实现类

在主线程中开启与日志文件数量相同的子线程用于生成字
典格式的数据并将数据存在全局的列表中，以在其中一个
日志处理线程产生IO等待时调度到另一个日志处理线程执
行用CPU时间的数据字典生成方法，节约数据的获取时间。
"""

from threading import Thread

from log import LogProcessing


class DataThread(Thread):
    """获取日志文件中字典格式的数据的Thread线程实现类

    Attributes:
        log_dict_list: 使用列表嵌套字典存储的所有交易或区块的的字典格式的数据，在所有线程中共享
    """

    def __init__(self, log_file, log_dict_list, analysis_type):
        super().__init__()
        self.__log_file = log_file  # 日志文件路径
        self.log_dict_list = log_dict_list  # 列表当作参数传递给线程会当作全局变量
        self.__type = analysis_type  # 要生成的数据类型:transaction或block
        self.__log_dict = dict()
        self.__log = LogProcessing(self.__log_file)  # 实例化日志处理类

    def run(self):
        """线程运行方法"""
        if self.__type == 'transaction':
            self.__create_transaction_dict()
        elif self.__type == 'block':
            self.__create__block_dict()
        # append操作为线程安全方法无需互斥锁
        self.log_dict_list.append(self.__log_dict)

    def __create_transaction_dict(self):
        """生成交易字典"""
        self.__log.generate_transaction_dictionary()
        self.__log_dict = self.__log.transaction_dict

    def __create__block_dict(self):
        """生成区块字典"""
        self.__log.generate_block_dictionary()
        self.__log_dict = self.__log.block_dict
