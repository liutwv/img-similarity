#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
直方图值比较
参考：
    https://segmentfault.com/a/1190000018849195
    http://www.ruanyifeng.com/blog/2013/03/similar_image_search_part_ii.html
@File    : hist_match.py.py
@Time    : 2020/4/17 17:55
@Author  : liutwv
@Software: PyCharm
"""

import cv2
from math import sqrt
import logging
from req_tool import read_img_from_net


def get_hist(img_url):
    """
    计算网络图片直方图数值
    Args:
        url: 图片URL地址
    Returns:
        dict类型直方图数值，转为json格式字符串返回
    """
    img = read_img_from_net(img_url)
    return calc_bgr_hist(img)


def calc_bgr_hist(img):
    """
    颜色直方图的数值计算
    Args:
        img: numpy.ndarray格式图片
    Returns:
        dict类型直方图数值
    """
    hist = {}
    try:
        if not img.size:
            return False

        # 缩放尺寸减小计算量
        image = cv2.resize(img, (32, 32))

        for bgr_list in image:  # 循环32次
            for bgr in bgr_list:  # 再循环32次，最后得到bgr为一个像素点
                # 颜色按照顺序映射，得到8进制的3个值
                maped_b = bgr_mapping(bgr[0])
                maped_g = bgr_mapping(bgr[1])
                maped_r = bgr_mapping(bgr[2])
                # 计算像素值，给三个元素不同的权重，分别为 8 * 8，8，1
                index = maped_b * 8 * 8 + maped_g * 8 + maped_r
                hist[index] = hist.get(index, 0) + 1
    except Exception as e:
        logging.info(e)

    return hist


def compare_similar_hist(h1, h2):
    """
    计算两张图片的相似度
    """
    if not h1 or not h2:
        return False
    sum1, sum2, sum_mixd = 0, 0, 0

    try:
        # 因为两个dict的key不一定相同，而像素值key的最大数不超过512，直接循环到512，遍历取出每个像素值
        for i in range(512):
            # 计算出现相同像素值次数的平方和
            v1i = h1.get(i, 0)
            v2i = h2.get(i, 0)
            sum1 = sum1 + (v1i * v1i)
            sum2 = sum2 + (v2i * v2i)
            # 计算两个图片次数乘积的和
            sum_mixd = sum_mixd + (v1i * v2i)

        # 按照余弦相似性定理计算相似度
        similarity = sum_mixd / (sqrt(sum1) * sqrt(sum2))
    except Exception as e:
        logging.info(e)

    return similarity


def compare_similarity_hist_with_net_imgs(img1_url, img2_url):
    """
    比较两张网络图片的相似度
    """
    h1 = calc_bgr_hist(read_img_from_net(img1_url))
    h2 = calc_bgr_hist(read_img_from_net(img2_url))
    return compare_similar_hist(h1, h2)


def bgr_mapping(img_val):
    """
    颜色映射
    将bgr颜色分成8个区间做映射
    """
    if 0 <= img_val <= 31:
        return 0
    if 32 <= img_val <= 63:
        return 1
    if 64 <= img_val <= 95:
        return 2
    if 96 <= img_val <= 127:
        return 3
    if 128 <= img_val <= 159:
        return 4
    if 160 <= img_val <= 191:
        return 5
    if 192 <= img_val <= 223:
        return 6
    if img_val >= 224:
        return 7
