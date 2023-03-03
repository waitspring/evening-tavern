#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#######################################################################################################################
#                                     , __                                                                            #
#                                    /|/  \              |                                                            #
#                                     |___/ ,_    __   __|          __   _   ,_                                       #
#                                     |    /  |  /  \_/  |  |   |  /    |/  /  |                                      #
#                                     |       |_/\__/ \_/|_/ \_/|_/\___/|__/   |_/                                    #
#                                                                                                                     #
#                                                                                                                     #
#######################################################################################################################
"""
producer.py
-------------------------------------------------------------------
This script was created by Xuanming in 2023, thanks for your reading
Location: Host: /path/to/producer.py
Statement: This Python script send some message to Kafka software, for helping us observe Kafka software feature
Usage:
     $ python /path/to/producer.py
"""


import datetime
import json
import kafka
import logging
import os
import random
import string
import sys
import time


# =====================================================================================================================
# Common Class
# =====================================================================================================================
class Logger(object):
    """
    提供标准的日志输出工具, 日志输出格式为 2022-02-22 22:22:22.222 INFO [xxxxxx] This is demo output.
    默认的:
        * DEBUG 及其以上级别的日志都是有效输出
        * INFO  及其以上级别的日志输出到日志文件
        * ERROR 及其以上级别的日志输出到终端
    """
    output = logging.getLogger('foo')
    output.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)s [%(name)s] %(message)s', 
                                  datefmt='%Y-%m-%d %H:%M:%S')
    logfile = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'log', 'foo.log')
    if not os.path.isdir(os.path.dirname(logfile)):
        os.makedirs(os.path.dirname(logfile))
    _x = logging.FileHandler(filename=logfile, mode='a', encoding='UTF-8')
    _x.setLevel(logging.INFO)
    _x.setFormatter(formatter)
    _y = logging.StreamHandler()
    _y.setLevel(logging.ERROR)
    _y.setFormatter(formatter)
    output.addHandler(_x)
    output.addHandler(_y)

    @staticmethod
    def debug(message=str):
        Logger.output.debug(message)

    @staticmethod
    def info(message=str):
        Logger.output.info(message)

    @staticmethod
    def error(message=str):
        Logger.output.error(message)

class RaisePoint(Exception):
    """
    提供多层嵌套循环的循环跳出工具
    """
    def __str__(self):
        return 'Function: ' + self.__class__.__name__ + '() Exception: ' + 'Escape from multiple nested loop'


# =====================================================================================================================
# Common Function
# =====================================================================================================================
def except_return_none(func):
    """
    捕获未知错误的装饰器
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            Logger.error('Function: ' + func.__name__ + '() Exception: ' + str(error))
            return None
    return wrapper

@except_return_none
def gbk_to_utf8(func):
    """
    转换 GBK 字符编码到 UTF-8 字符编码的装饰器
    """
    def wrapper(*args, **kwargs):
        meta = func(*args, **kwargs)
        for k, v in meta.items():
            if v is not None and type(v) is str and 'UTF' not in sys.stdin.encoding.upper():
                meta[k] = v.decode('GBK').encode('UTF-8')
        return meta
    return wrapper

@except_return_none
def time_pay(func):
    """
    捕获方法的执行用时
    """
    def wrapper(*args, **kwargs):
        timepoint_begin = time.time()
        result = func(*args, **kwargs)
        timepoint_end = time.time()
        timepoint_pay = round(timepoint_end - timepoint_begin, 3)
        Logger.debug('Function: ' + func.__name__ + '() execute time pay ' + str(timepoint_pay))
        return result
    return wrapper



# =====================================================================================================================
# Main Part
# =====================================================================================================================
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    try:
        foo = kafka.KafkaProducer(
            bootstrap_servers='kafka-0.season.com:9092,kafka-1.season.com:9092,kafka-2.season.com:9092')
    except kafka.errors.NoBrokersAvailable as err:
        Logger.error('Connect Kafka service failure')
        Logger.error(err)
        exit(1)
    for i in range(1000):
        data = {
            'index': i,
            'timestamp': datetime.datetime.today().strftime('%F %T.%f')[:-3],
            'foo': ''.join(random.choice(string.ascii_lowercase) for x in range(10))
        }
        try:
            foo.send(topic='foo', value=json.dumps(data).encode())
        except AssertionError as err:
            Logger.error('Send message \'%s\' into Kafka service failure' % data['foo'])
            Logger.error(err)
            continue



