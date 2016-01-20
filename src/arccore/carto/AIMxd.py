# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIMxd
# Description : MXD工程管理类
# project : GIS
# author : zhoufl3
# create date :2016年1月5日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------

import arcpy
import os
import time
from arccore.utils.AIUtils import AIUtils

class AIMxd(object):
    '''
     MXD工程类，包括新建以及添加图层
    '''
    __mxdOutFolder = None # mxd所在目录
    __mxdFullName = None  # mxd完整路径

    def __init__(self, mxdOutFolder, blankMxdPath):
        '''
         构造器
        '''
        if not AIUtils.isEmpty(mxdOutFolder) and os.path.exists(mxdOutFolder) and \
        not AIUtils.isEmpty(blankMxdPath) and os.path.exists(blankMxdPath):
            blankMapDoc = arcpy.mapping.MapDocument(blankMxdPath)
            mxdName = time.strftime("%Y%m%d%H%M%S")
            self.__mxdFullName = os.path.join(mxdOutFolder, mxdName + ".mxd").replace('\\', '/')
            blankMapDoc.saveACopy(self.__mxdFullName)
            
    
    def addLayers(self, layers):
        '''
         添加图层到工程
        '''
        if not AIUtils.isEmpty(self.__mxdFullName):
            mapDoc = arcpy.mapping.MapDocument(self.__mxdFullName)
            df = arcpy.mapping.ListDataFrames(mapDoc, "*")[0]
            for layer in layers:
                name = layer.getName()
                maxScale = layer.getMaxScale()
                minScale = layer.getMinScale()
                transparency = layer.getTransparency()
                visible = layer.getVisible()
                
                lyr = arcpy.mapping.Layer(name)
                # 设置图层属性
                lyr.name = name
                lyr.maxScale = maxScale
                lyr.minScale = minScale
                lyr.transparency = transparency
                lyr.visible = visible
                arcpy.mapping.AddLayer(df, lyr, "TOP")
                
            mapDoc.save()
    
    def convert2Msd(self):
        '''
          转化为msd文件
        ''' 
        msdFullName = None
        if not AIUtils.isEmpty(self.__mxdFullName):
            mapDoc = arcpy.mapping.MapDocument(self.__mxdFullName)
            msdFullName = os.path.join(os.path.dirname(self.__mxdFullName), os.path.basename(self.__mxdFullName).split('.')[0] + '.msd')
            try:
                arcpy.mapping.ConvertToMSD(mapDoc, msdFullName, None, 'BEST', 'FORCE')
            except:
                msdFullName = None
                raise
        return msdFullName
    
    def setMxdFullName(self, mxdFullName):
        '''
         设置工程全路径
        '''
        self.__mxdFullName = mxdFullName
    
    def getMxdFullName(self):
        '''
         获取工程全路径
        '''
        return self.__mxdFullName 
    
if __name__ == '__main__':
#     sde = AISde('D:\\tmp\\sde', 'orcl21', '192.168.0.21/arcgis', 'gis', 'gis123')
#     sdeOutFullName = sde.connect()
#     print sdeOutFullName
#     if not AIUtils.isEmpty(sdeOutFullName):
#         wks = AIWks(sdeOutFullName, 'gis')
#         mxd = AIMxd('D:/tmp/mxd', 'D:/tmp/mxd/blank.mxd')
#         lyrs = []
#         lyrs.append(AILayer('fuzhou', 0, 0, 0))
#         lyrs.append(AILayer('ILCGIS.乡镇', 0, 1000000, 0.5))
#         mxd.addLayers(lyrs)
#         print mxd.getMxdFullName()
    mxd = AIMxd('D:/tmp/mxd', 'D:/tmp/mxd/blank.mxd')
    mxd.setMxdFullName(r'D:\GitHome\mygis\src\app\resources\mxd\20160118151958.mxd')
    print mxd.convert2Msd()
        
        
        