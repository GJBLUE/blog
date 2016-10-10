#!/usr/bi/env python
# -*- coding: utf-8 -*-
# @Author  : Jblue
# @File    : __init__.py.py


from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views
