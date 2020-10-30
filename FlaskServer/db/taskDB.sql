/*
Navicat MySQL Data Transfer

Source Server         : 本地数据库
Source Server Version : 50724
Source Host           : localhost:3306
Source Database       : taskdb

Target Server Type    : MYSQL
Target Server Version : 50724
File Encoding         : 65001

Date: 2020-10-26 18:30:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tb_app_edition
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_edition`;
CREATE TABLE `tb_app_edition` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '类型：0安卓1IOS',
  `vsersion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '版本号',
  `downurl` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '下载地址',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='APP版本管理表';

-- ----------------------------
-- Records of tb_app_edition
-- ----------------------------
INSERT INTO `tb_app_edition` VALUES ('1', '0', 'V1.0.1', 'https://www.baidu.com', null, '2020-10-09 13:10:37', '2020-10-09 13:10:37');

-- ----------------------------
-- Table structure for tb_feedback
-- ----------------------------
DROP TABLE IF EXISTS `tb_feedback`;
CREATE TABLE `tb_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uid` int(11) NOT NULL COMMENT '反馈用户ID',
  `feedtype` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '反馈类型ID',
  `content` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '反馈内容',
  `imglist` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '图片集',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '1' COMMENT '状态：0删除，1正常',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='意见反馈表';

-- ----------------------------
-- Records of tb_feedback
-- ----------------------------

-- ----------------------------
-- Table structure for tb_feedback_type
-- ----------------------------
DROP TABLE IF EXISTS `tb_feedback_type`;
CREATE TABLE `tb_feedback_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `Feedtype` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '反馈类型',
  `uid` int(11) NOT NULL COMMENT '添加人ID',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '1' COMMENT '状态：0删除 1OK',
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='意见反馈类型配置表';

-- ----------------------------
-- Records of tb_feedback_type
-- ----------------------------
INSERT INTO `tb_feedback_type` VALUES ('3', '使用意见2', '1', '0', '2020-09-26 17:33:22', '2020-10-22 14:10:52');
INSERT INTO `tb_feedback_type` VALUES ('4', '垃圾官方1', '1', '0', '2020-10-09 11:19:08', '2020-10-09 11:20:25');
INSERT INTO `tb_feedback_type` VALUES ('5', '354313', '1', '0', '2020-10-22 14:11:02', '2020-10-22 14:11:35');
INSERT INTO `tb_feedback_type` VALUES ('6', 'gggggg', '1', '0', '2020-10-22 14:12:32', '2020-10-22 14:12:35');
INSERT INTO `tb_feedback_type` VALUES ('7', '爱仕达大所54354131', '4', '0', '2020-10-23 16:43:20', '2020-10-23 16:44:13');
INSERT INTO `tb_feedback_type` VALUES ('8', '大的', '4', '1', '2020-10-23 16:44:31', '2020-10-23 19:47:26');
INSERT INTO `tb_feedback_type` VALUES ('9', '呵呵呵', '3', '1', '2020-10-23 19:42:27', '2020-10-23 19:42:27');
INSERT INTO `tb_feedback_type` VALUES ('10', '嗡嗡嗡', '3', '0', '2020-10-23 19:45:20', '2020-10-25 18:55:26');

-- ----------------------------
-- Table structure for tb_sms_log
-- ----------------------------
DROP TABLE IF EXISTS `tb_sms_log`;
CREATE TABLE `tb_sms_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `phone` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '电话',
  `code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '验证码',
  `content` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '短信内容',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '状态：0未验证，1已验证',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=536 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='短信验证码';

-- ----------------------------
-- Records of tb_sms_log
-- ----------------------------

-- ----------------------------
-- Table structure for tb_system_banner
-- ----------------------------
DROP TABLE IF EXISTS `tb_system_banner`;
CREATE TABLE `tb_system_banner` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '标题',
  `imghost` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '图片地址',
  `content` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '内容详情',
  `sort` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '排序',
  `linkurl` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '外链地址',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '轮播图状态：0启用，1禁用',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='轮播图表';

-- ----------------------------
-- Records of tb_system_banner
-- ----------------------------

-- ----------------------------
-- Table structure for tb_system_config
-- ----------------------------
DROP TABLE IF EXISTS `tb_system_config`;
CREATE TABLE `tb_system_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `withdrawalInterval` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '提现时间间隔分',
  `moneyMinimum` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '最低提现金额元',
  `taskProfitratio` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '任务分润比例%',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统相关配置设置表';

-- ----------------------------
-- Records of tb_system_config
-- ----------------------------
INSERT INTO `tb_system_config` VALUES ('1', '10', '1', '10', null, '2020-10-09 12:54:45', '2020-10-26 16:12:59');

-- ----------------------------
-- Table structure for tb_system_explain
-- ----------------------------
DROP TABLE IF EXISTS `tb_system_explain`;
CREATE TABLE `tb_system_explain` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '类型，0服务协议 1 隐私协议 2 关于我们',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '标题，非必填',
  `content` varchar(1000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统说明配置表';

-- ----------------------------
-- Records of tb_system_explain
-- ----------------------------
INSERT INTO `tb_system_explain` VALUES ('1', '0', '', '', null, '2020-10-09 13:18:58', '2020-10-23 19:07:40');
INSERT INTO `tb_system_explain` VALUES ('2', '1', '测试23333', '<p><img src=\"https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=4064517686,3611876511&amp;fm=26&amp;gp=0.jpg\"></p>', null, '2020-10-09 13:19:05', '2020-10-21 17:19:29');
INSERT INTO `tb_system_explain` VALUES ('3', '2', null, '<p><img src=\"https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=4064517686,3611876511&amp;fm=26&amp;gp=0.jpg\"></p>', null, '2020-10-09 13:19:12', '2020-10-21 17:19:05');

-- ----------------------------
-- Table structure for tb_system_user
-- ----------------------------
DROP TABLE IF EXISTS `tb_system_user`;
CREATE TABLE `tb_system_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '账号',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `nickname` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '昵称',
  `phone` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '电话',
  `headimg` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '1' COMMENT '账号状态：0冻结1正常',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统管理员表';

-- ----------------------------
-- Records of tb_system_user
-- ----------------------------
INSERT INTO `tb_system_user` VALUES ('1', 'admin', '123456', '超级管理员', '18202876063', '21zSdTZcTwPUy50.jpg', '1', null, '2020-09-24 17:02:50', '2020-10-26 16:10:18');
INSERT INTO `tb_system_user` VALUES ('3', 'zhangsan', '123456', '超级管理员', '18202876063', '3hUQ5D4JgFtQO1Z.jpg', '1', null, '2020-09-24 17:02:50', '2020-10-20 18:25:26');
INSERT INTO `tb_system_user` VALUES ('4', 'lisi', '123456', '超级管理员', '18202876063', '3hUQ5D4JgFtQO1Z.jpg', '1', null, '2020-09-24 17:02:50', '2020-10-20 18:25:26');
INSERT INTO `tb_system_user` VALUES ('5', 'wangwu', '123456', '超级管理员', '18202876063', '7PKbGS3egwl3b4Z.jpg', '1', null, '2020-09-24 17:02:50', '2020-10-25 14:46:48');
INSERT INTO `tb_system_user` VALUES ('6', 'chenliu', '123456', '超级管理员', '18202876063', 'GANFKNNwEjvh3vM.jpg', '1', null, '2020-09-24 17:02:50', '2020-10-25 16:22:49');
INSERT INTO `tb_system_user` VALUES ('7', 'langjin', '123456', '超级管理员', '18202876063', '3hUQ5D4JgFtQO1Z.jpg', '1', null, '2020-09-24 17:02:50', '2020-10-20 18:25:26');

-- ----------------------------
-- Table structure for tb_tasks
-- ----------------------------
DROP TABLE IF EXISTS `tb_tasks`;
CREATE TABLE `tb_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务标题',
  `content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务描述',
  `type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务类型',
  `imglist` json NOT NULL COMMENT '图片集',
  `stop_time` datetime NOT NULL COMMENT '停止时间',
  `taskmoney` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '单个任务金额',
  `tasknums` int(255) NOT NULL COMMENT '任务个数',
  `taskReceiveNum` int(11) NOT NULL DEFAULT '0' COMMENT '任务并领取个数',
  `taskallmoney` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务总金额',
  `taskProfitratio` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '系统设置的分润比例',
  `uid` int(11) NOT NULL COMMENT '创建人ID',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '任务状态，0进行中，1结束',
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建任务时间',
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=206 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务表';

-- ----------------------------
-- Records of tb_tasks
-- ----------------------------

-- ----------------------------
-- Table structure for tb_task_appeal
-- ----------------------------
DROP TABLE IF EXISTS `tb_task_appeal`;
CREATE TABLE `tb_task_appeal` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `utaskid` int(11) NOT NULL COMMENT '用户领取的任务ID',
  `uid` int(11) NOT NULL COMMENT '用户ID',
  `content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '申诉详情',
  `imglist` json NOT NULL COMMENT '图片列表',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '状态：0申诉中，1申诉通过，2申诉没通过',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务申诉表';

-- ----------------------------
-- Records of tb_task_appeal
-- ----------------------------
INSERT INTO `tb_task_appeal` VALUES ('1', '1', '1', '哈哈哈哈', '[\"lomRp2rOWDD45bz.jpg\", \"lomRp2rOWDD45bz.jpg\"]', '1', '2020-09-25 22:06:27', '2020-10-08 13:19:59');
INSERT INTO `tb_task_appeal` VALUES ('2', '18', '4', 'yeyeye', '[\"g2QljImOSOjIjDw.jpg\"]', '0', '2020-10-13 17:18:14', '2020-10-13 17:18:14');
INSERT INTO `tb_task_appeal` VALUES ('3', '60', '8', '我已经完成了，为什么不给我通过', '[\"FuVdU6ZMwimITmx.jpg\"]', '2', '2020-10-21 16:24:39', '2020-10-21 16:28:12');
INSERT INTO `tb_task_appeal` VALUES ('4', '60', '8', '不给原因吗', '[\"EbA34bJgiLqHcmi.jpg\", \"PlCJ5RwO3HSoZOb.jpg\", \"wvHQAnPJkUvbhZC.jpg\", \"friFh9lN8tDRXVc.jpg\"]', '1', '2020-10-21 16:38:39', '2020-10-21 16:39:04');

-- ----------------------------
-- Table structure for tb_task_type
-- ----------------------------
DROP TABLE IF EXISTS `tb_task_type`;
CREATE TABLE `tb_task_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `tasktype` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务类型',
  `uid` int(11) NOT NULL COMMENT '添加人ID',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '1' COMMENT '状态：0删除 1OK',
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务类型配置表';

-- ----------------------------
-- Records of tb_task_type
-- ----------------------------
INSERT INTO `tb_task_type` VALUES ('1', '点赞', '1', '1', '2020-09-24 17:03:14', '2020-09-24 17:03:14');
INSERT INTO `tb_task_type` VALUES ('2', '转发', '1', '0', '2020-09-24 17:03:21', '2020-10-22 14:12:17');
INSERT INTO `tb_task_type` VALUES ('3', '2222', '1', '0', '2020-10-09 11:01:40', '2020-10-09 11:12:27');
INSERT INTO `tb_task_type` VALUES ('4', '发微博1', '1', '0', '2020-10-21 17:29:20', '2020-10-22 14:12:13');
INSERT INTO `tb_task_type` VALUES ('5', '@@@！！', '5', '1', '2020-10-24 17:00:10', '2020-10-24 17:00:10');
INSERT INTO `tb_task_type` VALUES ('6', '123456奥术大师多asdasd@@##￥..', '5', '0', '2020-10-24 17:00:24', '2020-10-24 17:06:37');

-- ----------------------------
-- Table structure for tb_user
-- ----------------------------
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '账号',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '密码',
  `payps` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付密码',
  `nickname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '昵称',
  `phone` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '电话',
  `wxopenid` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '微信openid',
  `wxunionId` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '微信unionId',
  `headimg` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像',
  `money` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '已提现金额',
  `frozen` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '审核金额',
  `withdrawal` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '可提现金额',
  `appealerroenums` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '审核错误次数',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '1' COMMENT '账号状态：0冻结1正常2禁止发布任务',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ----------------------------
-- Records of tb_user
-- ----------------------------

-- ----------------------------
-- Table structure for tb_user_account
-- ----------------------------
DROP TABLE IF EXISTS `tb_user_account`;
CREATE TABLE `tb_user_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uid` int(11) NOT NULL COMMENT '用户ID',
  `type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '账号类型：0支付宝，1银行卡',
  `realName` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `account` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '账号或者卡号',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '状态：0正常，1删除',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户提现账号表';

-- ----------------------------
-- Records of tb_user_account
-- ----------------------------

-- ----------------------------
-- Table structure for tb_user_money
-- ----------------------------
DROP TABLE IF EXISTS `tb_user_money`;
CREATE TABLE `tb_user_money` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `utaskid` int(11) NOT NULL COMMENT '用户领取的任务ID',
  `uid` int(11) NOT NULL COMMENT '用户ID',
  `money` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务佣金',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '1' COMMENT '任务状态：0待完成，1待审核，2审核通过，3审核失败，4申诉中',
  `reamrk` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收入明细表';

-- ----------------------------
-- Records of tb_user_money
-- ----------------------------

-- ----------------------------
-- Table structure for tb_user_task
-- ----------------------------
DROP TABLE IF EXISTS `tb_user_task`;
CREATE TABLE `tb_user_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `taskid` int(11) NOT NULL COMMENT '任务ID',
  `uid` int(11) NOT NULL COMMENT '用户id',
  `imglist` json DEFAULT NULL,
  `status` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '任务状态：0待完成，1待审核，2审核通过，3审核失败，4申诉中',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户任务记录表';

-- ----------------------------
-- Records of tb_user_task
-- ----------------------------

-- ----------------------------
-- Table structure for tb_user_withdrawal
-- ----------------------------
DROP TABLE IF EXISTS `tb_user_withdrawal`;
CREATE TABLE `tb_user_withdrawal` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uid` int(11) NOT NULL COMMENT '用户ID',
  `accountid` int(11) NOT NULL COMMENT '提现账号ID',
  `money` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '提现金额',
  `status` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '状态：0未处理，1已处理',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户提现记录表';

-- ----------------------------
-- Records of tb_user_withdrawal
-- ----------------------------
