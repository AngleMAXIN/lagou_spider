# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask


def register_app(app):

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app


def create_app():
    app = register_app(Flask(__name__))
    return app
