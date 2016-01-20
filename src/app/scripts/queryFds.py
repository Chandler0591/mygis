# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : queryFds
# Description : 查询要素集
# project : GIS
# author : zhoufl3
# create date :2016年1月11日
# ---------------------------------------------------------------------------
# Modify record
# author : zhoufl3
# Modify date : 2016年1月19日
# Description : 优化代码
# ---------------------------------------------------------------------------
import sys
import os
import logging.config
import ConfigParser
import arcpy
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIStrUtils import AIStrUtils
if __name__ == '__main__':
    qr = ''
    # 获取python服务端根目录
    path = sys.argv[0]
    if os.path.isfile(path):
        path = os.path.dirname(path)
    rootPath = os.path.abspath(os.path.join(path, os.pardir))
    # 读取日志配置
    logging.config.fileConfig(os.path.join(rootPath, 'resources', 'conf', 'logging.conf'))
    logger = logging.getLogger('app.scripts.queryFds')
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
            # 查询要素集
            param2 = sys.argv[2]
            param2 = param2.replace('null', '\'\'')
            param2 = param2.replace('true', 'True')
            param2 = param2.replace('false', 'False')
            fdsDict = AIUtils.str2dict(param2)
            keys = fdsDict.keys()
            fdsName = None if 'name' not in keys else fdsDict['name']
            try:
                if not AIUtils.isEmpty(fdsName):
                    fdsName = fdsName if ('.' in fdsName) else fdsName if AIUtils.isEmpty(sdeUsername) else (sdeUsername + '.') + fdsName
                    datasets = arcpy.ListDatasets(fdsName, 'Feature')
                    if len(datasets) > 0 and not AIUtils.isEmpty(datasets[0]):
                        dataset = datasets[0]
                        desc = arcpy.Describe(dataset)
                        sr = desc.spatialReference
                        qr = {'name' : AIUtils.unicode2utf8(desc.name), 'wkid' : None if AIUtils.isEmpty(sr) else sr.factoryCode}
                        qr = AIUtils.dict2json(qr)
            except Exception as e:        
                logger.info(unicode(e.message).encode("utf-8"))
                logger.info('要素集' + fdsName + '查询失败')
    print qr
    
    