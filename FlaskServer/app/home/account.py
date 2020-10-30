# -*- coding:utf-8 -*-
__author__ = 'LangJin'

from flask import request,jsonify
import requests,random,string
from . import appbp
from ..utils.dbtools import Db,RedisDb
from ..utils.common import setcors,create_token,encryptiontoken
from config import db_config,redis_config,upload_folder

db = Db(db_config)
redisdb = RedisDb(redis_config) 


@appbp.route("/api/regist",methods=['post'])
def regist():
    """
    用户注册
    """
    requestData = request.get_json()
    username = requestData.get("username")
    password = requestData.get("password")
    dbres = db.query("select * from tb_user where username = '{}';".format(username))
    if len(dbres) == 0: 
        dbres = db.commit("insert into tb_user (username,password,nickname) values ('{}','{}','{}');".format(username,password,username))
        data = setcors(msg=dbres,status=200)
    else:
        data = setcors(msg='账号已存在')
    return jsonify(data)
    

@appbp.route("/api/login",methods=['post'])
def login():
    """
    用户登陆
    """
    requestData = request.get_json()
    username = requestData.get("username")
    password = requestData.get("password")
    dbres = db.query("select id,username,password,nickname,phone,status from tb_user where username = '{}' and status != '0';".format(username))
    print(dbres)
    if len(dbres) == 1:
        if dbres[0].pop('password') == password:
            token = create_token()
            dbres[0].update(token=token)
            redisdb.setredisvalue(username,dbres[0])
            token = encryptiontoken(username,token)
            dbres[0].update(token=token)
            data = setcors(data=dbres[0],msg='登陆成功',status=200)
        else:
            data = setcors(msg='密码不正确')
    else:
        data = setcors(msg='账号不存在或者账号异常')
    return jsonify(data)



@appbp.route("/api/phone/login",methods=['post'])
def tellogin():
    """
    用户使用手机登陆
    """
    requestData = request.get_json()
    phone = requestData.get("phone")
    code = requestData.get("code")
    if phone and code:
        dbres = db.query("select id,code from tb_sms_log where phone = '{}' and status = '0' and content = 'login' order by createTime desc limit 1;".format(phone))
        if len(dbres) == 0:
            data = setcors(msg='验证码不正确')
            return jsonify(data)
        dbcode = dbres[0].get("code")
        if dbcode == code:
            dbmsg2 = db.commit("update tb_sms_log set status = '1' where id = {};".format(dbres[0].get("id")))
            dbres = db.query("select id,username,nickname,phone,status from tb_user where phone = '{}';".format(phone))
            if len(dbres) == 1:
                if dbres[0].get("status") != '0':
                    username = dbres[0].get("username")
                    token = create_token()
                    dbres[0].update(token=token)
                    redisdb.setredisvalue(username,dbres[0])
                    token = encryptiontoken(username,token)
                    dbres[0].update(token=token)
                    data = setcors(data=dbres[0],msg='登陆成功',status=200)
                else:
                    data = setcors(msg='账号被冻结，请联系管理员')
            else:
                dbmsg = db.commit("insert into tb_user (username,nickname,phone) values ('{}','{}','{}');".format(phone,phone,phone))
                dbres = db.query("select id,username,phone,status,nickname from tb_user where phone = '{}' and status != '0';".format(phone))
                username = dbres[0].get("username")
                token = create_token()
                dbres[0].update(token=token)
                redisdb.setredisvalue(username,dbres[0])
                token = encryptiontoken(username,token)
                dbres[0].update(token=token)
                data = setcors(data=dbres[0],msg='登陆成功',status=200)
        else:
            dbmsg2 = db.commit("update tb_sms_log set status = '1' where id = {};".format(dbres[0].get("id")))
            data = setcors(msg='验证码不正确')
    else:
        data = setcors(msg='参数不对')
    return jsonify(data)




@appbp.route("/api/system/login",methods=['post'])
def systemlogin():
    """
    管理员登陆
    """
    requestData = request.get_json()
    username = requestData.get("username")
    password = requestData.get("password")
    dbres = db.query("select id,username,password,nickname,phone,headimg from tb_system_user where username = '{}' and status = '1';".format(username))
    if len(dbres) == 1:
        if dbres[0].pop('password') == password:
            token = create_token()
            dbres[0].update(token=token)
            redisdb.setredisvalue(username,dbres[0])
            token = encryptiontoken(username,token)
            dbres[0].update(token=token)
            data = setcors(data=dbres[0],msg='登陆成功',status=200)
        else:
            data = setcors(msg='密码不正确')
    else:
        data = setcors(msg='账号不存在或者账号异常')
    return jsonify(data)
    


@appbp.route("/api/weixin/login",methods=['post'])
def wxlogin():
    """
    用户使用微信登陆
    """
    requestData = request.get_json()
    openId = requestData.get("openId")
    nickName = requestData.get("nickName")
    avatarUrl = requestData.get("avatarUrl")
    unionId = requestData.get("unionId")
    if openId and nickName and avatarUrl and unionId:
        r = requests.get(avatarUrl)
        headimg = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        with open('./'+upload_folder + '/{}.png'.format(headimg), 'wb') as f:
            f.write(r.content)
        dbres = db.query("select id,username,nickname,phone,status,headimg from tb_user where wxunionId = '{}';".format(unionId))
        if len(dbres) == 1:
            if dbres[0].get("status") != '0':
                username = dbres[0].get("username")
                token = create_token()
                dbres[0].update(token=token)
                redisdb.setredisvalue(username,dbres[0])
                token = encryptiontoken(username,token)
                dbres[0].update(token=token)
                data = setcors(data=dbres[0],msg='登陆成功',status=200)
            else:
                data = setcors(msg='账号被冻结，请联系管理员')
        else:
            dbmsg = db.commit("insert into tb_user (username,nickname,wxopenId,wxunionId,headimg) values ('{}','{}','{}','{}','{}.png');".format(unionId,nickName,openId,unionId,headimg))
            dbres = db.query("select id,username,phone,status,nickname,headimg from tb_user where wxunionId = '{}' and status != '0';".format(unionId))
            username = dbres[0].get("username")
            token = create_token()
            dbres[0].update(token=token)
            redisdb.setredisvalue(username,dbres[0])
            token = encryptiontoken(username,token)
            dbres[0].update(token=token)
            data = setcors(data=dbres[0],msg='登陆成功',status=200)
    else:
        data = setcors(msg='参数不对')
    return jsonify(data)
