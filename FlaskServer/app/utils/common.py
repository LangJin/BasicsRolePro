# -*- coding:utf-8 -*-
__author__ = 'LangJin'

import os, hashlib,urllib,time
from config import keys,redis_config
from .dbtools import RedisDb


def create_token():
    '''
    生成登陆后的token，格式如下：\n
    "eca7f38788d4764959919b46c61005038cf37f68"
    '''
    return hashlib.sha1(os.urandom(64)).hexdigest()

def encryption(username,password,role):
    '''
    说明：密码的加密算法,role是角色\n
    用法:encryption("用户名","明文密码","user")
    '''
    md5 = hashlib.md5()
    md5.update(password.encode("utf8")+username.encode("utf8")+keys.get(role).encode("utf8"))
    password = md5.hexdigest()
    return password


def encryptiontoken(username,token,role="token"):
    '''
    说明：token的加密算法,role是角色\n
    用法:encryption("用户名","原始token","user")
    '''
    num = keys.get(role)
    a = token[:num]
    b = token[(40-num)*-1:]
    username = username[::-1]
    token = a+username+b
    return token

def opentoken(token,role="token"):
    """
    解密token的算法,role默认‘token’
    """
    num = keys.get(role)
    a = token[:num]
    b = token[(40-num)*-1:]
    username = token[num:(40-num)*-1]
    username = username[::-1]
    token = a+b
    return username,token


def setcors(data=None,msg="操作成功！",status=401):
    '''
    返回体封装
    '''
    res = {
        "data":data,
        "msg":msg,
        "status":status
    }
    return res


def checkloginstatus(token):
    '''
    检查用户的登录状态
    '''
    if token == None:
        return "请先登录后再操作！",False
    userreq = opentoken(token)
    username = userreq[0]
    token = userreq[1]
    redisdb = RedisDb(redis_config)
    userinfo = redisdb.getredisvalue(username)
    if userinfo == None:
        return "请先登录后再操作！",False
    retoken = userinfo.get("token")
    if retoken == token:
        return userinfo,True
    else:
        return "token无效，请重新登录",False


def pageSizeCount(counts,pagesize,pagenum):
    """
    页码计算
    counts：总数
    pagesize：一页显示几条数据
    pagenum：第几页
    """
    nums = str(counts/pagesize).split(".")
    allpagenum = int(nums[0])
    if int(nums[1]) > 0:
        allpagenum = allpagenum + 1
    if pagenum <= allpagenum:
        startnum = (pagenum-1)*pagesize
        return startnum
    else:
        return "当前查询没有数据"



def strtimetotime(timedata):
    """
    时间格式转时间戳
    """
    # 转为时间数组
    timeArray = time.strptime(timedata, "%Y-%m-%d %H:%M:%S")
    # 转为时间戳
    timeStamp = int(time.mktime(timeArray))
    return timeStamp