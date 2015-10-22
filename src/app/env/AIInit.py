# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIInit
# Description : 应用初始化
# project : GIS
# author : zhoufl
# create date :2015年10月20日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------

import os
import logging.config
import ConfigParser
from core.Utils.AIArcSde import AIArcSde
from core.Utils.AIArcServer import AIArcServer
from core.Utils.AICommon import AICommon
from core.Utils.AIConstant import AIConstant


if __name__ == '__main__':   
    ret = {'errorCode' : 0, 'rootPath' : None, 'sdeInfos' : [], 'agsInfos' : []}
    cf = None
    # 操作根目录
#     rootPath = sys.argv[1]
    # 测试环境
    rootPath = 'E:\\Code\\workspace\\mygis\\src\\app'
    if AICommon.IsEmpty(rootPath) or not os.path.isdir(rootPath):
        ret.errorCode = -1
    else:
        # 保存根目录
        AIConstant.ROOTPATH = ret['rootPath'] = rootPath 
        # 读取日志配置
        logging.config.fileConfig(os.path.join(rootPath, 'resource', 'conf', 'logging.conf'))
        logger = logging.getLogger('aigis.app.env.AIInit')
        logger.info('读取日志配置成功')
        # 建立相关连接
        cf = ConfigParser.ConfigParser()
        cf.read(os.path.join(AIConstant.ROOTPATH, 'resource', 'conf', 'config.conf'))       
        if not AICommon.IsEmpty(cf):
            # SDE连接
            sdeNames = cf.options('sde')
            for sdeName in sdeNames:                
                sdeInfo = cf.get('sde', sdeName)
                sdeInfos = sdeInfo.split('/')
                sdeInstance = sdeInfos[0]
                sdeUsername = sdeInfos[1]
                sdePassword = sdeInfos[2]
                ret['sdeInfos'].append({'instance' : sdeName, 'username' : sdeUsername, 'password' : sdePassword})
                aiArcSde = AIArcSde(os.path.join(AIConstant.ROOTPATH, 'common', 'sde') ,sdeName)
                aiArcSde.connect(sdeInstance, sdeUsername, sdePassword)
            AIConstant.SDEINFOS =  ret['sdeInfos'] 

            # AGS连接
            agsNames = cf.options('ags')
            for agsName in agsNames:
                agsInfo = cf.get('ags', agsName)
                agsInfos = agsInfo.split('/')
                serverName = agsInfos[0]
                serverPort = agsInfos[1]
                username = agsInfos[2]
                password = agsInfos[3]
                ret['agsInfos'].append({'serverName' : serverName, 'serverPort' : serverPort, 'username' : username, 'password' : password});
                aiArcSde = AIArcServer(os.path.join(AIConstant.ROOTPATH, 'common', 'ags') ,agsName)
                aiArcSde.connect(serverName, serverPort, username, password)       
            AIConstant.AGSINFOS =  ret['agsInfos'] 
    print ret
