#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/9/18 下午4:10
# @Author  : Jblue
# @File    : views.py

from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')