#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/9/18 下午4:10
# @Author  : Jblue
# @File    : views.py

from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, abort, flash, request, current_app
from . import main
from ..models import Post


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)

