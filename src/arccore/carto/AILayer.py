# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AILayer
# Description : 工程图层类
# project : GIS
# author : zhoufl3
# create date :2016年1月5日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIBean import AIBean

class AILayer(AIBean):
    '''
    图层基本信息
    '''
    __name = None # 名称
    __maxScale = 0 # 显示最大比例尺
    __minScale = 0 # 显示最小比例尺
    __transparency = 0 # 透明度0-1
    __visible = True # 是否可见
#     __showLabels = False # 是否显示标注
#     __labelClasses = [] # 标注列表
    
    def __init__(self, name = None, minScale = 0, maxScale = 0, transparency = 0, visible = True):
        '''
        构造器
        '''
        self.__name = name  
        self.__minScale = 0 if AIUtils.isEmpty(minScale) else minScale
        self.__maxScale = 0 if AIUtils.isEmpty(maxScale) else maxScale
        self.__transparency = 0 if AIUtils.isEmpty(transparency) else transparency
        self.__visible = True if AIUtils.isEmpty(visible) else visible
#         self.__showLabels = showLabels
#         self.__labelClasses = labelClasses
    
    def setName(self, name):
        self.__name = name
    
    def getName(self):
        return self.__name
    
    def setMinScale(self, minScale):
        self.__minScale = 0 if AIUtils.isEmpty(minScale) else minScale
    
    def getMinScale(self):
        return self.__minScale
    
    def setMaxScale(self, maxScale):
        self.__maxScale = 0 if AIUtils.isEmpty(maxScale) else maxScale
    
    def getMaxScale(self):
        return self.__maxScale
    
    def setTransparency(self, transparency):
        self.__transparency = 0 if AIUtils.isEmpty(transparency) else transparency
    
    def getTransparency(self):
        return self.__transparency
    
    def setVisible(self, visible):
        self.__visible = True if AIUtils.isEmpty(visible) else visible
    
    def getVisible(self):
        return self.__visible
    
#     def setShowLabels(self, showLabels):
#         self.__showLabels = showLabels
#     
#     def getShowLabels(self):
#         return self.__showLabels
#     
#     def setLabelClasses(self, labelClasses):
#         self.__labelClasses = labelClasses
#     
#     def getLabelClasses(self):
#         return self.__labelClasses
    
if __name__ == '__main__':
    lyr = AILayer('building', 1000, 50000, 0.5)
    print lyr

    attrs = str(lyr)
    lyr2 = AILayer()
    lyr2 = lyr2.fromStr(attrs)
    print type(lyr2.getMinScale())
    pass