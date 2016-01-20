# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIAgs
# Description : ags GIS服务器连接类
# project : GIS
# author : zhoufl3
# create date :2016年1月5日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------

import os
import arcpy
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIStrUtils import AIStrUtils
from arccore.service.AISvc import AISvc
from arccore.service.AISEdit import AISEdit 

class AIAgs(object):
    '''
    GIS服务器连接类
    '''
    __agsOutFolder = None # ags连接文件所在目录
    __agsOutName = None # ags文件名称   
    __tmpOutFolder = None # 服务发布过程需要的临时文件夹
    __agsOutFullName = None # ags文件全路径名称
    __serverUrlPre = None # 服务前缀

    def __init__(self, agsOutFolder, agsOutName, tmpOutFolder, \
                 serverName, serverPort, username, password):
        '''
         构造器
        '''
        if not AIUtils.isEmpty(agsOutFolder) and not AIUtils.isEmpty(agsOutName) and not AIUtils.isEmpty(tmpOutFolder):
            self.__agsOutFolder = agsOutFolder
            self.__agsOutName = agsOutName
            self.__tmpOutFolder = tmpOutFolder
            if not self.__agsOutName.endswith('.ags'):
                self.__agsOutName += '.ags'
            server_url_part = self.__serverUrlPre = 'http://' + serverName + ':' + serverPort + '/arcgis'
            server_url = server_url_part + '/admin'
            use_arcgis_desktop_staging_folder = False
            staging_folder_path = self.__agsOutFolder
            self.__agsOutFolder = self.__agsOutFolder.replace('\\', '/')
            self.__agsOutFullName = os.path.join(self.__agsOutFolder, self.__agsOutName).replace('\\', '/')
            
            if not os.path.exists(self.__agsOutFullName):
                arcpy.mapping.CreateGISServerConnectionFile("PUBLISH_GIS_SERVICES",
                                                            self.__agsOutFolder,
                                                            self.__agsOutName,
                                                            server_url,
                                                            "ARCGIS_SERVER",
                                                            use_arcgis_desktop_staging_folder,
                                                            staging_folder_path,
                                                            username,
                                                            password,
                                                            "SAVE_USERNAME") 
                
    def publish(self, svc):
        '''
         发布服务
        '''
        if not AIUtils.isEmpty(self.__agsOutFullName) and isinstance(svc, AISvc):
            mxdFullName = svc.getMxdFullName()
            serviceName = svc.getServiceName()
            serviceFolder = svc.getServiceFolder()
            description = svc.getDescription()
            serviceItems = svc.getServiceItems()
            
            try:    
                # 生成服务草稿文件
                sddraftFullName = os.path.join(self.__tmpOutFolder, serviceName + '.sddraft')
                sdFullName = os.path.join(self.__tmpOutFolder, serviceName + '.sd')
                mapDoc = arcpy.mapping.MapDocument(mxdFullName)
                arcpy.mapping.CreateMapSDDraft(mapDoc, sddraftFullName, serviceName, 'ARCGIS_SERVER', self.__agsFullName, False, serviceFolder)
                sDDraftEditor = AISEdit(sddraftFullName)
                
                # 添加服务描述
                sDDraftEditor.setItemInfo({'description' : description})
                  
                # 添加额外服务能力
                for item in serviceItems:
                    if item.getEnabled():
                        sDDraftEditor.setSvcExtension(item.getTypeName(), 'true')
                    
                analysis = arcpy.mapping.AnalyzeForSD(sddraftFullName)
                
                if analysis['errors'] == {}:
                    # 过度服务草稿文件到SD文件
                    arcpy.StageService_server(sddraftFullName, sdFullName)
                    # 上传SD文件到GIS服务器
                    arcpy.UploadServiceDefinition_server(sdFullName, self.__agsServer)
                    
                # 发布成功存入服务地址
                for item in serviceItems:
                    if item.getEnabled():
                        typeName = item.getTypeName()
                        if AIStrUtils.isEqual(typeName, 'MapServer'):
                            svc.setUrl(self.__serverUrlPre + sDDraftEditor.getMapServerPartRestUrl())
                        elif AIStrUtils.isEqual(typeName, 'KmlServer'):
                            svc.setUrl(self.__serverUrlPre + sDDraftEditor.getKmlRestUrl())
                        elif AIStrUtils.isEqual(typeName, 'FeatureServer'):
                            svc.setUrl(self.__serverUrlPre + sDDraftEditor.getFeatureRestUrl())
                        elif AIStrUtils.isEqual(typeName, 'WFSServer'):
                            svc.setUrl(self.__serverUrlPre + sDDraftEditor.getWMSRestUrl())
                        else:
                            svc.setUrl(self.__serverUrlPre + sDDraftEditor.getWFSRestUrl())
                else: 
                    raise
            except:
                raise
            
            return svc
