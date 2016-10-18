#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jblue
# @File    : forms.py


from flask_wtf import Form
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import Length, Required, DataRequired
from flask_pagedown.fields import PageDownField


class DeleteArticleForm(Form):
    articleId = StringField(validators=[DataRequired()])


class DeleteArticlesForm(Form):
    articleIds = StringField(validators=[DataRequired()])


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 64)])
    tags = SelectField('Tags', coerce=int, validators=[DataRequired()])
    body = PageDownField("Body", validators=[Required()])
    #submit = SubmitField('submit')


class TagForm(Form):
    tagname = StringField('Tag', validators=[Length(1, 20)])
