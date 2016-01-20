# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : queryFc
# Description : 查询要素类
# project : GIS
# author : zhoufl3
# create date :2016年1月13日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------
import sys
import os
import logging.config
import ConfigParser
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIStrUtils import AIStrUtils
from arccore.store.AIFc import AIFc
from arccore.store.AISde import AISde
from arccore.store.AIWks import AIWks
if __name__ == '__main__':
    qr = ''
    # 获取python服务端根目录
    path = sys.argv[0]
    if os.path.isfile(path):
        path = os.path.dirname(path)
    rootPath = os.path.abspath(os.path.join(path, os.pardir))
    # 读取日志配置
    logging.config.fileConfig(os.path.join(rootPath, 'resources', 'conf', 'logging.conf'))
    logger = logging.getLogger('app.scripts.queryFc')
    logger.info('读取Python服务端日志配置成功')
    # 获取参数
    param1 = sys.argv[1]
    param1 = param1.replace('null', '\'\'')
    wksDict = AIUtils.str2dict(param1)
    # 设置工作空间
    wksId = wksDict['id']
    wksType = wksDict['type']
    if AIStrUtils.isEqual(wksType, 'sde'):
        # 建立相关连接
        cf = ConfigParser.ConfigParser()
        cf.read(os.path.join(rootPath, 'resources', 'conf', 'config.conf'))     
        # 获取sde连接文件
        sdeIds = cf.options('sde')
        if wksId in sdeIds:
            sdeInfo = cf.get('sde', wksId)
            sdeInfos = sdeInfo.split('/')
            sdeServer = sdeInfos[0]
            sdeInstance = sdeInfos[1]
            sdeUsername = sdeInfos[2]
            sdePassword = sdeInfos[3]
            try:
                sde = AISde(os.path.join(rootPath, 'resources', 'sde'), wksId, sdeServer + '/' + sdeInstance, sdeUsername, sdePassword)
                sde.connect()
            except Exception as e:            
                logger.info(unicode(e.message).encode("utf-8"))
                logger.info('数据库服务器' + sdeServer + '上空间数据库' + sdeInstance + '实例连接失败') 
            logger.info('数据库服务器' + sdeServer + '上空间数据库' + sdeInstance + '实例连接成功')             
            wks = AIWks(sde.getSdeOutFullName(), sde.getSdeUserName())
            logger.info('工作空间' + sde.getSdeOutFullName() + '初始化成功')
            # 查询要素类
            param2 = sys.argv[2]
            param2 = param2.replace('null', '\'\'')
            fc = AIFc()
            fc = fc.fromStr(param2)
            try:
                fc = wks.queryFc(fc)
                qr = AIUtils.dict2json(AIUtils.str2dict(str(fc)))
                qr = '' if not qr else qr
            except Exception as e:            
                logger.info(unicode(e.message).encode("utf-8"))
                logger.info('要素类' + fc.getName() + ' 查询失败')
    print qr