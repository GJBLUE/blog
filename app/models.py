#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/9/18 下午3:21
# @Author  : Jblue
# @File    : models.py

from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<User %r>' % self.name
