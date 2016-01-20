# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AISEdit
# Description : 服务草稿文件编辑类
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
import xml.dom.minidom as DOM  
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIStrUtils import AIStrUtils

class AISEdit(object):
    '''
    服务草稿文件编辑类
    '''
    __sddraftFullName = None # 服务草稿文件全路径
    __sddraftDoc = None # 服务草稿文件文档

    def __init__(self, sddraftFullName):
        '''
        构造器
        '''
        if sddraftFullName:
            try:
                self.__sddraftFullName = sddraftFullName.replace('\\', '/')
                self.__sddraftDoc = DOM.parse(self.__sddraftFullName)
            except:
                raise
    
    def getSddraftDoc(self):
        '''
         获取服务草稿文件文档
        '''
        return self.__sddraftDoc
        
    def __overrideSddraft(self):
        '''
         覆盖已存在的服务草稿文件
        '''
        if os.path.exists(self.__sddraftFullName):
            os.remove(self.__sddraftFullName)
            
            f = open(self.__sddraftFullName, 'w')
            self.__sddraftDoc.writexml(f)
            f.close()
    
    def setSvcExtension(self, svcType, svcState):
        '''
        设置服务类型是否可用
        '''
        if(self.__sddraftDoc):
            extensions = self.__sddraftDoc.getElementsByTagName('Extensions')[0]
            extensionSets = extensions.childNodes
            find = False
            for extensionSet in extensionSets:
                if find:
                    break
                keyValues = extensionSet.childNodes
                for keyValue in keyValues:
                    if keyValue.tagName == 'TypeName':
                        if keyValue.firstChild.data == svcType:
                            skeyValues = keyValue.parentNode.childNodes
                            for skeyValue in skeyValues:
                                if skeyValue.tagName == 'Enabled':
                                    skeyValue.firstChild.data = svcState
                                    # 覆盖服务草稿文件
                                    self.__overrideSddraft()
                                    find = True
                                    break
                                
    def getSvcExtension(self, svcType):
        '''
        获取服务类型是否可用
        '''
        if(self.__sddraftDoc):
            extensions = self.__sddraftDoc.getElementsByTagName('Extensions')[0]
            extensionSets = extensions.childNodes
            for extensionSet in extensionSets:
                keyValues = extensionSet.childNodes
                for keyValue in keyValues:
                    if keyValue.tagName == 'TypeName':
                        if keyValue.firstChild.data == svcType:
                            skeyValues = keyValue.parentNode.childNodes
                            for skeyValue in skeyValues:
                                if skeyValue.tagName == 'Enabled':
                                    return skeyValue.firstChild.data
    
    def setServiceName(self, serviceName):
        '''
        设置服务名
        '''
        if(self.__sddraftDoc):
            svcConfiguration = self.__sddraftDoc.getElementsByTagName('SVCConfiguration')[0]
            keyValues = svcConfiguration.childNodes
            for keyValue in keyValues:
                if keyValue.tagName == 'Name':
                    if keyValue.firstChild.firstChild:
                        keyValue.firstChild.firstChild.data = serviceName
                    else:
                        keyValue.firstChild.appendChild(self.__sddraftDoc.createTextNode(serviceName))
                    # 覆盖服务草稿文件
                    self.__overrideSddraft()
    
    def getServiceName(self):
        '''
        获取服务名
        '''
        if(self.__sddraftDoc):
            svcConfiguration = self.__sddraftDoc.getElementsByTagName('SVCConfiguration')[0]
            keyValues = svcConfiguration.childNodes
            for keyValue in keyValues:
                if keyValue.tagName == 'Name':
                    return keyValue.firstChild.data
                                
    def setServiceFolder(self, serviceFolder):
        '''
        设置服务文件夹
        '''
        if(self.__sddraftDoc):
            sf = self.__sddraftDoc.getElementsByTagName('ServiceFolder')[0]
            # 改变服务文件夹
            if sf.firstChild.firstChild:
                sf.firstChild.firstChild.data = serviceFolder
            else:
                sf.firstChild.appendChild(self.__sddraftDoc.createTextNode(serviceFolder))
            # 覆盖服务草稿文件
            self.__overrideSddraft()
    
    def getServiceFolder(self):
        '''
        获取服务文件夹
        '''
        if(self.__sddraftDoc):
            sf = self.__sddraftDoc.getElementsByTagName('ServiceFolder')[0]
            return None if not sf.firstChild else sf.firstChild.data
    
    def setMaxRecordCount(self, maxRecordCount):
        '''
        设置服务返回最大记录数
        '''
        if(self.__sddraftDoc):
            configProps = self.__sddraftDoc.getElementsByTagName('ConfigurationProperties')[0]
            propArray = configProps.firstChild
            propSets = propArray.childNodes
            find = False
            for propSet in propSets:
                if find:
                    break
                keyValues = propSet.childNodes
                for keyValue in keyValues:
                    if keyValue.tagName == 'Key':
                        if keyValue.firstChild.data == 'maxRecordCount':
                            # 设置记录数
                            keyValue.nextSibling.firstChild.data = maxRecordCount
                            # 覆盖服务草稿文件
                            self.__overrideSddraft()
                            find = True
                            break
                            
            # 覆盖服务草稿文件
            self.__overrideSddraft()
    
    def getMaxRecordCount(self):
        '''
        获取服务返回最大记录数
        '''
        if(self.__sddraftDoc):
            configProps = self.__sddraftDoc.getElementsByTagName('ConfigurationProperties')[0]
            propArray = configProps.firstChild
            propSets = propArray.childNodes
            for propSet in propSets:
                keyValues = propSet.childNodes
                for keyValue in keyValues:
                    if keyValue.tagName == 'Key':
                        if keyValue.firstChild.data == 'maxRecordCount':
                            # 返回记录数
                            return keyValue.nextSibling.firstChild.data
    
    def setReplaceExist(self, replaceExist):
        '''
        设置是否替换已经存在服务
        '''
        if(self.__sddraftDoc):
            tagsType = self.__sddraftDoc.getElementsByTagName('Type')
            for tagType in tagsType:
                if tagType.parentNode.tagName == 'SVCManifest':
                    if tagType.hasChildNodes():
                        tagType.firstChild.data = "esriServiceDefinitionType_Replacement"
                        break
                        
            tagsState = self.__sddraftDoc.getElementsByTagName('State')
            for tagState in tagsState:
                if tagState.parentNode.tagName == 'SVCManifest':
                    if tagState.hasChildNodes():
                        tagState.firstChild.data = 'esriSDState_Published'
                        break
            
            # 覆盖服务草稿文件
            self.__overrideSddraft()
            
    def getReplaceExist(self):
        '''
        获取是否替换已经存在服务
        '''
        if(self.__sddraftDoc):
            serviceDefinitionType = sDState = None
            tagsType = self.__sddraftDoc.getElementsByTagName('Type')
            for tagType in tagsType:
                if tagType.parentNode.tagName == 'SVCManifest':
                    if tagType.hasChildNodes():
                        serviceDefinitionType = tagType.firstChild.data
                            
            tagsState = self.__sddraftDoc.getElementsByTagName('State')
            for tagState in tagsState:
                if tagState.parentNode.tagName == 'SVCManifest':
                    if tagState.hasChildNodes():
                        sDState = tagState.firstChild.data
            
            return 'esriServiceDefinitionType_Replacement' == serviceDefinitionType and 'esriSDState_Published' == sDState
    
    def setItemInfo(self, itemInfo):
        '''
         设置服务描述
        '''
        summary = None if 'summary' not in itemInfo.keys() else itemInfo['summary'] 
        tags =  None if 'tags' not in itemInfo.keys() else itemInfo['tags']
        description = None if 'description' not in itemInfo.keys() else itemInfo['description']
        
        if(self.__sddraftDoc):
            itemInfo = self.__sddraftDoc.getElementsByTagName('ItemInfo')[0]
            keyValues = itemInfo.childNodes
            for keyValue in keyValues:
                if keyValue.tagName == 'Tags':
                    if tags:
                        if keyValue.firstChild:
                            tagss = tags.split(',')
                            for tag in tagss:
                                keyValue.firstChild.appendChild(self.__sddraftDoc.createTextNode(tag))
                            
                if keyValue.tagName == 'Description':
                    if description:
                        if keyValue.firstChild:
                            keyValue.firstChild.data = description
                        else:
                            keyValue.appendChild(self.__sddraftDoc.createTextNode(description))
                if keyValue.tagName == 'Snippet':
                    if summary:
                        if keyValue.firstChild:
                            keyValue.firstChild.data = summary
                        else:
                            keyValue.appendChild(self.__sddraftDoc.createTextNode(summary))
                    
            svcConfiguration = self.__sddraftDoc.getElementsByTagName('SVCConfiguration')[0]
            keyValues = svcConfiguration.childNodes
            for keyValue in keyValues:
                if keyValue.tagName == 'Definition':
                    if description:
                        if keyValue.firstChild.firstChild:
                            keyValue.firstChild.firstChild.data = description
                        else:
                            keyValue.firstChild.appendChild(self.__sddraftDoc.createTextNode(description))
            
            # 覆盖服务草稿文件
            self.__overrideSddraft()
                        
    def getItemInfo(self):
        '''
         获取服务描述
        '''
        if(self.__sddraftDoc):
            summary = None
            tags =  None
            description = None
            itemInfo = self.__sddraftDoc.getElementsByTagName('ItemInfo')[0]
            keyValues = itemInfo.childNodes
            for keyValue in keyValues:
                if keyValue.tagName == 'Tags':
                    tagsKeyValues = keyValue.childNodes
                    tags = ','.join([tagsKeyValue.firstChild.data for tagsKeyValue in tagsKeyValues]) if tagsKeyValues else None
                if keyValue.tagName == 'Description':
                    description = None if not keyValue.firstChild else keyValue.firstChild.data
                if keyValue.tagName == 'Snippet':
                    summary = None if not keyValue.firstChild else keyValue.firstChild.data
    
            return {'summary':summary, 'tags':tags, 'description':description}
    
    def getMapRestUrl(self):
        '''
         获取局部地图服务Rest地址
        '''
        return '/rest/services/' + '' if AIUtils.isEmpty(self.getServiceFolder()) else (self.getServiceFolder() + '/') + (self.getServiceName() + '/MapServer')
    
    def getKmlRestUrl(self):
        '''
         获取局部Kml服务Rest地址
        '''
        return '/rest/services/' + '' if AIUtils.isEmpty(self.getServiceFolder()) else (self.getServiceFolder() + '/') + (self.getServiceName() + '/MapServer/KmlServer')
    
    def getFeatureRestUrl(self):
        '''
         获取局部要素服务Rest地址
        '''
        if self.getSvcExtension('FeatureServer'):
            return '/rest/services/' + '' if AIUtils.isEmpty(self.getServiceFolder()) else (self.getServiceFolder() + '/') + (self.getServiceName() + '/FeatureServer')
    
    def getWMSRestUrl(self):
        '''
         获取局部WMS服务Rest地址
        '''
        if self.getSvcExtension('WMSServer'):
            return '/rest/services/' + '' if AIUtils.isEmpty(self.getServiceFolder()) else (self.getServiceFolder() + '/') + (self.getServiceName() + '/MapServer/WMSServer')
    
    def getWFSRestUrl(self):
        '''
         获取局部WFS服务Rest地址
        '''
        if self.getSvcExtension('WFSServer'):
            return '/rest/services/' + '' if AIUtils.isEmpty(self.getServiceFolder()) else (self.getServiceFolder() + '/') + (self.getServiceName() + '/MapServer/WFSServer')
        
if __name__ == '__main__':
    pass
    