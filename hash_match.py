#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
hash值比较
@File    : hash_match.py
@Time    : 2020/4/8 23:08
@Author  : liutwv
@Software: PyCharm
"""

import cv2
import numpy as np
from skimage import transform, img_as_ubyte
import logging
from req_tool import read_img_from_net


def img_to_hashes(url, p=False, d=False, a=False, w=False):
    """
    图片解析为hash值
    Args:
        url: 图片URL地址
        p: 是否计算pHash值
        d: 是否计算dHash值
        a: 是否计算aHash值
    Returns:
        {
            "phash": "xxx",
            "dhash": "xxx",
            "ahash": "xxx",
            "whash": "xxx"
        }
    """
    data = {}

    netImg = read_img_from_net(url)

    try:
        # 分表选择90°、180°、270°
        netImgX = img_as_ubyte(transform.rotate(netImg, 90, resize=True))
        netImgY = img_as_ubyte(transform.rotate(netImg, 180, resize=True))
        netImgZ = img_as_ubyte(transform.rotate(netImg, 270, resize=True))
        # 水平翻转
        h_flip = cv2.flip(netImg, 1)
        # 垂直翻转
        v_flip = cv2.flip(netImg, 0)

        if p:
            data['p'] = {}
            data['p']['o'] = pHash(netImg)
            data['p']['x'] = pHash(netImgX)
            data['p']['y'] = pHash(netImgY)
            data['p']['z'] = pHash(netImgZ)
            data['p']['h'] = pHash(h_flip)
            data['p']['v'] = pHash(v_flip)
        if d:
            data['d'] = {}
            data['d']['o'] = dHash(netImg)
            data['d']['x'] = dHash(netImgX)
            data['d']['y'] = dHash(netImgY)
            data['d']['z'] = dHash(netImgZ)
            data['d']['h'] = pHash(h_flip)
            data['d']['v'] = pHash(v_flip)
        if a:
            data['a'] = {}
            data['a']['o'] = aHash(netImg)
            data['a']['x'] = aHash(netImgX)
            data['a']['y'] = aHash(netImgY)
            data['a']['z'] = aHash(netImgZ)
            data['a']['h'] = pHash(h_flip)
            data['a']['v'] = pHash(v_flip)
        if w:
            data['w'] = {}
            data['w']['0'] = wHash(netImg)
            data['w']['x'] = wHash(netImgX)
            data['w']['y'] = wHash(netImgY)
            data['w']['z'] = wHash(netImgZ)
            data['w']['h'] = pHash(h_flip)
            data['w']['v'] = pHash(v_flip)
    except Exception as e:
        logging.info(e)

    return data


def get_channel_count(img):
    """
    判断图片通道数
    """
    if img.ndim == 2:  # 2维度表示长宽
        channels = 1  # 单通道(grayscale)
    elif img.ndim == 3:
        channels = 3
    else:  # 异常维度，不是图片了
        channels = -1
    return channels


def pre_handle_img(img, leng, wid):
    """
    图片预处理
    """
    # 缩小图片
    img = cv2.resize(img, (leng, wid))
    # 转换为灰度图
    if get_channel_count(img) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def pHash(img, leng=32, wid=32):
    """
    感知哈希算法
    """
    img = pre_handle_img(img, leng, wid)

    # DCT变换
    dct = cv2.dct(np.float32(img))
    # 掩码
    dct_roi = dct[0:8, 0:8]
    avreage = np.mean(dct_roi)
    phash_01 = (dct_roi > avreage) + 0
    # 行列转换，取第一列，转数组
    phash_list = phash_01.reshape(1, -1)[0].tolist()
    hashStr = ''.join([str(x) for x in phash_list])
    return hashStr


def dHash(img, leng=9, wid=8):
    """
    difference hashing
    差异哈希算法：分别计算左右两个像素的差值
    """
    img = pre_handle_img(img, leng, wid)

    hash = []
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(wid):
        for j in range(wid):
            if img[i, j] > img[i, j + 1]:
                hash.append(1)
            else:
                hash.append(0)
    hashStr = ''.join([str(x) for x in hash])
    return hashStr


def aHash(img, leng=8, wid=8):
    """
    average hashing
    平均哈希算法：对每个像素，与平均像素值进行比较大小
    """
    img = pre_handle_img(img, leng, wid)

    hash = []
    # 求均值
    avreage = np.mean(img)
    # 遍历累加求像素和
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # 灰度大于平均值为1相反为0生成图片的hash值
            if img[i, j] >= avreage:
                hash.append(1)
            else:
                hash.append(0)
    hashStr = ''.join([str(x) for x in hash])
    return hashStr


def wHash(img, leng=8, wid=8):
    """
    wavelet hashing
    离散小波变换
    """
    hash = []
    # TODO
    hashStr = ''.join([str(x) for x in hash])
    return hashStr


def calculate_hamming_distance(hash1, hash2):
    """
    计算两个hash值的汉明距离
    """
    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
    return num


def calculate_similarity(distance):
    """
    根据汉明距离计算相似度
    """
    return (1 - distance * 1.0 / 64)


def calculate_hamming_distance_btw_imgs(url1, url2, p=False, d=False, a=False, w=False):
    """
    计算两张图片的汉明距离
    Args:
        url1: 图片1的URL地址
        url2: 图片2的URL地址
        p: 是否计算pHash值
        d: 是否计算dHash值
        a: 是否计算aHash值
    Returns:
        {
            "p": 0.92345,
            "d": 0.88822,
            "a": 1
            "w": 0.99334
        }
    """
    distanceResult = {}

    data1 = img_to_hashes(url1, p, d, a, w)
    data2 = img_to_hashes(url2, p, d, a, w)

    if p:
        data1_v = data1['p']
        data2_v = data2['p']
        distance = calculate_hamming_distance(data1_v['o'], data2_v['o'])
        distancex = calculate_hamming_distance(data1_v['x'], data2_v['x'])
        distancey = calculate_hamming_distance(data1_v['y'], data2_v['y'])
        distancez = calculate_hamming_distance(data1_v['z'], data2_v['z'])
        distanceH = calculate_hamming_distance(data1_v['h'], data2_v['h'])
        distanceV = calculate_hamming_distance(data1_v['v'], data2_v['v'])
        array = [distance, distancex, distancey, distancez, distanceH, distanceV]
        maxDis = min(array)
        distanceResult['p'] = {}
        distanceResult['p']['distance'] = maxDis
        distanceResult['p']['similarity'] = calculate_similarity(maxDis)
    if d:
        data1_v = data1['d']
        data2_v = data2['d']
        distance = calculate_hamming_distance(data1_v['o'], data2_v['o'])
        distancex = calculate_hamming_distance(data1_v['x'], data2_v['x'])
        distancey = calculate_hamming_distance(data1_v['y'], data2_v['y'])
        distancez = calculate_hamming_distance(data1_v['z'], data2_v['z'])
        distanceH = calculate_hamming_distance(data1_v['h'], data2_v['h'])
        distanceV = calculate_hamming_distance(data1_v['v'], data2_v['v'])
        array = [distance, distancex, distancey, distancez, distanceH, distanceV]
        maxDis = min(array)
        distanceResult['d'] = {}
        distanceResult['d']['distance'] = maxDis
        distanceResult['d']['similarity'] = calculate_similarity(maxDis)
    if a:
        data1_v = data1['a']
        data2_v = data2['a']
        distance = calculate_hamming_distance(data1_v['o'], data2_v['o'])
        distancex = calculate_hamming_distance(data1_v['x'], data2_v['x'])
        distancey = calculate_hamming_distance(data1_v['y'], data2_v['y'])
        distancez = calculate_hamming_distance(data1_v['z'], data2_v['z'])
        distanceH = calculate_hamming_distance(data1_v['h'], data2_v['h'])
        distanceV = calculate_hamming_distance(data1_v['v'], data2_v['v'])
        array = [distance, distancex, distancey, distancez, distanceH, distanceV]
        maxDis = min(array)
        distanceResult['a'] = {}
        distanceResult['a']['distance'] = maxDis
        distanceResult['a']['similarity'] = calculate_similarity(maxDis)
    if w:
        data1_v = data1['w']
        data2_v = data2['w']
        distance = calculate_hamming_distance(data1_v['o'], data2_v['o'])
        distancex = calculate_hamming_distance(data1_v['x'], data2_v['x'])
        distancey = calculate_hamming_distance(data1_v['y'], data2_v['y'])
        distancez = calculate_hamming_distance(data1_v['z'], data2_v['z'])
        distanceH = calculate_hamming_distance(data1_v['h'], data2_v['h'])
        distanceV = calculate_hamming_distance(data1_v['v'], data2_v['v'])
        array = [distance, distancex, distancey, distancez, distanceH, distanceV]
        maxDis = min(array)
        distanceResult['w'] = {}
        distanceResult['w']['distance'] = maxDis
        distanceResult['w']['similarity'] = calculate_similarity(maxDis)

    return distanceResult
