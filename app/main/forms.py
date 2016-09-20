#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jblue
# @File    : forms.py

from flask_wtf import Form
from wtforms import SubmitField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    body = PageDownField("write some things!", validators=[Required()])
    submit = SubmitField('submit')