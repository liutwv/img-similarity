#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File    : api.py
@Time    : 2020/4/8 23:08
@Author  : liutwv
@Software: PyCharm
"""
from flask import Flask, request, jsonify, make_response
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import settings
import hash_match
import feature_match
import c_hist_match

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/chist', endpoint="chist", methods=['POST'])
def calculate_cindy_hist():
    """
    计算网络图片直方图
    """
    parameters = request.get_json()
    url = parameters['url']

    try:
        data = c_hist_match.get_hist(url)
        logger.info(data)
        return make_response(jsonify(data), 200)
    except Exception as e:
        logger.info(e)
        return make_response({}, 500)


@app.route('/hash', endpoint="hash", methods=['POST'])
def calculate_img_phash():
    """
    计算网络图片hash值
    """
    parameters = request.get_json()
    url = parameters['url']
    hs = parameters['hs']

    try:
        data = hash_match.img_to_hashes(url, 'p' in hs, 'd' in hs, 'a' in hs)
        logger.info(data)
        return make_response(jsonify(data), 200)
    except Exception as e:
        logger.info(e)
        return make_response({}, 500)


@app.route('/hm_distance', endpoint="hm_distance", methods=['POST'])
def calculate_hamming_distance():
    """
    计算两张网络图片之间的汉明距离
    """
    parameters = request.get_json()
    url1 = parameters['url1']
    url2 = parameters['url2']
    hs = parameters['hs']

    try:
        data = hash_match.calculate_hamming_distance_btw_imgs(url1, url2, 'p' in hs, 'd' in hs, 'a' in hs)
        logger.info(data)
        return make_response(jsonify(data), 200)
    except Exception as e:
        logger.info(e)
        return make_response({}, 500)


@app.route('/feature_sim', endpoint="feature_sim", methods=['POST'])
def calculate_feature_similarity():
    """
    根据特征匹配算法计算两张网络图片之间的相似度
    """
    parameters = request.get_json()
    url1 = parameters['url1']
    url2 = parameters['url2']
    type = parameters['type']

    try:
        data = feature_match.feature_similarity(url1, url2, type)
        logger.info(data)
        return make_response(jsonify(data), 200)
    except Exception as e:
        logger.info(e)
        return make_response({}, 500)


def register_log():
    """
    配置日志
    :return:
    """
    info_log = settings.RUN_LOG_FILE
    err_log = settings.ERROR_LOG_FILE

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handler = TimedRotatingFileHandler(info_log, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    handler.setLevel(logging.INFO)
    err_handler = TimedRotatingFileHandler(err_log, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    err_handler.setLevel(logging.ERROR)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    logging.basicConfig(
        format=fmt,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[handler, err_handler, console]
    )
    logging.getLogger(__name__).setLevel(logging.INFO)


if __name__ == '__main__':
    register_log()

    app.run(host='0.0.0.0', port='5001')
