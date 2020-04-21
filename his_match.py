#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
直方图值比较
@File    : his_match.py
@Time    : 2020/4/17 20:53
@Author  : liutwv
@Software: PyCharm
"""

import cv2
from req_tool import read_img_from_net
import logging


def single_sim(img1_url, img2_url):
    return calculate(read_img_from_net(img1_url), read_img_from_net(img2_url))

def three_sim(img1_url, img2_url):
    return classify_hist_with_split(read_img_from_net(img1_url), read_img_from_net(img2_url))


def calculate(image1, image2):
    """
    灰度直方图算法
    计算单通道的直方图的相似值
    """
    degree = 0
    try:
        # 计算直方图数值
        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])

        # 计算直方图的重合度
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + \
                         (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
    except Exception as e:
        logging.info(e)
    return degree


def classify_hist_with_split(image1, image2, size=(256, 256)):
    """
    RGB每个通道的直方图相似度
    """
    hist = 0
    try:
        # 将图像resize
        image1 = cv2.resize(image1, size)
        image2 = cv2.resize(image2, size)
        # 分离为RGB三个通道，再计算每个通道的相似值
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += calculate(im1, im2)
        hist = sub_data / 3
    except Exception as e:
        logging.info(e)
    return hist
