#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File    : req_tool.py
@Time    : 2020/4/17 22:46
@Author  : liutwv
@Software: PyCharm
"""

from skimage import io
from urllib import request


def read_img_from_net(img_url):
    """
    读取网络图片
    Args:
        url: 图片URL地址
    Returns:
        numpy.ndarray
    """
    img_url = request.quote(img_url, safe=";/?:@&=+$,", encoding="utf-8")
    return io.imread(img_url)

