# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIArcSvc
# Description : Arc服务管理类
# project : GIS
# author : zhoufl
# create date :2015年10月20日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------

import arcpy
import os
import logging
import time
from core.Utils.AISDDraftEditor import AISDDraftEditor
from core.Utils.AIConstant import AIConstant
from core.Utils.AICommon import AICommon

class AIArcSvc(object):
    '''
    地图服务的发布
    '''
    __sdeFullName = None
    __agsFullName = None
    __mxdFullName = None
    __serviceName = None
    __logger = logging.getLogger("aigis.core.Service.AIArcSvc") # 日志

    def __init__(self, agsName):
        '''
        构造器
        '''   
        # AGS连接信息
        self.__agsFullName = os.path.join(AIConstant.ROOTPATH, 'common', 'ags', agsName)
        if not os.path.exists(self.__agsFullName):
            self.__agsFullName = None
            return
        
    def __setWorkSpace(self, sdeName):
        '''
        设置数据源工作空间
        '''
        # SDE工作空间
        self.__sdeFullName = os.path.join(AIConstant.ROOTPATH, 'common', 'sde', sdeName)
        if not os.path.exists(self.__sdeFullName):
            self.__sdeFullName = None
            return
        arcpy.env.workspace = self.__sdeFullName
        
    def __setAgs(self, agsName):
        '''
        设置GIS服务地址
        '''
        # AGS连接信息
        self.__agsFullName = os.path.join(AIConstant.ROOTPATH, 'common', 'ags', agsName)
        if not os.path.exists(self.__agsFullName):
            self.__agsFullName = None
            return
    
    def __createMxd(self, featureList):
        '''
        创建MXD文档，添加自定义图层
        '''
        try:
            blankMxdPath = os.path.join(AIConstant.ROOTPATH, 'common', 'mxd', 'Blank.mxd')
            if os.path.exists(blankMxdPath):
                # 新建MXD文档
                blankMapDoc = arcpy.mapping.MapDocument(blankMxdPath)
                mxdName = self.__serviceName
                self.__mxdFullName = os.path.join(AIConstant.ROOTPATH, 'common', 'mxd', mxdName + ".mxd")
                if os.path.exists(self.__serverOutFullName):
                    self.__logger.info('发布的服务名已经存在')
                    return
                
                blankMapDoc.saveACopy(self.__mxdFullName)
                
                # 打开文档添加工作空间图层
                mapDoc = arcpy.mapping.MapDocument(self.__mxdFullName)
                df = arcpy.mapping.ListDataFrames(mapDoc, "*")[0]
                for featureClass in featureList:
                    name = featureClass['name']
                    maxScale = 0.0 if not 'maxScale' in featureClass.keys() else featureClass['maxScale']
                    minScale = 0.0 if not 'minScale' in featureClass.keys() else featureClass['minScale']
                    transparency = 0 if not 'transparency' in featureClass.keys() else featureClass['transparency']
                    visible = True if not 'visible' in featureClass.keys() else featureClass['visible']
                    lyr = arcpy.mapping.Layer(name)
                    
                    # 设置图层属性
                    lyr.maxScale = maxScale
                    lyr.minScale = minScale
                    lyr.transparency = transparency
                    lyr.visible = visible
                    
                    arcpy.mapping.AddLayer(df, lyr, "BOTTOM")
                    
                mapDoc.save()
        except:
            self.__logger.exception('地图服务数据加载失败')
            
    
    def publishService(self, options):
        '''
        依据用户需求发布服务
        '''
        agsName = None if 'agsName' not in options.keys() else options['agsName']
        srcData = None if 'srcData' not in options.keys() else options['srcData']
        serviceName = None if 'srcData' not in options.keys() else options['serviceName']
        serviceFolder = None if 'serviceFolder' not in options.keys() else options['serviceFolder']
        capabilities = None if 'capabilities' not in options.keys() else options['capabilities']
        summary = None if 'summary' not in options.keys() else options['summary']
        tags = None if 'tags' not in options.keys() else options['tags']
        description = None if 'description' not in options.keys() else options['description']
        sdeName = None
        featureList = []
        
        # 必要参数为空返回
        if srcData is None or serviceName is None:
            return
        self.__serviceName = serviceName
        
        # 解析发布服务数据源
        if srcData:
            sdeName = None if 'sdeName' not in srcData.keys() else options['sdeName']
            featureList = None if 'featureList' not in srcData.keys() else options['featureList']
            if sdeName is None or featureList is None or not isinstance(featureList, list):
                return
            if not sdeName.endswith('.sde'):
                sdeName += '.sde'
            self.__setWorkSpace(sdeName)
            # 创建MXD文件，添加图层数据 
            self.__createMxd(featureList)
            
        if agsName:
            if not self.agsName.endswith('.ags'):
                agsName += '.ags'
            self.__setAgs(agsName)
        try:    
            # 生成服务草稿文件
            sddraftFullName = os.path.join(AIConstant.ROOTPATH, 'common', 'mxd', 'svc', serviceName + '.sddraft')
            sdFullName = os.path.join(AIConstant.ROOTPATH, 'common', 'mxd', 'svc', serviceName + '.sd')
            mapDoc = arcpy.mapping.MapDocument(self.__mxdFullName)
            arcpy.mapping.CreateMapSDDraft(mapDoc, sddraftFullName, serviceName, 'ARCGIS_SERVER', self.__agsFullName, False, serviceFolder, summary, tags)
            sDDraftEditor = AISDDraftEditor(sddraftFullName)
            sDDraftEditor.setItemInfo({'description' : description}) # 添加服务描述
            #print sDDraftEditor.getItemInfo()
              
            # 添加GIS扩展服务能力
            for extention in capabilities:
                sDDraftEditor.setSvcExtension(extention, 'true')
                
            analysis = arcpy.mapping.AnalyzeForSD(sddraftFullName)
            
            if analysis['errors'] == {}:
                # 备份服务草稿文件
                sddraftFullNameBack = os.path.join(AIConstant.ROOTPATH, 'common', 'mxd', 'svc', self.__serviceName + '_back' + '.sddraft') 
                f = open(sddraftFullNameBack, 'w')
                sddraftDoc = sDDraftEditor.getSddraftDoc()
                sddraftDoc.writexml(f)
                f.close()
                
                # 过度服务草稿文件到SD文件
                arcpy.StageService_server(sddraftFullName, sdFullName)
                # 上传SD文件到GIS服务器
                arcpy.UploadServiceDefinition_server(sdFullName, self.__agsServer)
                self.__logger.info('服务发布成功')
                
#               print server_url_part + sDDraftEditor.getMapServerPartRestUrl()
            else: 
                self.__logger.info('服务发布失败')
                self.__logger.info(analysis['errors'])
            
#                     if analysis['messages']:
#                         print analysis['messages']
#                     
#                     if analysis['warnings']:
#                         print analysis['warnings']
        except:
            self.__logger.exception('服务发布失败')
            

if __name__ == '__main__':
#     arcpy.env.workspace = 'D:/tmp/82.sde'
#     for ds in arcpy.ListDatasets():
#         des = arcpy.Describe(ds)
#         print des.name
#     sde_conn = arcpy.ArcSDESQLExecute('D:/tmp/82.sde')
#     sde_return = sde_conn.execute("SELECT LAT,LNG FROM WATER_DETECT")  
#     print sde_return
    svcConfig = { 'gisTmpDir' : 'D:\\tmp',\
                  'serverName' : '172.17.212.82',\
                  'serverPort' : '6080',\
                  'username' : 'siteadmin',\
                  'password' : '123'
                }
    arcSvc = AIArcSvc(svcConfig)
    svcOptions = { 'workSpace' : 'D:/tmp/82.sde',\
                   'featureList': [{'name' : 'AIR_DETECT', 'maxScale' : 1000, 'minScale' : 2000000, 'transparency' : 50},
                                   {'name' : 'WATER_DETECT', 'minScale' : 0, 'visible' : False},
                                   {'name' : 'DISTRICT_AREA', 'minScale' : 2000000, 'transparency' : 80}],\
                   'serviceName' : 'fm2025', \
                   'serviceFolder' : 'yaxin', \
                   'capabilities' : ['WMSServer', 'WFSServer'],\
                   'description' : '服务'}
    #['AIR_DETECT', 'WATER_DETECT', 'DISTRICT_AREA']
    #fz,water,air
    # 'FeatureServer', 
    #                    'summary' : '123',\
#                    'tags' : '',\
    arcSvc.publishService(svcOptions)