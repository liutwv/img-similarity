#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
特征点匹配方法
@File    : feature_match.py
@Time    : 2020/4/16 14:01
@Author  : liutwv
@Software: PyCharm
"""

import cv2
import logging
from req_tool import read_img_from_net


def feature_similarity(img1_url, img2_url, type='o'):
    """
    图片解析为hash值
    Args:
        img1_url: 第一张图片URL地址
        img2_url: 第二张图片URL地址
        type: 算法类型，'o' -> ORB
    Returns:
        {
            "similarity": "xxx"
        }
    """
    img1 = read_img_from_net(img1_url, cv2.IMREAD_GRAYSCALE)
    img2 = read_img_from_net(img2_url, cv2.IMREAD_GRAYSCALE)

    similarity = 0
    if type == 'o':
        similarity = orb_similarity(img1, img2)

    print(similarity)
    return similarity


def orb_similarity(img1, img2):
    """
    ORB算法相似性
    """
    try:
        # 初始化ORB检测器
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        print(type(des1))
        # 获得一个暴力匹配器的对象
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        # knn筛选结果
        matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)

        # 查看最大匹配点数目
        good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
        similarity = len(good) / len(matches)
        return similarity
    except Exception as e:
        logging.info(e)
        return '0'
