#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/9/18 下午3:11
# @Author  : Jblue
# @File    : __init__.py

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import  config

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config['development'])
    config['development'].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
