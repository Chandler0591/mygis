# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AISvc
# Description : 地图服务基础类
# project : GIS
# author : zhoufl3
# create date :2016年1月5日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------
from arccore.service.AISvcItem import AISvcItem

class AISvc(object):
    '''
    地图服务基本信息
    '''
    __mxdFullName = None # mxd全路径
    __serviceName = None # 服务名称
    __serviceFolder = None # 服务所在文件夹
    __description = None # 服务描述
    __serviceItems = [] # 服务项

    def __init__(self, mxdFullName, serviceName, serviceFolder, description):
        '''
        构造器
        '''   
        self.__mxdFullName = mxdFullName
        self.__serviceName = serviceName
        self.__serviceFolder = serviceFolder
        self.__description = description
        # 初始化服务项
        self.__serviceItems.append(AISvcItem('MapServer', True, None, None, None))
        self.__serviceItems.append(AISvcItem('KmlServer', False, None, None, None))
        self.__serviceItems.append(AISvcItem('FeatureServer', False, None, None, None))
        self.__serviceItems.append(AISvcItem('WFSServer', False, None, None, None))
        self.__serviceItems.append(AISvcItem('WCSServer', False, None, None, None))
    
    def setMxdFullName(self, mxdFullName):
        self.__mxdFullName = mxdFullName
    
    def getMxdFullName(self):
        return self.__mxdFullName
    
    def setServiceName(self, serviceName):
        self.__serviceName = serviceName
    
    def getServiceName(self):
        return self.__serviceName
    
    def setServiceFolder(self, serviceFolder):
        self.__serviceFolder = serviceFolder
    
    def getServiceFolder(self):
        return self.__serviceFolder
    
    def setDescription(self, description):
        self.__description = description
    
    def getDescription(self):
        return self.__description
    
    def getServiceItems(self):
        return self.__serviceItems
    
if __name__ == '__main__':
    pass