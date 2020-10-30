# -*- coding:utf-8 -*-
__author__ = 'LangJin'

from flask import request,jsonify,g,send_from_directory
from . import adminbp
from ..utils.dbtools import Db,RedisDb
from ..utils.common import setcors,checkloginstatus,pageSizeCount
from config import db_config,redis_config,upload_folder
import random,string,os,time,json,logging


db = Db(db_config)
redisdb = RedisDb(redis_config) 



"""
个人中心
"""
@adminbp.route("/api/system/admininfo",methods=["get"])
def get_system_admininfo():
    '''
    获取登陆用户信息
    '''
    userid = g.userinfo.get("id")
    dbres = db.query("select * from tb_system_user where id = {};".format(userid))[0]
    data = setcors(data=dbres,status=200)
    return jsonify(data)


@adminbp.route("/api/system/updateinfo",methods=["post"])
def updateinfo():
    """
    修改个人资料
    """
    requestData = request.get_json()
    userid = g.userinfo.get("id")
    nickname = requestData.get("nickname")
    phone = requestData.get("phone")
    headimg = requestData.get("headimg")
    dbres = db.query("select * from tb_system_user where id = {} and status = '1';".format(userid))
    if dbres != 0:
        if nickname and phone and headimg:
            dbmsg = db.commit("update tb_system_user set nickname = '{}',phone='{}',headimg='{}'\
                where id = {};".format(nickname,phone,headimg,userid))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    else:
        data = setcors(msg="管理员不存在或者被冻结")
    return jsonify(data)



@adminbp.route("/api/system/updatepassword",methods=["post"])
def updatepassword():
    """
    修改密码
    """
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    oldps = requestData.get("oldps")
    newps = requestData.get("newps")
    dbres = db.query("select * from tb_system_user where id = {} and status = '1';".format(userid))
    if dbres != 0:
        if oldps and newps:
            if dbres[0].pop('password') == oldps:
                dbmsg = db.commit("update tb_system_user set password = '{}' where id = {};".format(newps,userid))
                data = setcors(msg=dbmsg,status=200)
            else:
                data = setcors(msg="旧密码不正确")
        else:
            data = setcors(msg="参数不能为空")
    else:
        data = setcors(msg="管理员不存在或者被冻结")
    return jsonify(data)


"""
轮播图管理
"""


@adminbp.route("/api/system/newbanner",methods=["post"])
def newbanner():
    requestData = request.get_json()
    title = requestData.get("title")
    imghost = requestData.get("imghost")
    linkurl = requestData.get("linkurl")
    sort = requestData.get("sort")
    if title and imghost and linkurl and sort:
        dbmsg = db.commit("insert into tb_system_banner (title,imghost,sort,linkurl) \
            values ('{}','{}','{}','{}');".format(title,json.dumps(imghost),sort,linkurl))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)


@adminbp.route("/api/system/updatebanner",methods=["post"])
def updatebanner():
    """
    修改banner图
    """
    requestData = request.get_json()
    ids = requestData.get("id")
    title = requestData.get("title")
    imghost = requestData.get("imghost")
    linkurl = requestData.get("linkurl")
    sort = requestData.get("sort")
    dbres = db.query("select * from tb_system_banner where id = {};".format(ids))
    if dbres != 0:
        if title and imghost and linkurl and sort and ids:
            dbmsg = db.commit("update tb_system_banner set title = '{}',imghost='{}',sort='{}',linkurl='{}' \
                where id = {};".format(title,json.dumps(imghost),sort,linkurl,ids))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    else:
        data = setcors(msg="修改的轮播图不存在")
    return jsonify(data)



@adminbp.route('/api/system/bannerlist/<int:pagenum>/<int:pagesize>',methods=["post"])
def get_banner_list(pagenum,pagesize):
    '''
    轮播图列表
    '''
    requestData = request.get_json()
    sqlquery = ""
    if len(requestData) > 0:
        sqlquery = "where 'test'='test' "
        status = requestData.get("status")
        if status != "" and status != None:
            sqlquery = sqlquery + "and status = '{}'".format(status)
        title = requestData.get("title")
        if title != "" and title != None:
            sqlquery = sqlquery + "and title like '%{}%'".format(title)
    counts = db.query("select count(*) counts from tb_system_banner {};".format(sqlquery))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select * from tb_system_banner {} order by sort limit {},{};".format(sqlquery,startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/setbannerstatus/<int:id>",methods=["get"])
def setbannerstatus(id):
    """
    启用、禁用轮播图
    """
    dbres = db.query("select * from tb_system_banner where id = {};".format(id))
    if len(dbres) != 0:
        dbmsg = db.commit("update tb_system_banner set status = (case when status = 1 then 0 else 1 end) where id = {};".format(id))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="轮播图不存在")
    return jsonify(data)


"""
任务管理
"""

@adminbp.route("/api/system/tasklist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_tasklist(pagenum,pagesize):
    '''
    用户任务列表
    '''
    requestData = request.get_json()
    sqlquery = "where a.status !='2' "
    if len(requestData) > 0:
        phone = requestData.get("phone")
        if phone != "" and phone != None:
            sqlquery = sqlquery + "and b.phone = '{}'".format(phone)
        timedata = requestData.get("timedata")
        if timedata != "" and phone != timedata:
            sqlquery = sqlquery + "and a.stop_time between '{}' and '{}'".format(timedata[0],timedata[1])
        nickname = requestData.get("nickname")
        if nickname != "" and nickname != None:
            sqlquery = sqlquery + "and b.nickname like '%{}%'".format(nickname)
        status = requestData.get("status")
        if status != "" and status != None:
            sqlquery = sqlquery + "and a.status = '{}'".format(status)
        idx = requestData.get("id")
        if idx != "" and idx != None:
            sqlquery = sqlquery + "and b.id = '{}'".format(idx)
    counts = db.query("select count(*) counts from tb_tasks a join tb_user b on a.uid = b.id join tb_task_type c on a.type = c.id {};".format(sqlquery))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        sql = "select a.id,a.title,a.content,c.tasktype,a.imglist,b.phone,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') \
            createtime, DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') stop_time,\
            b.nickname,a.tasknums,a.taskReceiveNum,a.taskmoney,a.status \
            from tb_tasks a join tb_user b on a.uid = b.id join tb_task_type c on a.type = c.id \
            {} limit {},{};".format(sqlquery,startnum,pagesize)
        dbres = db.query(sql)
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/taskinfo/<int:taskid>",methods=["get"])
def get_taskinfo(taskid):
    '''
    任务详情
    '''
    dbres = db.query("select a.id,a.title,a.content,c.tasktype,a.imglist,b.phone,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime, DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') stop_time,\
            b.nickname,a.tasknums,a.taskReceiveNum,a.taskmoney,a.status \
            from tb_tasks a join tb_user b on a.uid = b.id join tb_task_type c on a.type = c.id \
            where a.id = {};".format(taskid))
    if len(dbres) != 1:
        data = setcors(msg="任务不存在")
    else:
        data = setcors(data=dbres[0],status=200)
    return jsonify(data)


"""
申诉管理
"""
@adminbp.route("/api/system/appeallist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_appeallist(pagenum,pagesize):
    '''
    用户申诉列表
    '''
    requestData = request.get_json()
    sqlquery = ""
    if len(requestData) > 0:
        sqlquery = "where 'test'='test' "
        phone = requestData.get("phone")
        if phone != "" and phone != None:
            sqlquery = sqlquery + "and c.phone = '{}'".format(phone)
        timedata = requestData.get("timedata")
        if timedata != "" and phone != timedata:
            sqlquery = sqlquery + "and a.createTime between '{}' and '{}'".format(timedata[0],timedata[1])
        nickname = requestData.get("nickname")
        if nickname != "" and nickname != None:
            sqlquery = sqlquery + "and c.nickname like '%{}%'".format(nickname)
        status = requestData.get("status")
        if status != "" and status != None:
            sqlquery = sqlquery + "and a.status = '{}'".format(status)
        idx = requestData.get("id")
        if idx != "" and idx != None:
            sqlquery = sqlquery + "and b.id = '{}'".format(idx)
    counts = db.query("select count(*) counts from tb_task_appeal a join tb_tasks b on a.utaskid = b.id join tb_user c on c.id = a.uid {};".format(sqlquery))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select a.id,a.content,c.nickname,c.phone,b.title,a.status,DATE_FORMAT(a.createTime,'%Y-%m-%d %H:%i:%s') createTime \
            from tb_task_appeal a join tb_tasks b on a.utaskid = b.id join tb_user c on c.id = a.uid \
            {} limit {},{};".format(sqlquery,startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/appealinfo/<int:taskid>",methods=["get"])
def get_appeal(taskid):
    '''
    申诉详情详情
    '''
    appealinfo = db.query("select a.id,a.utaskid,c.nickname,a.status,c.phone,DATE_FORMAT(a.createTime,'%Y-%m-%d %H:%i:%s') createTime \
        from tb_task_appeal a join tb_tasks b on a.utaskid = b.id join tb_user c on c.id = a.uid \
        where a.id = {};".format(taskid))
    if len(appealinfo) != 1:
        data = setcors(msg="任务不存在")
    else:
        utaskid = appealinfo[0].get("utaskid")
        utaskinfo = db.query("select a.taskid,a.imglist,a.remark,DATE_FORMAT(a.updatetime,'%Y-%m-%d %H:%i:%s') updatetime,b.nickname,b.phone \
            from tb_user_task a join tb_user b on a.uid = b.id where a.id = {};".format(utaskid))
        taskid = utaskinfo[0].get("taskid")
        taskinfo = db.query("select a.id,a.title,a.content,a.imglist,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime,c.tasktype,b.nickname,\
            b.phone,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') stop_time,a.taskmoney,a.tasknums,a.taskReceiveNum \
            from tb_tasks a join tb_user b on a.uid = b.id join tb_task_type c on a.type = c.id \
            where a.id = {};".format(taskid))
        data = {"appeal":appealinfo[0],"utaskinfo":utaskinfo[0],"taskinfo":taskinfo[0]}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/appeal/<int:appealid>",methods=["post"])
def set_appeal(appealid):
    '''
    申诉操作
    '''
    requestData = request.get_json()
    dbres = db.query("select a.id,c.uid from tb_user_task a join tb_task_appeal b on a.id = b.utaskid join tb_tasks c on a.taskid = c.id where b.id = {};".format(appealid))
    if len(dbres) != 1:
        data = setcors(msg="该审核数据不存在")
    else:
        utaskid = dbres[0].get("id")
        userid = dbres[0].get("uid")
        status = requestData.get("status")
        if status in ("1",1):
            dbres = db.query("select appealerroenums from tb_user where id = {};".format(userid))
            appealerroenums = dbres[0].get("appealerroenums")
            dbmsg = db.commit("update tb_user set appealerroenums = '{}' where id = {};".format(int(appealerroenums)+1,userid))
            dbmsg1 = db.commit("update tb_task_appeal set status = 1 where id = {};".format(appealid))
            dbmsg2 = db.commit("update tb_user_task set status = 2 where id = {};".format(utaskid))
            data = setcors(data=dbmsg1 and dbmsg2 and dbmsg,status=200)
        elif status in ("2",2):
            dbmsg1 = db.commit("update tb_task_appeal set status = 2 where id = {};".format(appealid))
            dbmsg2 = db.commit("update tb_user_task set status = 3 where id = {};".format(utaskid))
            data = setcors(data=dbmsg1 and dbmsg2,status=200)
        else:
            data = setcors(msg="审核状态不正确")
    return jsonify(data)


"""
会员管理
"""

@adminbp.route("/api/system/userlist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_userlist(pagenum,pagesize):
    '''
    用户列表
    '''
    requestData = request.get_json()
    sqlquery = ""
    if len(requestData) > 0:
        sqlquery = "where 'test'='test' "
        phone = requestData.get("phone")
        if phone != "" and phone != None:
            sqlquery = sqlquery + "and phone = '{}'".format(phone)
        timedata = requestData.get("timedata")
        if timedata != "" and phone != timedata:
            sqlquery = sqlquery + "and create_time between '{}' and '{}'".format(timedata[0],timedata[1])
        nickname = requestData.get("nickname")
        if nickname != "" and nickname != None:
            sqlquery = sqlquery + "and nickname like '%{}%'".format(nickname)
        status = requestData.get("status")
        if status != "" and status != None:
            sqlquery = sqlquery + "and status = '{}'".format(status)
        idx = requestData.get("id")
        if idx != "" and idx != None:
            sqlquery = sqlquery + "and b.id = '{}'".format(idx)
    counts = db.query("select count(*) counts from tb_user {};".format(sqlquery))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select id,nickname,phone,headimg,appealerroenums,DATE_FORMAT(create_time,'%Y-%m-%d %H:%i:%s') create_time,status from tb_user {} limit {},{};".format(sqlquery,startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/userinfo/<int:userid>",methods=["post"])
def get_userinfo(userid):
    '''
    查看用户详情
    '''
    dbres = db.query("select id,nickname,phone,DATE_FORMAT(create_time,'%Y-%m-%d %H:%i:%s') create_time,status,headimg,withdrawal + money moneys from tb_user where id = {};".format(userid))
    if len(dbres) != 1:
        data = setcors(msg="用户不存在")
    else:
        dbutasknum = db.query("select a.id,a.nickname,count(*) counts from tb_user a join tb_user_task b on a.id = b.uid  where b.`status` in ('0','1','4') group by a.id having a.id = {};".format(userid))  # 进行中的任务
        if len(dbutasknum) > 0:
            dbutasknum = dbutasknum[0].get("counts")
        else:
            dbutasknum = 0
        dbutaskoknum = db.query("select a.id,a.nickname,count(*) counts from tb_user a join tb_user_task b on a.id = b.uid  where b.`status` in ('2') group by a.id having a.id = {};".format(userid))  # 完成的任务
        if len(dbutaskoknum) > 0:
            dbutaskoknum = dbutaskoknum[0].get("counts")
        else:
            dbutaskoknum = 0
        data = {"userinfo":dbres[0],"tasknum":{"taskingnum":dbutasknum,"taskendnum":dbutaskoknum}}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/updateuserinfo/<int:userid>",methods=["post"])
def updateuserinfo(userid):
    '''
    修改用户信息
    '''
    requestData = request.get_json()
    nickname = requestData.get("nickname")
    headimg = requestData.get("headimg")
    dbres = db.query("select * from tb_user where id = {};".format(userid))
    if len(dbres) != 1:
        data = setcors(msg="用户不存在")
    else:
        if nickname and headimg:
            dbmsg = db.commit("update tb_user set nickname = '{}',headimg = '{}' where id = {};".format(nickname,headimg,userid))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    return jsonify(data)


@adminbp.route("/api/system/newuser",methods=["post"])
def createuserinfo():
    '''
    新增用户信息
    '''
    requestData = request.get_json()
    nickname = requestData.get("nickname")
    headimg = requestData.get("headimg")
    phone = requestData.get("phone")
    dbres = db.query("select * from tb_user  where phone = {};".format(phone))
    if len(dbres) != 0:
        data = setcors(msg="用户已存在")
    else:
        if nickname and headimg and phone:
            sql = "insert into tb_user (username,password,phone,headimg,nickname) values ('{}','123456','{}','{}','{}');".format(phone,phone,headimg,nickname)
            dbmsg = db.commit(sql)
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    return jsonify(data)



@adminbp.route("/api/system/updateuserstatus/<int:userid>",methods=["post"])
def updateuserstatus(userid):
    '''
    修改用户状态
    '''
    requestData = request.get_json()
    status = requestData.get("status")
    dbres = db.query("select * from tb_user where id = {};".format(userid))
    if len(dbres) != 1:
        data = setcors(msg="用户不存在")
    else:
        if status in (0,'0'):
            dbmsg = db.commit("update tb_user set status = '0' where id = {};".format(userid))
            data = setcors(msg=dbmsg,status=200)
        elif status in (1,'1'):
            dbmsg = db.commit("update tb_user set status = '1' where id = {};".format(userid))
            data = setcors(msg=dbmsg,status=200)
        elif status in (2,'2'):
            dbmsg = db.commit("update tb_user set status = '2' where id = {};".format(userid))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    return jsonify(data)



"""
财务管理
"""

@adminbp.route("/api/system/taskmoneylist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_task_moneylist(pagenum,pagesize):
    '''
    财务列表
    '''
    requestData = request.get_json()
    sqlquery = "where a.status != '2' "
    if len(requestData) > 0:
        phone = requestData.get("phone")
        if phone != "" and phone != None:
            sqlquery = sqlquery + "and b.phone = '{}'".format(phone)
        timedata = requestData.get("timedata")
        if timedata != "" and phone != timedata:
            sqlquery = sqlquery + "and a.updatetime between '{}' and '{}'".format(timedata[0],timedata[1])
        nickname = requestData.get("nickname")
        if nickname != "" and nickname != None:
            sqlquery = sqlquery + "and b.nickname like '%{}%'".format(nickname)
        idx = requestData.get("id")
        if idx != "" and idx != None:
            sqlquery = sqlquery + "and b.id = '{}'".format(idx)
    counts = db.query("select count(*) counts from tb_tasks a join tb_user b on a.uid = b.id join tb_task_type c on a.type = c.id {};".format(sqlquery))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select a.id,c.tasktype,a.title,b.nickname,b.phone,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') stop_time,a.taskallmoney,a.taskProfitratio \
            from tb_tasks a join tb_user b on a.uid = b.id join tb_task_type c on a.type = c.id \
            {} limit {},{};".format(sqlquery,startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/withdrawallist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_user_withdrawallist(pagenum,pagesize):
    '''
    提现申请列表
    '''
    requestData = request.get_json()
    sqlquery = ""
    if len(requestData) > 0:
        sqlquery = "where 'test'='test' "
        phone = requestData.get("phone")
        if phone != "" and phone != None:
            sqlquery = sqlquery + "and b.phone = '{}'".format(phone)
        timedata = requestData.get("timedata")
        if timedata != "" and phone != timedata:
            sqlquery = sqlquery + "and a.createTime between '{}' and '{}'".format(timedata[0],timedata[1])
        nickname = requestData.get("nickname")
        if nickname != "" and nickname != None:
            sqlquery = sqlquery + "and b.nickname like '%{}%'".format(nickname)
        status = requestData.get("status")
        if status != "" and status != None:
            sqlquery = sqlquery + "and a.status = '{}'".format(status)
        idx = requestData.get("id")
        if idx != "" and idx != None:
            sqlquery = sqlquery + "and b.id = '{}'".format(idx)
    counts = db.query("select count(*) counts from tb_user_withdrawal a join tb_user b on b.id = a.uid {};".format(sqlquery))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select a.id,DATE_FORMAT(a.createTime,'%Y-%m-%d %H:%i:%s') createTime,b.nickname,b.phone,a.money,a.`status` from tb_user_withdrawal a join tb_user b on b.id = a.uid \
            {} limit {},{};".format(sqlquery,startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/withdrawal",methods=["get"])
def get_withdrawal():
    '''
    提现统计数据
    '''
    dbres = db.query("select sum(case when `status` = 0 then money end) withdrawaling ,sum(case when `status` = 1 then money end) withdrawalend from tb_user_withdrawal;")[0]
    data = setcors(data=dbres,status=200)
    return jsonify(data)


@adminbp.route("/api/system/checkwithdrawal/<int:withId>",methods=["get"])
def do_withdrawal(withId):
    '''
    提现结算
    '''
    dbmsg = db.commit("update tb_user_withdrawal set status = '1' where id = {};".format(withId))
    data = setcors(msg=dbmsg,status=200)
    return jsonify(data)



@adminbp.route("/api/system/checkswithdrawal",methods=["post"])
def do_withdrawals():
    '''
    批量提现结算
    '''
    requestData = request.get_json()
    idlist = requestData.get("idlist")[:-1]
    sql = "update tb_user_withdrawal set status = '1' where id in ({});".format(idlist)
    dbmsg = db.commit(sql)
    data = setcors(msg=dbmsg,status=200)
    return jsonify(data)



"""
系统设置
"""
@adminbp.route("/api/system/tasktypelist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_task_type(pagenum,pagesize):
    '''
    任务类型配置表
    '''
    counts = db.query("select count(*) counts from tb_task_type where status = '1';")[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select id,tasktype,status,DATE_FORMAT(createtime,'%Y-%m-%d %H:%i:%s') createtime,DATE_FORMAT(updatetime,'%Y-%m-%d %H:%i:%s') updatetime from tb_task_type where status = '1' limit {},{};".format(startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)



@adminbp.route("/api/system/createtasktype",methods=["post"])
def create_task_type():
    '''
    新增任务类型
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    typename = requestData.get("typeName")
    if typename:
        dbmsg = db.commit("insert into tb_task_type (tasktype,uid) values ('{}',{});".format(typename,userid))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)




@adminbp.route("/api/system/updatetasktype",methods=["post"])
def update_task_type():
    '''
    修改任务类型
    '''
    requestData = request.get_json()
    idx = requestData.get("id")
    typename = requestData.get("typeName")
    dbres = db.query("select * from tb_task_type where id = {} and status = '1';".format(idx))
    if len(dbres) != 0:
        if typename and idx:
            dbmsg = db.commit("update tb_task_type set tasktype = '{}' where id = {};".format(typename,idx))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    else:
        data = setcors(msg="修改的数据不存在")
    return jsonify(data)




@adminbp.route("/api/system/deletetasktype/<int:ttid>",methods=["get"])
def delete_task_type(ttid):
    '''
    删除任务类型
    '''
    dbres = db.query("select * from tb_task_type where id = {} and status = '1';".format(ttid))
    if len(dbres) != 0:
        dbmsg = db.commit("update tb_task_type set status = '0' where id = {};".format(ttid))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="删除的数据不存在")
    return jsonify(data)




@adminbp.route("/api/system/feedbacktypelist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_feedback_type(pagenum,pagesize):
    '''
    反馈类型配置表
    '''
    counts = db.query("select count(*) counts from tb_feedback_type where status = '1';")[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select id,Feedtype,status,DATE_FORMAT(createtime,'%Y-%m-%d %H:%i:%s') createtime,DATE_FORMAT(updatetime,'%Y-%m-%d %H:%i:%s') updatetime from tb_feedback_type where status = '1' limit {},{};".format(startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)



@adminbp.route("/api/system/createfeedbacktype",methods=["post"])
def create_feedback_type():
    '''
    新增反馈类型
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    typename = requestData.get("typeName")
    if typename:
        dbmsg = db.commit("insert into tb_feedback_type (Feedtype,uid) values ('{}',{});".format(typename,userid))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)



@adminbp.route("/api/system/updatefeedbacktype",methods=["post"])
def update_feedback_type():
    '''
    修改反馈类型
    '''
    requestData = request.get_json()
    idx = requestData.get("id")
    typename = requestData.get("typeName")
    dbres = db.query("select * from tb_feedback_type where id = {} and status = '1';".format(idx))
    if len(dbres) != 0:
        if typename and idx:
            dbmsg = db.commit("update tb_feedback_type set Feedtype = '{}' where id = {};".format(typename,idx))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    else:
        data = setcors(msg="修改的数据不存在")
    return jsonify(data)



@adminbp.route("/api/system/deletefeedbacktype/<int:ttid>",methods=["get"])
def delete_feedback_type(ttid):
    '''
    删除反馈类型
    '''
    dbres = db.query("select * from tb_feedback_type where id = {} and status = '1';".format(ttid))
    if len(dbres) != 0:
        dbmsg = db.commit("update tb_feedback_type set status = '0' where id = {};".format(ttid))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="删除的数据不存在")
    return jsonify(data)



@adminbp.route("/api/system/feedbacklist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_feedback_list(pagenum,pagesize):
    '''
    反馈意见表
    '''
    counts = db.query("select count(*) counts from tb_feedback a join tb_user b on a.uid = b.id join tb_feedback_type c on c.id = a.feedtype where a.status = '1';")[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select a.id,b.nickname,b.phone,c.Feedtype,a.content,a.imglist,a.`status`,DATE_FORMAT(a.createTime,'%Y-%m-%d %H:%i:%s') createTime \
            from tb_feedback a join tb_user b on a.uid = b.id join tb_feedback_type c on c.id = a.feedtype \
            where a.status = '1' limit {},{};".format(startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)



@adminbp.route("/api/system/deletefeedback/<int:ttid>",methods=["get"])
def delete_feedback(ttid):
    '''
    删除反馈
    '''
    dbres = db.query("select * from tb_feedback where id = {} and status = '1';".format(ttid))
    if len(dbres) != 0:
        dbmsg = db.commit("update tb_feedback set status = '0' where id = {};".format(ttid))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="删除的数据不存在")
    return jsonify(data)


@adminbp.route("/api/system/getconfig",methods=["get"])
def get_system_config():
    '''
    获取系统任务设置
    '''
    dbres = db.query("select * from tb_system_config;")[0]
    data = setcors(data=dbres,status=200)
    return jsonify(data)


@adminbp.route("/api/system/config",methods=["post"])
def set_system_config():
    '''
    修改系统任务设置
    '''
    requestData = request.get_json()
    withdrawalInterval = requestData.get("withdrawalInterval")
    moneyMinimum = requestData.get("moneyMinimum")
    taskProfitratio = requestData.get("taskProfitratio")
    if withdrawalInterval and moneyMinimum and taskProfitratio:
        dbmsg = db.commit("update tb_system_config set withdrawalInterval = '{}',moneyMinimum = '{}',taskProfitratio = '{}' where id = 1;".format(withdrawalInterval,moneyMinimum,taskProfitratio))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)


@adminbp.route("/api/system/applist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_appVersion_list(pagenum,pagesize):
    '''
    APP版本管理表
    '''
    counts = db.query("select count(*) counts from tb_app_edition;")[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select id,type,vsersion,downurl,remark,DATE_FORMAT(createTime,'%Y-%m-%d %H:%i:%s') createTime,DATE_FORMAT(updateTime,'%Y-%m-%d %H:%i:%s') updateTime from tb_app_edition limit {},{};".format(startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/getexplain",methods=["get"])
def get_system_explain():
    '''
    获取系统说明
    '''
    dbres = db.query("select * from tb_system_explain;")
    data = setcors(data=dbres,status=200)
    return jsonify(data)


@adminbp.route("/api/system/setexplain1",methods=["post"])
def set_system_explain1():
    '''
    修改服务协议
    '''
    requestData = request.get_json()
    title = requestData.get("title")
    content = requestData.get("content")
    dbmsg = db.commit("update tb_system_explain set title = '{}',content = '{}' where id = 1;".format(title,content))
    data = setcors(msg=dbmsg,status=200)
    return jsonify(data)


@adminbp.route("/api/system/setexplain2",methods=["post"])
def set_system_explain2():
    '''
    修改隐私协议
    '''
    requestData = request.get_json()
    title = requestData.get("title")
    content = requestData.get("content")
    dbmsg = db.commit("update tb_system_explain set title = '{}',content = '{}' where id = 2;".format(title,content))
    data = setcors(msg=dbmsg,status=200)
    return jsonify(data)


@adminbp.route("/api/system/setexplain3",methods=["post"])
def set_system_explain3():
    '''
    修改关于我们
    '''
    requestData = request.get_json()
    content = requestData.get("content")
    dbmsg = db.commit("update tb_system_explain set content = '{}' where id = 3;".format(content))
    data = setcors(msg=dbmsg,status=200)
    return jsonify(data)



"""
权限管理
"""

@adminbp.route("/api/system/systemuser/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_admin_list(pagenum,pagesize):
    '''
    管理员表
    '''
    counts = db.query("select count(*) counts from tb_system_user;")[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select id,username,nickname,phone,headimg,status,DATE_FORMAT(create_time,'%Y-%m-%d %H:%i:%s') create_time from tb_system_user limit {},{};".format(startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@adminbp.route("/api/system/newadmin",methods=["post"])
def createadmininfo():
    '''
    新增管理员
    '''
    requestData = request.get_json()
    nickname = requestData.get("nickname")
    username = requestData.get("username")
    dbres = db.query("select * from tb_system_user  where username = '{}';".format(username))
    if len(dbres) != 0:
        data = setcors(msg="用户已存在")
    else:
        if nickname and username:
            sql = "insert into tb_system_user (username,password,nickname) values ('{}','123456','{}');".format(username,nickname)
            dbmsg = db.commit(sql)
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    return jsonify(data)


@adminbp.route("/api/system/updateadmininfo/<int:userid>",methods=["post"])
def updateadmininfo(userid):
    '''
    修改管理员信息
    '''
    requestData = request.get_json()
    nickname = requestData.get("nickname")
    headimg = requestData.get("headimg")
    dbres = db.query("select * from tb_system_user where id = {};".format(userid))
    if len(dbres) != 1:
        data = setcors(msg="用户不存在")
    else:
        if nickname and headimg:
            dbmsg = db.commit("update tb_system_user set nickname = '{}',headimg = '{}' where id = {};".format(nickname,headimg,userid))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    return jsonify(data)


@adminbp.route("/api/system/updateadminstatus/<int:userid>",methods=["post"])
def updateadminstatus(userid):
    '''
    修改管理员状态
    '''
    requestData = request.get_json()
    status = requestData.get("status")
    dbres = db.query("select * from tb_system_user where id = {};".format(userid))
    if len(dbres) != 1:
        data = setcors(msg="用户不存在")
    else:
        if status in (0,'0'):
            dbmsg = db.commit("update tb_system_user set status = '0' where id = {};".format(userid))
            data = setcors(msg=dbmsg,status=200)
        elif status in (1,'1'):
            dbmsg = db.commit("update tb_system_user set status = '1' where id = {};".format(userid))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="参数不能为空")
    return jsonify(data)