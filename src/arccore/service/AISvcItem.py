# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AISvcItem
# Description : 地图服务项
# project : GIS
# author : zhoufl3
# create date :2016年1月6日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------

class AISvcItem(object):
    '''
    地图服务项基本信息
    '''
    __typeName = None # 服务类型
    __enabled = None # 是否启用
    __url = None # 服务rest地址
#     __capabilities = [] # 服务能力
#     __properties = {} # 服务属性

    def __init__(self, typeName, enabled, url):
        '''
        构造器
        '''   
        self.__typeName = typeName
        self.__enabled = enabled
        self.__url = url
    
    def setTypeName(self, typeName):
        self.__typeName = typeName
    
    def getTypeName(self):
        return self.__typeName
    
    def setEnabled(self, enabled):
        self.__enabled = enabled
    
    def getEnabled(self):
        return self.__enabled
    
    def setUrl(self, url):
        self.__url = url
    
    def getUrl(self):
        return self.__url
    
#     def setCapabilities(self, capabilities):
#         self.__capabilities = capabilities
#     
#     def getCapabilities(self):
#         return self.__capabilities
#     
#     def setProperties(self, properties):
#         self.__properties = properties
#     
#     def getProperties(self):
#         return self.__properties
    
if __name__ == '__main__':
    pass