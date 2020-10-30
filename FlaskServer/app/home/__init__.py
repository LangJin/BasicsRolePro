# -*- coding:utf-8 -*-
__author__ = 'LangJin'
from flask import Blueprint

appbp = Blueprint("home", __name__)

from . import home,account