#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File    : settings.py.py
@Time    : 2020/5/18 12:52
@Author  : LT
@Software: PyCharm
"""

import os

BASE_DIR = '/opt'

RUN_LOG_FILE = os.path.join(BASE_DIR, "logs", "text-similarity.log")
ERROR_LOG_FILE = os.path.join(BASE_DIR, "logs", "text-similarity-error.log")
