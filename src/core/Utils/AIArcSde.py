# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIArcSde
# Description : sde空间数据库操作类
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
import arcpy
import logging
from core.Utils.AICommon import AICommon

class AIArcSde(object):
    '''
    sde空间数据库操作类，包括数据库连接、操作等
    '''
    __sdeOutFolder = None # sde连接文件所在目录
    __sdeOutName = None #sde文件名称   
    __sdeOutFullName = None #sde文件全路径名称
    __logger = logging.getLogger("aigis.core.Utils.AIArcSde")#日志

    def __init__(self, sdeOutFolder, sdeOutName):
        '''
         构造器
        '''
        self.__sdeOutFolder = sdeOutFolder
        self.__sdeOutName = sdeOutName
    
    def connect(self, instance, username, password, \
                databasePlatform = 'ORACLE', accountAuthentication='DATABASE_AUTH'):
        '''
         连接数据库， 返回sde全路径
        '''
        if AICommon.IsEmpty(self.__sdeOutFolder) or AICommon.IsEmpty(self.__sdeOutName):
            return None
        if not self.__sdeOutName.endswith('.sde'):
            self.__sdeOutName += '.sde'
        self.__sdeOutFolder = self.__sdeOutFolder.replace('\\', '/')
        self.__sdeOutFullName = os.path.join(self.__sdeOutFolder, self.__sdeOutName).replace('\\', '/')
        if not os.path.exists(self.__sdeOutFullName):
            try:
                arcpy.CreateDatabaseConnection_management(self.__sdeOutFolder,
                                                          self.__sdeOutName,
                                                          databasePlatform,
                                                          instance,
                                                          accountAuthentication,
                                                          username,
                                                          password)
                
                self.__logger.info('创建ArcSDE连接文件成功，文件名为' + self.__sdeOutName)
            except:
                self.__sdeOutFullName = None
                self.__logger.exception('创建ArcSDE连接文件失败，文件名为' + self.__sdeOutName)
        return self.__sdeOutFullName
    
    def execute(self, sql_statement):
        '''
        执行sql语句
        '''
        sde_return = None
        if self.__sdeOutFullName:
            sde_conn = arcpy.ArcSDESQLExecute(self.__sdeOutFullName)
            try:
                sde_return = sde_conn.execute(sql_statement)
                if isinstance(sde_return, list):
                    return {'count' : len(sde_return), 'records' : sde_return}
            except:
                self.__logger.exception('执行SQL语句出错')
            finally:
                del sde_conn
        return sde_return
    
if __name__ == '__main__':
    pass
    
    
    
    
    
        