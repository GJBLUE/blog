#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jblue
# @File    : forms.py


from flask_wtf import Form
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import Length, Required, DataRequired
from flask_pagedown.fields import PageDownField


class DeleteArticleForm(Form):
    articleId = StringField(validators=[DataRequired()])


class DeleteArticlesForm(Form):
    articleIds = StringField(validators=[DataRequired()])


class PostForm(Form):
    title = StringField('Title', validators=[Length(1, 64)])
    tag_id = StringField('Tag_id', validators=[Length(1, 64)])
    body = PageDownField("write some things!", validators=[Required()])
    submit = SubmitField('submit')