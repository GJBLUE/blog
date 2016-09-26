#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jblue
# @File    : forms.py

from flask_wtf import Form
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import Length, Required
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    title = StringField('Title', validators=[Length(1, 64)])
    classify = StringField('Classify', validators=[Length(1, 64)])
    tag = StringField('Tag', validators=[Length(1, 64)])
    body = PageDownField("write some things!", validators=[Required()])
    submit = SubmitField('submit')