#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jblue
# @File    : __init__

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
