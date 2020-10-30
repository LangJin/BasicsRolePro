# -*- coding:utf-8 -*-
__author__ = 'LangJin'

from flask import request,jsonify,g
from . import userbp
from ..utils.dbtools import Db,RedisDb
from ..utils.common import setcors,checkloginstatus
from config import db_config,redis_config

db = Db(db_config)
redisdb = RedisDb(redis_config) 


@userbp.before_request
def before_request():
    token = request.headers.get("token")
    userinfo = checkloginstatus(token)
    if userinfo[1] == False:
        data = setcors(msg=userinfo[0])
        return jsonify(data)
    else:
        g.userinfo = userinfo[0]


