#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File    : req_tool.py
@Time    : 2020/4/17 22:46
@Author  : liutwv
@Software: PyCharm
"""

import requests
import cv2
import numpy as np

def read_img_from_net(img_url):
    """
    读取网络图片
    Args:
        url: 图片URL地址
    Returns:
        numpy.ndarray
    """
    img_data = requests.get(img_url).content
    img = np.asarray(bytearray(img_data), dtype="uint8")
    img = cv2.imdecode(img, -1)

    return img

