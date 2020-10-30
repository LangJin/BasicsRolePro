# -*- coding:utf-8 -*-
__author__ = 'LangJin'

from flask import request,jsonify,g,send_from_directory
from . import userbp
from ..utils.dbtools import Db,RedisDb
from ..utils.common import setcors,checkloginstatus,pageSizeCount,strtimetotime
from config import db_config,redis_config,upload_folder
import random,string,os,time,json




db = Db(db_config)
redisdb = RedisDb(redis_config) 


@userbp.route("/api/user/logout",methods=["get"])
def logout():
    """
    推出登陆
    """
    username = g.userinfo.get("username")
    res = redisdb.delredisvalue(username)
    data = setcors(data=res,status=200,msg='退出成功')
    return jsonify(data)



@userbp.route("/api/update/userinfo",methods=["post"])
def update_user_info():
    """
    修改头像和昵称
    """
    userid = g.userinfo.get("id")
    requstsData = request.get_json()
    nickname = requstsData.get("nickname")
    headimg = requstsData.get("headimg")
    if nickname and headimg:
        dbmsg = db.commit("update tb_user set nickname='{}',headimg='{}' where id = '{}';".format(nickname,headimg,userid))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg='参数不能为空')
    return jsonify(data)


@userbp.route("/api/get/userinfo",methods=["get"])
def get_user_info():
    """
    获取头像和昵称
    """
    userid = g.userinfo.get("id")
    dbres = db.query("select nickname,headimg,money,phone,frozen,withdrawal from tb_user where id = '{}';".format(userid))
    data = setcors(data=dbres[0],status=200)
    return jsonify(data)


@userbp.route("/api/update/phone",methods=["post"])
def update_user_phone():
    """
    用户修改电话号码
    """
    userid = g.userinfo.get("id")
    requstsData = request.get_json()
    phone = requstsData.get("phone")
    code = requstsData.get("code")
    if phone and code:
        dbres = db.query("select id,code from tb_sms_log where phone = '{}' and status = '0'  and  content = 'ps' order by createTime desc limit 1;".format(phone))
        dbcode = dbres[0].get("code")
        if code == dbcode:
            dbmsg2 = db.commit("update tb_sms_log set status = '1' where id = {};".format(dbres[0].get("id")))
            dbres = db.query("select * from tb_user where phone = '{}';".format(phone))
            if len(dbres) == 0:
                dbmsg1 = db.commit("update tb_user set phone = '{}' where id = {};".format(phone,userid))
                data = setcors(msg=dbmsg1 and dbmsg2,status=200)
            else:
                data = setcors(msg="手机号已被绑定")
        else:
            data = setcors(msg="验证码不正确")
    else:
        data = setcors(msg='参数不能为空')
    return jsonify(data)


@userbp.route("/api/get/userhavepayps",methods=["get"])
def get_user_paypsstatus():
    """
    获取是否设置支付密码状态
    """
    userid = g.userinfo.get("id")
    dbres = db.query("select payps from tb_user where id = '{}';".format(userid))
    print(dbres)
    if dbres[0].get("payps") != None:
        print(dbres[0].get("payps"))
        data = setcors(data=True,status=200)
    else:
        data = setcors(data=False,status=200)
    return jsonify(data)


@userbp.route("/api/update/userfpayps",methods=["post"])
def update_user_newpayps():
    """
    设置支付密码
    """
    userid = g.userinfo.get("id")
    requstsData = request.get_json()
    newps = requstsData.get("newps")
    if newps:
        dbmsg = db.commit("update tb_user set payps='{}' where id = '{}';".format(newps,userid))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg='参数不能为空')
    return jsonify(data)


@userbp.route("/api/update/userpayps",methods=["post"])
def update_user_payps():
    """
    修改支付密码
    """
    userid = g.userinfo.get("id")
    requstsData = request.get_json()
    oldps = requstsData.get("oldps")
    newps = requstsData.get("newps")
    if oldps and newps:
        dbres = db.query("select payps from tb_user where id = {};".format(userid))
        if oldps == dbres[0].get("payps"):
            dbmsg = db.commit("update tb_user set payps='{}' where id = '{}';".format(newps,userid))
            data = setcors(msg=dbmsg,status=200)
        else:
            data = setcors(msg='支付密码不正确')
    else:
        data = setcors(msg='参数不能为空')
    return jsonify(data)


@userbp.route("/api/update/userpaypstophone",methods=["post"])
def userpaypstophone():
    """
    修改支付密码验证手机号
    """
    userid = g.userinfo.get("id")
    requstsData = request.get_json()
    phone = requstsData.get("phone")
    code = requstsData.get("code")
    if phone and code:
        if phone == g.userinfo.get("phone"):
            dbres = db.query("select id,code from tb_sms_log where phone = '{}' and status = '0'  and  content = 'payps' order by createTime desc limit 1;".format(phone))
            dbcode = dbres[0].get("code")
            if code == dbcode:
                dbmsg2 = db.commit("update tb_sms_log set status = '1' where id = {};".format(dbres[0].get("id")))
                data = setcors(msg=dbmsg2,status=200)
            else:
                data = setcors(msg="验证码不正确")
        else:
            data = setcors(msg='手机号和当前账号不匹配')
    else:
        data = setcors(msg='参数不能为空')
    return jsonify(data)


@userbp.route("/api/upload/image",methods=["post"])
def fileupload():
    '''
    上传图片接口，支持'png', 'jpg', 'jpeg', 'gif'格式。
    '''
    file = request.files["file"]
    if file and ('.' in file.filename and file.filename.rsplit('.', 1)[-1] in set(['png','png"','jpg','jpg"','jpeg','jpeg"','gif','gif"'])):
        filename = file.filename
        fname = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        if file.filename.rsplit('.', 1)[-1] in ('png"','jpg"','jpeg"','gif"'):
            filename = fname+"."+filename.split(".")[-1][:-1]
        else:
            filename = fname+"."+filename.split(".")[-1]
        uploadhost = os.path.join(os.getcwd()+upload_folder, filename)
        file.save(uploadhost)
        return setcors(data=filename,status=200)
    else:
        return setcors(msg="请上传正确的图片。")


@userbp.route("/api/get/tasktype",methods=["get"])
def get_tasktype():
    '''
    获取任务类型
    '''
    dbres = db.query("select id,tasktype from tb_task_type where status = 1;")
    data = setcors(data=dbres,status=200)
    return jsonify(data)



@userbp.route("/api/get/fackbacktype",methods=["get"])
def get_facktype():
    '''
    获取反馈类型
    '''
    dbres = db.query("select id,Feedtype feedtype from tb_feedback_type where status = 1;")
    data = setcors(data=dbres,status=200)
    return jsonify(data)


@userbp.route("/api/set/taskinfo",methods=["post"])
def set_taskinfo():
    '''
    用户发布任务
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    title = requestData.get("title")
    content= requestData.get("content")
    types= requestData.get("type")
    imglist= requestData.get("imglist")
    stop_time= requestData.get("stop_time")
    taskmoney= requestData.get("taskmoney")
    tasknums= requestData.get("tasknums")
    if int(tasknums) <= 0:
        data = setcors(msg="任务个数不得低于1个！")
        return jsonify(data)
    now = time.time()
    try:
        stopTime = int(time.mktime(time.strptime(stop_time, "%Y-%m-%d %H:%M")))
    except:
        data = setcors(msg="时间格式不正确，应该为 2020-10-29 13：30这种格式。")
        return jsonify(data)
    dbres = db.query("select status from tb_user where id = {};".format(userid))
    if dbres[0].get("status") not in  (2,'2'):
        if (title and content and types and imglist and stop_time and taskmoney and tasknums):
            if float(taskmoney) > 0 :
                if now < stopTime:
                    taskProfitratio = db.query("select * from tb_system_config;")[0].get("taskProfitratio")
                    taskallmoney= round(float(taskmoney) * int(tasknums),2)
                    taskmoney = round(float(taskmoney) * (1-float(taskProfitratio)/100),2)
                    sql = "insert into tb_tasks (title,content,type,imglist,stop_time,taskmoney,tasknums,taskallmoney,taskProfitratio,uid) \
                        values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(title,content,types,json.dumps(imglist),stop_time,taskmoney,tasknums,taskallmoney,taskProfitratio,userid)
                    dbmsg = db.commit(sql)
                    if dbmsg:
                        dbres = db.query("select id,taskallmoney from tb_tasks where uid = {} and status = '2' order by createtime desc limit 1;".format(userid))[0]
                        data = setcors(data=dbres,status=200)
                    else:
                        data = setcors(msg="发布任务失败")
                else:
                    data = setcors(msg="截至时间不能小于当前时间！")
            else:
                data = setcors(msg="任务金额不能为负数")
        else:
            data = setcors(msg="参数不能为空")
    else:
        data = setcors(msg="禁止发布任务，请联系管理员")
    return jsonify(data)


@userbp.route("/api/getuser/tasklist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_tasklist(pagenum,pagesize):
    '''
    用户任务列表
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    status = requestData.get("status")
    counts = db.query("select count(*) counts from tb_tasks where uid = '{}' and status = '{}';".format(userid,status))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        if status in (0,'0'):
            dbres = db.query("select a.id,a.title,a.content,c.nickname,b.tasktype,a.imglist,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') \
                stop_time,a.taskmoney,a.tasknums,a.taskReceiveNum,a.taskallmoney,a.uid,a.status,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') \
                createtime from tb_tasks a join tb_task_type b on b.id = a.type join tb_user c on c.id = a.uid where a.status = '0' \
                and a.uid = '{}' limit {},{};".format(userid,startnum,pagesize))
            data = {"counts":counts,"data":dbres}
            data = setcors(data=data,status=200)
        elif status in (1,'1'):
            dbres = db.query("select a.id,a.title,a.content,c.nickname,b.tasktype,a.imglist,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') \
                stop_time,a.taskmoney,a.tasknums,a.taskReceiveNum,a.taskallmoney,a.uid,a.status,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') \
                createtime from tb_tasks a join tb_task_type b on b.id = a.type join tb_user c on c.id = a.uid where a.status = '1' \
                and a.uid = '{}' limit {},{};".format(userid,startnum,pagesize))
            data = {"counts":counts,"data":dbres}
            data = setcors(data=data,status=200)
        else:
            data = setcors(msg="筛选状态不正确")
    return jsonify(data)


@userbp.route("/api/off/taskinfo",methods=["post"])
def off_taskinfo():
    '''
    用户下架任务
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    taskid = requestData.get("id")
    dbres = db.query("select taskallmoney,tasknums,taskReceiveNum from tb_tasks where id = {} and status = 0 and uid = '{}';".format(taskid,userid))
    if len(dbres) != 0:
        dbres = dbres[0]
        taskallmoney = float(dbres.get("taskallmoney"))
        tasknums = int(dbres.get("tasknums"))
        taskReceiveNum = int(dbres.get("taskReceiveNum"))
        toUserMoney = round((taskallmoney/tasknums) * (tasknums - taskReceiveNum),2)
        newTaskAllMoney = taskallmoney - toUserMoney
        dbmsg1 = db.commit("update tb_tasks set status = 1,taskallmoney = '{}',tasknums = '{}' where id = {};".format(taskid,newTaskAllMoney,taskReceiveNum))
        dbmsg2 = db.commit("update tb_user set withdrawal = withdrawal + {} where id = {};".format(toUserMoney,userid))
        data = setcors(msg=dbmsg1 and dbmsg2,status=200)
    else:
        data = setcors(msg="任务不存在")
    return jsonify(data)


@userbp.route("/api/receive/taskinfo",methods=["post"])
def receive_taskinfo():
    '''
    用户领取任务
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    taskid = requestData.get("id")
    dbres = db.query("select id,stop_time,tasknums,taskReceiveNum from tb_tasks where status = 0 and id = {};".format(taskid))
    if len(dbres) == 1:
        stopTime = str(dbres[0].get("stop_time"))
        if time.time() > strtimetotime(stopTime):
            data = setcors(msg="此任务时间已经截止，不能领取。")
        elif int(dbres[0].get("tasknums")) <= int(dbres[0].get("taskReceiveNum")):
            data = setcors(msg="此任务已经被领光了")
        else:
            dbres = db.query("select * from tb_user_task where taskid = {} and uid = {};".format(taskid,userid))
            if len(dbres) != 0:
                data = setcors(msg="任务不能重复领取")
            else:
                dbres = db.query("select tasknums,taskReceiveNum from tb_tasks where id = {};".format(taskid))[0]
                tasknums = dbres.get("tasknums")
                taskReceiveNum = dbres.get("taskReceiveNum")
                if tasknums > taskReceiveNum:
                    taskReceiveNum = taskReceiveNum + 1
                    dbmsg1 = db.commit("insert into tb_user_task (taskid,uid) values ({},{});".format(taskid,userid))
                    dbmsg2 = db.commit("update tb_tasks set taskReceiveNum = {} where id = {};".format(taskReceiveNum,taskid))
                    data = setcors(msg=dbmsg1 and dbmsg2,status=200)
                else:
                    data = setcors(msg="任务已经被领完了")
    else:
        data = setcors(msg="任务不存在")
    return jsonify(data)


@userbp.route("/api/getreceive/tasklist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_myreceive_tasklist(pagenum,pagesize):
    '''
    自己领取的任务列表
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    status = requestData.get("status")
    counts = db.query("select count(*) counts from tb_tasks a join tb_user_task b on a.id = b.taskid join tb_user c on c.id = a.uid where b.uid = '{}'  and b.status = '{}';".format(userid,status))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        if status in (0,'0'):
            dbres = db.query("select b.id,a.title,a.content,d.tasktype,a.tasknums,a.taskReceiveNum,a.taskmoney,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') \
                stop_time,c.nickname,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime,b.status \
                from tb_tasks a join tb_user_task b on a.id = b.taskid join tb_user c on c.id = a.uid \
                join tb_task_type d on d.id = a.type \
                where b.uid = '{}' and b.status = '0' limit {},{};".format(userid,startnum,pagesize))
            data = {"counts":counts,"data":dbres}
        elif status in (1,'1'):
            sql = "select b.id,a.title,a.content,d.tasktype,a.tasknums,a.taskReceiveNum,a.taskmoney,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') \
                stop_time,c.nickname,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime,b.status \
                from tb_tasks a join tb_user_task b on a.id = b.taskid join tb_user c on c.id = a.uid \
                join tb_task_type d on d.id = a.type \
                where b.uid = '{}' and b.status = '1' limit {},{};".format(userid,startnum,pagesize)
            dbres = db.query(sql)
            data = {"counts":counts,"data":dbres}
        elif status in (2,'2'):
            dbres = db.query("select b.id,a.title,a.content,d.tasktype,a.tasknums,a.taskReceiveNum,a.taskmoney,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') stop_time,c.nickname,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime,b.status \
                from tb_tasks a join tb_user_task b on a.id = b.taskid join tb_user c on c.id = a.uid \
                join tb_task_type d on d.id = a.type \
                where b.uid = '{}' and b.status in ('2','3','4') limit {},{};".format(userid,startnum,pagesize))
            data = {"counts":counts,"data":dbres}
        else:
            data = setcors(msg="筛选状态不正确")
        data = setcors(data=data,status=200)
    return jsonify(data)


@userbp.route("/api/getrelease/tasklist/<int:pagenum>/<int:pagesize>",methods=["post"])
def get_myrelease_tasklist(pagenum,pagesize):
    '''
    自己发布的的被领取的任务列表
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    status = requestData.get("status")
    if status in (0,'0'):
        counts = db.query("select count(*) counts from tb_tasks a join tb_user_task b on a.id = b.taskid \
            join tb_user c on c.id = a.uid where a.uid = '{}' and b.status = '1';".format(userid))[0].get("counts")
    elif status in (1,'1'):
        counts = db.query("select count(*) counts from tb_tasks a join tb_user_task b on a.id = b.taskid \
            join tb_user c on c.id = a.uid where a.uid = '{}' and b.status in ('3','2');".format(userid))[0].get("counts")
    else:
        counts = 0
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        if status in (0,'0'):
            sql = "select b.id,a.title,a.content,d.tasktype,a.tasknums,a.taskReceiveNum,a.taskmoney,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') \
            stop_time,c.nickname,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime,b.status,DATE_FORMAT(b.updatetime,'%Y-%m-%d %H:%i:%s') updatetime \
            from tb_tasks a join tb_user_task b on a.id = b.taskid join tb_user c on c.id = a.uid \
                join tb_task_type d on d.id = a.type \
            where a.uid = '{}' and b.status = '1' limit {},{};".format(userid,startnum,pagesize)
            dbres = db.query(sql)
            data = {"counts":counts,"data":dbres}
            data = setcors(data=data,status=200)
        elif status in (1,'1'):
            sql = "select b.id,a.title,a.content,d.tasktype,a.tasknums,a.taskReceiveNum,a.taskmoney,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') stop_time,\
            c.nickname,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime,b.status,DATE_FORMAT(b.updatetime,'%Y-%m-%d %H:%i:%s') updatetime \
            from tb_tasks a join tb_user_task b on a.id = b.taskid join tb_user c on c.id = a.uid \
                join tb_task_type d on d.id = a.type \
            where a.uid = '{}' and b.status in ('2','3') limit {},{};".format(userid,startnum,pagesize)
            dbres = db.query(sql)
            data = {"counts":counts,"data":dbres}
            data = setcors(data=data,status=200)
        else:
            data = setcors(msg="筛选状态不正确")
    return jsonify(data)


@userbp.route("/api/complete/taskinfo",methods=["post"])
def complete_taskinfo():
    '''
    用户提交任务
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    utaskid = requestData.get("id")
    imglist= requestData.get("imglist")
    remark= requestData.get("remark")
    if (utaskid and imglist and remark):
        dbres = db.query("select a.imglist,a.remark,b.taskmoney from tb_user_task a join tb_tasks b on a.taskid = b.id where a.uid = '{}' and a.id = '{}';".format(userid,utaskid))
        if len(dbres) == 1:
            if (dbres[0].get("imglist") != None and dbres[0].get("remark") != None):
                data = setcors(msg="不能重复提交任务！")
            else:
                money = dbres[0].get("taskmoney")
                dbmsg1 = db.commit("update tb_user_task set imglist = '{}',remark = '{}',status = '1' where id = {};".format(json.dumps(imglist),remark,utaskid))
                sql = "insert into tb_user_money (utaskid,uid,money) values ({},{},{});".format(utaskid,userid,money)
                dbmsg2 = db.commit(sql)
                dbres = db.query("select frozen,money,withdrawal from tb_user where id = {};".format(userid))
                dbmsg3 = db.commit("update tb_user set frozen = '{}' where id = {}".format(round(float(dbres[0].get("frozen"))+float(money),2),userid))
                data = setcors(msg=dbmsg1 and dbmsg2 and dbmsg3,status=200)
        else:
            data = setcors(msg="请先领取任务")
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)


@userbp.route("/api/examine/taskinfo",methods=["post"])
def examine_taskinfo():
    '''
    用户审核任务
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    utaskid = requestData.get("id")
    status= requestData.get("status")
    if (utaskid and status):
        dbres = db.query("select b.id,b.status from tb_tasks a join tb_user_task b on a.id = b.taskid join tb_user c on c.id = a.uid where a.uid = {} and b.id = {};".format(userid,utaskid))
        if len(dbres) == 1:
            if dbres[0].get("status") not in ("2","3",2,3):
                dbmsg1 = db.commit("update tb_user_task set status = '{}' where id = {};".format(status,utaskid))
                dbmsg2 = db.commit("update tb_user_money set status = '{}' where utaskid = {} and uid = {};".format(status,utaskid,userid))
                if status in ('2',2):  #审核通过
                    dbuserres = db.query("select frozen,money,withdrawal from tb_user where id = {};".format(userid))
                    dbmoneyres = db.query("select money from tb_user_money where utaskid = {} and uid = {};".format(utaskid,userid))
                    taskmoney = round(float(dbmoneyres[0].get("money")),2)
                    frozen = round(float(dbuserres[0].get("frozen")) - taskmoney,2)
                    withdrawal = round(float(dbuserres[0].get("withdrawal")) + taskmoney,2)
                    dbmsg3 = db.commit("update tb_user set frozen = '{}',withdrawal = '{}' where id = {}".format(frozen,withdrawal,userid))
                    data = setcors(msg=dbmsg1 and dbmsg2 and dbmsg3,status=200)
                else:  # 审核失败
                    dbuserres = db.query("select frozen,money,withdrawal from tb_user where id = {};".format(userid))
                    dbmoneyres = db.query("select money from tb_user_money where utaskid = {} and uid = {};".format(utaskid,userid))
                    taskmoney = round(float(dbmoneyres[0].get("money")),2)
                    frozen = round(float(dbuserres[0].get("frozen")) - taskmoney,2)
                    dbmsg3 = db.commit("update tb_user set frozen = '{}' where id = {}".format(frozen,userid))
                    data = setcors(msg=dbmsg1 and dbmsg2 and dbmsg3,status=200)
            else:
                data = setcors(msg="任务已审核，不能重复审核")
        else:
            data = setcors(msg="此任务不存在")
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)


@userbp.route("/api/getrelease/taskinfo/<int:utaskid>",methods=["get"])
def get_myrelease_taskinfo(utaskid):
    '''
    自己发布的的被领取的任务详情
    '''
    userid = g.userinfo.get("id")
    dbres = db.query("select b.id,a.title,a.content,a.imglist,d.tasktype,a.tasknums,a.taskReceiveNum,a.taskmoney,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') stop_time ,c.nickname,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime,b.status, \
            b.imglist uimglist,b.remark from tb_tasks a join tb_user_task b on a.id = b.taskid join tb_user c on c.id = a.uid \
                join tb_task_type d on d.id = a.type \
            where a.uid = '{}' and b.id = {};".format(userid,utaskid))
    if len(dbres) != 1:
        data = setcors(msg="任务不存在")
    else:
        data = setcors(data=dbres[0],status=200)
    return jsonify(data)


@userbp.route("/api/getreceive/taskinfo/<int:utaskid>",methods=["get"])
def get_myreceive_taskinfo(utaskid):
    '''
    自己领取的任务详情
    '''
    userid = g.userinfo.get("id")
    dbres = db.query("select b.id,a.title,a.content,d.tasktype,a.imglist,a.tasknums,b.imglist uimglist,b.remark, a.taskReceiveNum,a.taskmoney,DATE_FORMAT(a.stop_time,'%Y-%m-%d %H:%i:%s') stop_time,\
        c.nickname,DATE_FORMAT(a.createtime,'%Y-%m-%d %H:%i:%s') createtime,b.status \
        from tb_tasks a join tb_user_task b on a.id = b.taskid join tb_user c on c.id = a.uid \
        join tb_task_type d on d.id = a.type \
        where b.uid = '{}' and b.id = {};".format(userid,utaskid))
    if len(dbres) != 1:
        data = setcors(msg="任务不存在")
    else:
        data = setcors(data=dbres[0],status=200)
    return jsonify(data)


@userbp.route("/api/appeal/taskinfo",methods=["post"])
def appeal_taskinfo():
    '''
    用户提交任务申诉
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    utaskid = requestData.get("id")
    imglist= requestData.get("imglist")
    content= requestData.get("content")
    if (utaskid and imglist and content):
        dbres = db.query("select status from tb_user_task where uid = '{}' and id = '{}';".format(userid,utaskid))
        if len(dbres) == 1:
            if (dbres[0].get("status") != "3"):
                data = setcors(msg="该任务不满足申诉条件！")
            else:
                dbmsg1 = db.commit("update tb_user_task set status = '4' where id = {};".format(utaskid))
                dbmsg2 = db.commit("insert into tb_task_appeal (utaskid,uid,content,imglist) values ({},{},'{}','{}');".format(utaskid,userid,content,json.dumps(imglist)))
                data = setcors(msg=dbmsg1 and dbmsg2,status=200)
        else:
            data = setcors(msg="任务不存在")
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)



@userbp.route("/api/setmoney/account",methods=["post"])
def setmoney_account():
    '''
    用户添加提现账号
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    types = requestData.get("type")
    realName = requestData.get("realName")
    account = requestData.get("account")
    if (types and realName and account):
        dbmsg = db.commit("insert into tb_user_account (uid,type,realName,account) values ({},'{}','{}','{}');".format(userid,types,realName,account))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="参数不完整")
    return jsonify(data)


@userbp.route("/api/getmoney/account/<int:pagenum>/<int:pagesize>",methods=["post"])
def getmoney_account(pagenum,pagesize):
    '''
    用户提现账号列表
    '''
    userid = g.userinfo.get("id")
    counts = db.query("select count(*) counts from tb_user_account where uid = {} and status = '0';".format(userid))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select * from tb_user_account where uid = '{}' and status = '0' limit {},{};".format(userid,startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@userbp.route("/api/updatemoney/account",methods=["post"])
def updatemoney_account():
    '''
    用户修改提现账号
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    accountid = requestData.get("id")
    types = requestData.get("type")
    realName = requestData.get("realName")
    account = requestData.get("account")
    if (accountid and types and realName and account):
        dbmsg = db.commit("update tb_user_account set type = '{}',realName = '{}',account = '{}' where id = {} and uid = {};".format(types,realName,account,accountid,userid))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="参数不完整")
    return jsonify(data)


@userbp.route("/api/deletemoney/account",methods=["post"])
def deletemoneymoney_account():
    '''
    用户删除提现账号
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    accountid = requestData.get("id")
    if (accountid):
        dbres = db.query("select status from tb_user_account where id = {} and uid = {};".format(accountid,userid))
        if dbres[0].get("status") == 1:
            data = setcors(msg="账号已删除")
        else:
            dbmsg = db.commit("update tb_user_account set status = '1' where id = {} and uid = {};".format(accountid,userid))
            data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="参数不完整")
    return jsonify(data)


@userbp.route("/api/getmoney/tasklist/<int:pagenum>/<int:pagesize>",methods=["post"])
def getmoney_tasklist(pagenum,pagesize):
    '''
    用户收入明细
    '''
    userid = g.userinfo.get("id")
    counts = db.query("select count(*) counts from tb_user_money a  join tb_user_task b on a.utaskid = b.id join tb_tasks c on b.taskid = c.id  where a.uid = {};".format(userid))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select DATE_FORMAT(a.updateTime,'%Y-%m-%d') updateTime,a.money,c.title,c.type,b.id,a.status from tb_user_money a  \
            join tb_user_task b on a.utaskid = b.id join tb_tasks c on b.taskid = c.id  \
            where a.status in ('1','2') and a.uid  = '{}' limit {},{};".format(userid,startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@userbp.route("/api/withdrawal/money",methods=["post"])
def withdrawal_money():
    '''
    用户发起提现
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    money = requestData.get("money")
    accountid= requestData.get("accountid")
    if (money and accountid):
        dbres = db.query("select * from tb_system_config;")
        moneyMinimum = dbres[0].get("moneyMinimum")
        withdrawalInterval = dbres[0].get("withdrawalInterval")
        if float(money) >= float(moneyMinimum):
            dbresTime = db.query("select createTime from tb_user_withdrawal where uid = '{}' order by createTime desc limit 1;".format(userid))
            if len(dbresTime) == 0 or (len(dbresTime) > 0 and (time.time() - strtimetotime(str(dbresTime[0].get("createTime"))) > float(withdrawalInterval)*60)):
                dbuserres = db.query("select frozen,money,withdrawal from tb_user where id = {};".format(userid))
                withdrawal = float(dbuserres[0].get("withdrawal"))
                usermoney = float(dbuserres[0].get("money"))
                if float(money) <= withdrawal:
                    dbmsg1 = db.commit("insert into tb_user_withdrawal (uid,accountid,money) values ({},{},'{}');".format(userid,accountid,money))
                    withdrawal = round(withdrawal - float(money),2)
                    usermoney = round(usermoney + float(money),2)
                    dbmsg2 = db.commit("update tb_user set money = '{}',withdrawal = '{}' where id = {};".format(usermoney,withdrawal,userid))
                    data = setcors(msg=dbmsg1 and dbmsg2,status=200)
                else:
                    data = setcors(msg="提现金额不能大于可提现金额")
            else:
                data = setcors(msg="提现时间间隔不能小于{}分钟".format(withdrawalInterval))
        else:
            data = setcors(msg="提现金额不能小于{}元".format(moneyMinimum))
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)


@userbp.route("/api/getmoney/moneylist/<int:pagenum>/<int:pagesize>",methods=["post"])
def getmoney_moneylist(pagenum,pagesize):
    '''
    用户提现记录明细
    '''
    userid = g.userinfo.get("id")
    counts = db.query("select count(*) counts from tb_user_withdrawal where uid = {};".format(userid))[0].get("counts")
    startnum = pageSizeCount(counts,pagesize,pagenum)
    if type(startnum) != int:
        data = setcors(msg=startnum)
    else:
        dbres = db.query("select id,uid,money,DATE_FORMAT(updateTime,'%Y-%m-%d') updateTime from tb_user_withdrawal where uid  = '{}' limit {},{};".format(userid,startnum,pagesize))
        data = {"counts":counts,"data":dbres}
        data = setcors(data=data,status=200)
    return jsonify(data)


@userbp.route("/api/set/feedback",methods=["post"])
def set_feedback():
    '''
    用户意见反馈
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    feedtype = requestData.get("type")
    content= requestData.get("content")
    imglist= requestData.get("imglist")
    if (content and feedtype and imglist):
        dbmsg = db.commit("insert into tb_feedback (uid,feedtype,content,imglist) values ({},'{}','{}','{}');".format(userid,feedtype,content,json.dumps(imglist)))
        data = setcors(msg=dbmsg,status=200)
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)


@userbp.route("/api/get/explain/<int:extype>",methods=["get"])
def get_app_explain(extype):
    '''
    获取那三个说明
    '''
    dbres = db.query("select * from tb_system_explain where type = '{}';".format(extype))[0]
    data = setcors(data=dbres,status=200)
    return jsonify(data)


@userbp.route("/api/get/appversion",methods=["post"])
def get_app_version():
    '''
    获取APP版本号
    '''
    requestData = request.get_json()
    apptype = requestData.get("type")
    dbres = db.query("select * from tb_app_edition where type = '{}' order by createTime desc limit 1;".format(apptype))[0]
    data = setcors(data=dbres,status=200)
    return jsonify(data)


@userbp.route("/api/pay/yue",methods=["post"])
def yuepay():
    '''
    余额支付
    '''
    userid = g.userinfo.get("id")
    requestData = request.get_json()
    taskid = requestData.get("id")
    paymoney = requestData.get("paymoney")
    payps = requestData.get("payps")
    if taskid and paymoney and payps:
        dbres = db.query("select payps,withdrawal from tb_user where id = {};".format(userid))[0]
        if payps == dbres.get("payps"):
            if float(paymoney) <= float(dbres.get("withdrawal")):
                withdrawal = round(float(dbres.get("withdrawal")) - float(paymoney),2)
                dbmsg1 = db.commit("update tb_user set withdrawal = '{}' where id = {};".format(withdrawal,userid))
                dbmsg2 = db.commit("update tb_tasks set status = '0' where id = {};".format(taskid))
                data = setcors(msg=dbmsg1 and dbmsg2,status=200)
            else:
                data = setcors(msg="余额不足，请使用其他支付方式")
        else:
            data = setcors(msg="支付密码错误")
    else:
        data = setcors(msg="参数不能为空")
    return jsonify(data)