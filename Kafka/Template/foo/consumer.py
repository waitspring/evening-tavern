#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#######################################################################################################################
#                                   ___                                                                               #
#                                  / (_)                                                                              #
#                                 |      __   _  _    ,          _  _  _    _   ,_                                    #
#                                 |     /  \_/ |/ |  / \_|   |  / |/ |/ |  |/  /  |                                   #
#                                  \___/\__/   |  |_/ \/  \_/|_/  |  |  |_/|__/   |_/                                 #
#                                                                                                                     #
#                                                                                                                     #
#######################################################################################################################
"""
consumer.py
-------------------------------------------------------------------
This script was created by Xuanming in 2023, thanks for your reading
Location: Host: /path/to/consumer.py
Statement: This Python script read some message to Kafka software, for helping us observe Kafka software feature
Usage:
     $ python /path/to/consumer.py
"""


import kafka
import logging
import os
import random
import sys


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



# =====================================================================================================================
# Main Part
# =====================================================================================================================
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    try:
        foo = kafka.KafkaConsumer(
            bootstrap_servers='kafka-0.season.com:9092,kafka-1.season.com:9092,kafka-2.season.com:9092',
            group_id='foo')
    except kafka.errors.NoBrokersAvailable as err:
        Logger.error('Connect Kafka service failure')
        Logger.error(err)
        exit(1)
    foo.subscribe(topics=('foo'))
    for message in foo:
        print('--------------------------------------------------')
        print(message.topic)
        print(message.partition)
        print(message.offset)
        print(message.key)
        print(message.value)
