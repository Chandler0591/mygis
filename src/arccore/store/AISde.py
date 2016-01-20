# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AISde
# Description : sde空间数据库操作类
# project : GIS
# author : zhoufl3
# create date :2015年10月20日
# ---------------------------------------------------------------------------
# Modify record
# author : zhoufl3
# Modify date :2016年01月04日
# Description :
# ---------------------------------------------------------------------------

import os
import arcpy
from arccore.utils.AIUtils import AIUtils

class AISde(object):
    '''
    sde空间数据库操作类，包括数据库连接、操作等
    '''
    __sdeOutFolder = None # sde连接文件所在目录
    __sdeOutName = None # sde文件名称   
    __sdeOutFullName = None # sde文件全名
    __sdeUserName = None # sde连接用户名

    def __init__(self, sdeOutFolder, sdeOutName, instance, username, password, \
                databasePlatform = 'ORACLE', accountAuthentication='DATABASE_AUTH'):
        '''
         构造器
        '''
        if not AIUtils.isEmpty(sdeOutFolder) and not AIUtils.isEmpty(sdeOutName):
            self.__sdeOutFolder = sdeOutFolder
            self.__sdeOutName = sdeOutName
            if not self.__sdeOutName.endswith('.sde'):
                self.__sdeOutName += '.sde'
            self.__sdeOutFolder = self.__sdeOutFolder.replace('\\', '/')
            self.__sdeOutFullName = os.path.join(self.__sdeOutFolder, self.__sdeOutName).replace('\\', '/')
            self.__sdeUserName = username
            if not os.path.exists(self.__sdeOutFullName):
                arcpy.CreateDatabaseConnection_management(self.__sdeOutFolder,
                                                          self.__sdeOutName,
                                                          databasePlatform,
                                                          instance,
                                                          accountAuthentication,
                                                          username,
                                                          password)
        
    def connect(self):
        '''
         尝试连接数据库，  成功返回sde全路径
        '''
        connResult = None
        if not AIUtils.isEmpty(self.__sdeOutFullName):
            try:        
#                 sde_return = self.execute('select 1 from dual')
#                 if not AIUtils.isEmpty(sde_return):
#                     connResult = self.__sdeOutFullName
                connResult = self.__sdeOutFullName
            except:
                raise
#             except Exception as e:
#                 print 'failure, connect error'             
#                 print unicode(e.message).encode("utf-8") 
            
        return connResult
    
    def execute(self, sql):
        '''
        执行sql语句
        '''
        sde_conn = None
        sde_return = None
        try:
            sde_conn = None if AIUtils.isEmpty(self.__sdeOutFullName) else arcpy.ArcSDESQLExecute(self.__sdeOutFullName)
            if not AIUtils.isEmpty(sde_conn):
                try:
                    sde_return = sde_conn.execute(sql)
                except:
                    raise
        except:
            raise
        finally:
            del sde_conn
        
        return sde_return
    
    def getSdeOutFullName(self):
        return self.__sdeOutFullName
    
    def getSdeUserName(self):
        return self.__sdeUserName
    
if __name__ == '__main__':
    try:
        sde = AISde('D:\\tmp\\sde', 'orcl21', '192.168.0.21/arcgis', 'gis', 'gis123')
        sdeOutFullName = sde.connect()
        print sdeOutFullName
        sql = "SELECT {0},{1} FROM ent_4326 where objectid < {2}".format('code', 'name', 10200)
        result = sde.execute(sql)
        print [rec[1].encode('utf-8','ignore') for rec in result]
    except Exception as e:            
        print unicode(e.message).encode("utf-8") 
    
    
    
        