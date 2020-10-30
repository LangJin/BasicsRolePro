# -*- coding:utf-8 -*-
__author__ = 'LangJin'
from flask import Flask
from config import flask_config
from .errors import errorbp
from .user import userbp
from .home import appbp
from .admin import adminbp



def create_app(config_name="DevelopConfig"):
    '''
    工厂方法
    '''
    app = Flask(__name__)
    app.config.from_object(flask_config[config_name])
    app.register_blueprint(errorbp)  # 注册蓝本
    app.register_blueprint(userbp)  # 注册蓝本
    app.register_blueprint(adminbp)  # 注册蓝本
    app.register_blueprint(appbp)  # 注册蓝本
    return app
