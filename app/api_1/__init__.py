#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jblue
# @File    : __init__.py

from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, posts, errors
