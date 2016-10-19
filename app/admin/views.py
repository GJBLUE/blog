#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jblue
# @File    : views.py

import json

from . import admin
from .. import db
from ..models import Post, ArticleType
from .forms import DeleteArticleForm, DeleteArticlesForm, PostForm, TagForm
from flask.ext.login import login_required, current_user
from flask import render_template, redirect, flash, \
    url_for, request, current_app, abort


@admin.route('/article_details/<int:id>', methods=['GET', 'POST'])
def article_details(id):
    post = Post.query.get_or_404(id)
    return render_template('admin/article_details.html', post=post)


@admin.route('/create_article', methods=['GET', 'POST'])
def create_article():
    form = PostForm()
    tags = [(t.id, t.name) for t in ArticleType.query.all()]
    form.tags.choices = tags
    if request.method == "POST":
        post = Post(
            title=form.title.data,
            tag_id=form.tags.data,
            body=form.body.data,
            author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('admin/create_article.html', form=form)


@admin.route('/manage_articles/delete_article/<int:id>', methods=['GET', 'POST'])
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
            flash(u'成功删除%s篇博文' % len(ids), 'success')
    if form.errors:
        flash(u'删除失败', 'danger')

    return redirect(url_for('admin.manage_articles', page=request.args.get('page', 1, type=int)))


@admin.route('/manage_articles/edit_articles/<int:id>', methods=['GET', 'POST'])
def edit_articles(id):
    form = PostForm()
    post = Post.query.get_or_404(id)
    tags = [(t.id, t.name) for t in ArticleType.query.all()]
    form.tags.choices = tags

    if current_user != post.author:
        abort(403)

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.tag_id = form.tags.data
        db.session.add(post)
        db.session.commit()
        flash('Articles Published')
        return redirect(url_for('admin.article_details', id=post.id))
    else:
        flash('Publish error!')
    form.title.data = post.title
    form.body.data = post.body
    form.tags.data = post.tag_id
    return render_template('admin/edit_article.html', form=form)


@admin.route('/manage_articles', methods=['GET', 'POST'])
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


@admin.route('/manage_tags', methods=['GET', 'POST'])
@login_required
def manage_tags():
    form = TagForm()
    page = request.args.get('page', 1, type=int)

    result = ArticleType.query.order_by(ArticleType.id.desc())
    pagination_search = result.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    tags = pagination_search.items

    return render_template('admin/manage_tags.html', Tag=ArticleType, tags=tags, form=form,
                           endpoint='admin.manage_articles', pagination=pagination_search)


@admin.route('/manage_article/create_tag', methods=['POST'])
@login_required
def create_tag():
    form = TagForm()

    if form.validate_on_submit():
        name = form.tagname.data
        flag = ArticleType.query.filter_by(name=name).first()
        if flag:
            flash(u'添加失败!分类已存在!', 'danger')
        else:
            article_type = ArticleType(name=name)
            db.session.add(article_type)
            db.session.commit()
            flash(u'sucess!', 'sucess')

    return redirect(url_for('admin.manage_tags'))


@admin.route('/manage_tags/edit_tag/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tag(id):
    print id
    post = ArticleType.query.get_or_404(id)
    exist_tags = ArticleType.query.all()
    form = TagForm()
    page = request.args.get('page', 1, type=int)
    print request.data
    if form.validate_on_submit():
        print 123
        tag_name = form.tagname.data
        print tag_name
        post.name = tag_name
        if tag_name in exist_tags:
            flash(u'该分类已存在!', 'danger')
        else:
            db.session.add(post)
            db.session.commit()
            flash('Articles Published')
        return redirect(url_for('.manage_tags'))
    form.tagname.data = post.name
    return redirect(url_for('.manage_tags', page=page))


@admin.route('/manage_articles/delete_tag/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_tag(id):

    tag = ArticleType.query.get_or_404(id)
    db.session.delete(tag)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'删除失败', 'danger')
    else:
        flash(u'文章删除成功', 'success')

    return redirect(url_for('admin.manage_tags', page=request.args.get('page', 1, type=int)))
