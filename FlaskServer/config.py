# -*- coding:utf-8 -*-
__author__ = 'LangJin'

# 开发环境
class DevelopConfig:
    DEBUG = True
    JSON_AS_ASCII = False #json 中文支持
    BABEL_DEFAULT_LOCALE = 'zh'
    SECRET_KEY = "ssssdddd"    # SESSION配置
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 2MB


# 线上发布环境
class ProductionConfig:
    DEBUG = False
    JSON_AS_ASCII = False #json 中文支持
    BABEL_DEFAULT_LOCALE = 'zh'
    SECRET_KEY = "sdjhnskjfnsdkjfndskdfksaldaksmdadiewdoqeiwe8w7edfwedfsmcf"    # SESSION配置
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 2MB



flask_config = {
    "DevelopConfig": DevelopConfig,
    "ProductionConfig": ProductionConfig
    }

upload_folder = "./uploads"

db_config = {
    'host': '118.24.255.132',
    'port': 3306,
    'user': 'root',
    'password': 'EIWQotcukX!9hOVilQygBUfrc0TjqlVA',
    'db': 'taskDB',
    'charset': 'utf8mb4'
}


redis_config = {
    'host': '118.24.255.132',
    'port': 6379,
    'password': 'EIWQotcukX!9hOVilQygBUfrc0TjqlVA',
    'db': 0
}

redis_aconfig = {
    'host': '118.24.255.132',
    'port': 6379,
    'password': 'EIWQotcukX!9hOVilQygBUfrc0TjqlVA',
    'db': 1
}


keys = {
    "user":"sb250",
    "admin":"god666",
    "token":23
}