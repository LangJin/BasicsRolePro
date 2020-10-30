# -*- coding:utf-8 -*-
from flask import Blueprint,jsonify,Flask
from .utils.common import setcors
import traceback,logging

errorbp = Blueprint("errorbp",__name__)
app = Flask(__name__)


@errorbp.app_errorhandler(404)
def not_found_page(e):
    data = setcors(msg='%s' % e )
    return jsonify(data),404


@errorbp.app_errorhandler(405)
def request_method_error(e):
    data = setcors(msg='%s' % e )
    return jsonify(data),405


@errorbp.app_errorhandler(400)
def request_data_error(e):
    data = setcors(msg='%s' % e )
    return jsonify(data),400


@errorbp.app_errorhandler(Exception)
def error_info(e):
    print(traceback.print_exc())
    data = setcors(msg='服务器异常，请联系管理员')
    return jsonify(data),500


