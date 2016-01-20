# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : removeFc
# Description : 移除要素类
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
import arcpy
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIStrUtils import AIStrUtils
if __name__ == '__main__':
    flag = 'false'
    # 获取python服务端根目录
    path = sys.argv[0]
    if os.path.isfile(path):
        path = os.path.dirname(path)
    rootPath = os.path.abspath(os.path.join(path, os.pardir))
    # 读取日志配置
    logging.config.fileConfig(os.path.join(rootPath, 'resources', 'conf', 'logging.conf'))
    logger = logging.getLogger('app.scripts.removeFc')
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
            
            # 默认文件已经存在
            sdeOutFullName = os.path.join(rootPath, 'resources', 'sde', wksId + ".sde").replace('\\', '/')
            # 设置当前工作空间
            arcpy.env.workspace = sdeOutFullName
            logger.info('工作空间' + sdeOutFullName + '初始化成功')
            # 新增要素类
            param2 = sys.argv[2]
            param2 = param2.replace('null', '\'\'')
            param2 = param2.replace('true', 'True')
            param2 = param2.replace('false', 'False')
            fcDict = AIUtils.str2dict(param2)
            keys = fcDict.keys()
            fcName = None if 'name' not in keys else fcDict['name']
            fcAlias = None if 'alias' not in keys else fcDict['alias']
            fcFtype = None if 'ftype' not in keys else fcDict['ftype']
            fcWkid = None if 'wkid' not in keys else fcDict['wkid']
            fcFds = None if 'fds' not in keys else fcDict['fds']
            fcFields = None if 'fields' not in keys else fcDict['fields']
            
            try:
                if not AIUtils.isEmpty(fcName):
                    arcpy.Delete_management(fcName)
                    flag = 'true'
            except Exception as e:            
                logger.info(unicode(e.message).encode("utf-8"))
                logger.info('要素类' + fcName + '删除失败') 
    print flag