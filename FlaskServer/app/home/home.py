# -*- coding:utf-8 -*-
__author__ = 'LangJin'

from flask import request,jsonify,g,send_from_directory,render_template
from . import appbp
from ..utils.dbtools import Db,RedisDb
from ..utils.common import setcors,checkloginstatus,pageSizeCount
from ..utils.tcc import SendTxSms
from config import db_config,redis_config,upload_folder
import random,string,os,time


db = Db(db_config)


@appbp.route("/apidocs",methods=["get"])
def apidocs():
    return render_template("接口文档.html")



@appbp.route('/api/get/image/<string:imgname>',methods=["get"])
def get_image_file(imgname):
    '''
    读取图片接口
    '''
    return send_from_directory(os.getcwd()+upload_folder,imgname)


@appbp.route('/api/get/bannerlist',methods=["get"])
def get_banner_list():
    '''
    轮播图列表
    '''
    dbres = db.query("select imghost,linkurl from tb_system_banner where status = '0' order by sort;")
    data = setcors(data=dbres,status=200)
    return jsonify(data)



@appbp.route("/api/get/tasklist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_tasklist(pagenum,pagesize):
    '''
    任务列表
    '''
    requestData = request.get_json()
    if requestData != None:
        sorttype = requestData.get("sorttype")
    else:
        sorttype = None
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    print(now)
    counts = db.query("select count(*) counts from tb_tasks a join tb_user b on a.uid = b.id join tb_task_type c on a.type = c.id where a.status = 0 and a.taskReceiveNum < a.tasknums and a.stop_time > '{}';".format(now))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        if sorttype == "time":
            dbres = db.query("select a.id,a.title,a.content,c.nickname,b.tasktype,a.imglist,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') \
                stop_time,a.taskmoney,a.tasknums,a.taskReceiveNum,a.taskallmoney,a.uid,a.status,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') \
                    createtime from tb_tasks a join tb_task_type b on b.id = a.type join tb_user c on c.id = a.uid where a.status = 0 and a.taskReceiveNum < a.tasknums and a.stop_time > '{}'\
                    order by stop_time desc limit {},{};".format(now,startnum,pagesize))
            data = {"counts":counts,"data":dbres}
            data = setcors(data=data,status=200)
        elif sorttype == "money":
            dbres = db.query("select a.id,a.title,a.content,c.nickname,b.tasktype,a.imglist,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') \
                stop_time,a.taskmoney,a.tasknums,a.taskReceiveNum,a.taskallmoney,a.uid,a.status,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') \
                createtime from tb_tasks a join tb_task_type b on b.id = a.type join tb_user c on c.id = a.uid where a.status = 0 and a.taskReceiveNum < a.tasknums and a.stop_time > '{}'\
                order by cast(taskmoney as UNSIGNED INTEGER) desc limit {},{};".format(now,startnum,pagesize))
            data = {"counts":counts,"data":dbres}
            data = setcors(data=data,status=200)
        else:
            dbres = db.query("select a.id,a.title,a.content,c.nickname,b.tasktype,a.imglist,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') \
                stop_time,a.taskmoney,a.tasknums,a.taskReceiveNum,a.taskallmoney,a.uid,a.status,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') \
                    createtime from tb_tasks a join tb_task_type b on b.id = a.type join tb_user c on c.id = a.uid where a.status = 0 and a.taskReceiveNum < a.tasknums and a.stop_time > '{}' limit {},{};".format(now,startnum,pagesize))
            data = {"counts":counts,"data":dbres}
            data = setcors(data=data,status=200)
    return jsonify(data)



@appbp.route("/api/get/taskinfo/<int:taskid>",methods=["get"])
def get_taskinfo(taskid):
    '''
    任务详情
    '''
    dbres = db.query("select a.id,a.title,a.content,c.nickname,b.tasktype,a.imglist,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') stop_time,a.taskmoney,a.tasknums,a.taskReceiveNum,a.taskallmoney,a.uid,a.status,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime from tb_tasks a join tb_task_type b on b.id = a.type join tb_user c on c.id = a.uid where a.status = 0  and a.id = {};".format(taskid))
    if len(dbres) != 1:
        data = setcors(msg="任务不存在")
    else:
        data = setcors(data=dbres[0],status=200)
    return jsonify(data)


@appbp.route("/api/send/smscode",methods=["post"])
def send_smscode():
    '''
    发送验证码
    '''
    requestData = request.get_json()
    phone = requestData.get("phone")
    templateType = requestData.get("type")
    code = str(random.randint(100000,999999))
    if phone and templateType:
        sendMsg = SendTxSms(phone,templateType,code)
        if sendMsg.get("SendStatusSet")[0].get("Code") == "Ok":
            dbmsg = db.commit("insert into tb_sms_log (phone,code,content) values ('{}','{}','{}');".format(phone,code,templateType))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg="验证码发送失败")
    else:
        data = setcors(msg="参数不对")
    return jsonify(data)



