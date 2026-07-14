#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#######################################################################################################################
#                                              ___  _                                                                 #
#                                             / (_)| | o                                                              #
#                                            |     | |     _   _  _  _|_                                              #
#                                            |     |/  |  |/  / |/ |  |                                               #
#                                             \___/|__/|_/|__/  |  |_/|_/                                             #
#                                                                                                                     #
#                                                                                                                     #
#######################################################################################################################
"""
client.py
-------------------------------------------------------------------
This script was created by Xuanming in 2026, thanks for your reading
Location: Host: /path/to/client.py
Statement: This Python script write some key-value into Redis software, then read them from Redis Software
Usage:
     $ python /path/to/client.py
"""

import redis
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
        client = redis.Redis(host='redis.season.com', port=6379, db=0, password='season_4U',
                             ssl=False, decode_response=True)
    except redis.exceptions.TimeoutError as err:
        Logger.error('Connect Redis service timeout')
        Logger.error(err)
        exit(1)
    client.geoadd(name='China', values=[116.40, 39.90, 'Beijing',
                                        121.47, 31.23, 'Shanghai',
                                        117.20, 39.08, 'Tianjing',
                                        106.55, 29.56, 'Chongqing'])
    for city in client.georadius(name='China', longitude=0, latitude=0, radius=1000000, unit='km',
                              withdist=True, sort='ASC'):
        print('{element}: {score}km'.format(element=city[0], score=city[1]))
