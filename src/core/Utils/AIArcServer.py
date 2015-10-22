# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIArcServer
# Description : GIS服务器操作类
# project : GIS
# author : zhoufl
# create date :2015年9月19日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------

import os
import logging
import arcpy
from core.Utils.AICommon import AICommon

class AIArcServer(object):
    '''
    GIS服务操作，包括连接
    '''
    __serverOutFolder = None # server连接文件所在目录
    __serverOutName = None #server文件名称   
    __serverOutFullName = None #server文件全路径名称
    __logger = logging.getLogger("aigis.core.Utils.AIArcServer")#日志

    def __init__(self, serverOutFolder, serversdeOutName):
        '''
         构造器
        '''
        self.__serverOutFolder = serverOutFolder
        self.__serverOutName = serversdeOutName
        
    def connect(self, serverName, serverPort, username, password):
        '''
         连接GIS服务器， 返回server全路径
        '''
        if AICommon.IsEmpty(self.__serverOutFolder) or AICommon.IsEmpty(self.__serverOutName):
            return None
        
        if not self.__serverOutName.endswith('.ags'):
            self.__serverOutName += '.ags'
        server_url_part = 'http://' + serverName + ':' + serverPort + '/arcgis'
        server_url = server_url_part + '/admin'
        use_arcgis_desktop_staging_folder = False
        staging_folder_path = self.__serverOutFolder
        self.__serverOutFolder = self.__serverOutFolder.replace('\\', '/')
        self.__serverOutFullName = os.path.join(self.__serverOutFolder, self.__serverOutName).replace('\\', '/')

        if not os.path.exists(self.__serverOutFullName):
            try:
                arcpy.mapping.CreateGISServerConnectionFile("PUBLISH_GIS_SERVICES",
                                                            self.__serverOutFolder,
                                                            self.__serverOutName,
                                                            server_url,
                                                            "ARCGIS_SERVER",
                                                            use_arcgis_desktop_staging_folder,
                                                            staging_folder_path,
                                                            username,
                                                            password,
                                                            "SAVE_USERNAME")
                self.__logger.info('创建ArcServer连接文件成功，文件名为' + self.__serverOutName)
            except:
                self.__sdeOutFullName = None
                self.__logger.exception('创建ArcServer连接文件失败，文件名为' + self.__serverOutName)
        return self.__serverOutFullName
    
    
    