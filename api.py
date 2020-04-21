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
import hash_match
import feature_match
import c_hist_match

app = Flask(__name__)


@app.route('/chist', endpoint="chist", methods=['POST'])
def calculate_cindy_hist():
    """
    计算网络图片直方图
    """
    parameters = request.get_json()
    url = parameters['url']

    try:
        data = c_hist_match.get_hist(url)
        logging.info(data)
        return make_response(jsonify(data), 200)
    except Exception as e:
        logging.info(e)
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
        logging.info(data)
        return make_response(jsonify(data), 200)
    except Exception as e:
        logging.info(e)
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
        logging.info(data)
        return make_response(jsonify(data), 200)
    except Exception as e:
        logging.info(e)
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
        logging.info(data)
        return make_response(jsonify(data), 200)

    except Exception as e:
        logging.info(e)
        return make_response({}, 500)


if __name__ == '__main__':
    logging.basicConfig(
        # 日志级别
        level=logging.DEBUG,
        # 日志格式
        # 时间、代码所在文件名、代码行号、日志级别名字、日志信息
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        # 打印日志的时间
        datefmt='%a, %d %b %Y %H:%M:%S',
        # 日志文件存放的目录（目录必须存在）及日志文件名
        filename='/opt/logs/img-similarity.log',
        # 打开日志文件的方式
        filemode='w'
    )

    app.run(host='0.0.0.0', port='5001')
