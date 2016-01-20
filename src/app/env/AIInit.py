# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIInit
# Description : Python服务器端应用环境初始化入口
# project : GIS
# author : zhoufl3
# create date :2016年1月7日
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
from arccore.store.AISde import AISde
# from arccore.service.AIAgs import AIAgs 

if __name__ == '__main__':
    message = 'Python服务端环境初始化失败'
    # 获取python服务端根目录
    path = sys.path[0]
    if os.path.isfile(path):
        path = os.path.dirname(path)
    rootPath = os.path.abspath(os.path.join(path, os.pardir))

    cf = None
    # 修改日志配置中日志存储位置
    cf = ConfigParser.ConfigParser()
    logCfPath = os.path.join(rootPath, 'resources', 'conf', 'logging.conf')
    cf.read(logCfPath)
    cf.set('handler_rotateFileHandler', 'args', str((os.path.join(rootPath, 'resources', 'log', 'logging.log'), 'a', 5*1024*1024, 100)))
    logCfFile = open(logCfPath ,'w')
    cf.write(logCfFile)
    logCfFile.close()
    # 读取日志配置
    logging.config.fileConfig(os.path.join(rootPath, 'resources', 'conf', 'logging.conf'))
    logger = logging.getLogger('app.env.AIInit')
    # 建立相关连接
    cf = ConfigParser.ConfigParser()
    cf.read(os.path.join(rootPath, 'resources', 'conf', 'config.conf'))     
    if not AIUtils.isEmpty(cf):
        # 生成sde连接文件
        sdeNames = cf.options('sde')
        for sdeName in sdeNames:                
            sdeInfo = cf.get('sde', sdeName)
            sdeInfos = sdeInfo.split('/')
            sdeServer = sdeInfos[0]
            sdeInstance = sdeInfos[1]
            sdeUsername = sdeInfos[2]
            sdePassword = sdeInfos[3]
            
            sde = AISde(os.path.join(rootPath, 'resources', 'sde'), sdeName, sdeServer + '/' + sdeInstance, sdeUsername, sdePassword)
            sde.connect()
            
            logger.info('数据库服务器' + sdeServer + '上空间数据库' + sdeInstance + '实例连接文件新建成功')
#             # 生成ags连接文件
#             agsNames = cf.options('ags')
#             for agsName in agsNames:
#                 agsInfo = cf.get('ags', agsName)
#                 agsInfos = agsInfo.split('/')
#                 serverName = agsInfos[0]
#                 serverPort = agsInfos[1]
#                 username = agsInfos[2]
#                 password = agsInfos[3]
# 
#                 ags = AIAgs(os.path.join(rootPath, 'app', 'resources', 'ags') ,agsName, os.path.join(rootPath, 'app', 'resources', 'tmp'), \
#                             serverName, serverPort, username, password)
#                 
#                 # 设置ags实例
#                 setattr(AIConstant, agsName, ags)
#                 logger.info('服务器' + serverName + '上GIS服务管理实例连接文件新建成功，' + '端口号为' + serverPort)
        message = 'Python服务端环境初始化成功'
        logger.info('Python服务端环境初始化成功')
            
    
    print message
