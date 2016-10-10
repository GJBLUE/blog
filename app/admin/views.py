#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jblue
# @File    : views.py

import json

from . import admin
from .. import db
from ..models import Post
from .forms import DeleteArticleForm, DeleteArticlesForm, PostForm
from flask.ext.login import login_required, current_user
from flask import render_template, redirect, flash, \
    url_for, request, current_app, jsonify, abort


@admin.route('/article_details/<int:id>', methods=['GET', 'POST'])
def article_details(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


@admin.route('/create_article', methods=['GET', 'POST'])
def create_article():
    form = PostForm()
    if request.method == "POST":
        post = Post(
            title=form.title.data,
            tag_id=form.tag_id.data,
            body=form.body.data,
            author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('admin/create_article.html', form=form)


@admin.route('/manage-articles/delete_article/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_article(id):

    article = Post.query.get_or_404(id)
    db.session.delete(article)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'删除失败', 'danger')
    else:
        flash(u'文章删除成功', 'success')

    return redirect(url_for('admin.manage_articles', page=request.args.get('page', 1, type=int)))


@admin.route('/manage-articles/delete_articles', methods=['GET', 'POST'])
@login_required
def delete_articles():
    form = DeleteArticlesForm()

    if form.validate_on_submit():
        ids = json.loads(form.articleId.data)
        for id in ids:
            article = Post.query.get_or_404(id)
            db.session.delete(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败', 'danger')
        else:
            flash(u'成功删除%s篇博文和%s条评论！' % len(ids), 'success')
    if form.errors:
        flash(u'删除失败', 'danger')

    return redirect(url_for('admin.manage_articles', page=request.args.get('page', 1, type=int)))


@admin.route('/manage-articles/edit_articles/<int:id>')
def edit_articles(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.tag_id = form.tag_id.data
        db.session.add(post)
        flash('Articles Published')
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.tag_id.data = post.tag_id
    return render_template('edit_post.html', form=form)


@admin.route('manage_articles', methods=['GET', 'POST'])
@login_required
def manage_articles():
    del_single_form = DeleteArticleForm()  # for delete an article
    del_multi_form = DeleteArticlesForm()  # for delete articles

    page = request.args.get('page', 1, type=int)
    result = Post.query.order_by(Post.timestamp.desc())
    pagination_search = result.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    articles = pagination_search.items

    return render_template('admin/manage_articles.html', Article=Post, articles=articles,
                           pagination=pagination_search, endpoint='admin.manage_articles',
                           del_single_form=del_single_form, del_multi_form=del_multi_form,
                           page=page
                           )