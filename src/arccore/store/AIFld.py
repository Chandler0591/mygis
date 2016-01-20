# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIFld
# Description : 要素字段基础类
# project : GIS
# author : zhoufl3
# create date :2016年1月6日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIBean import AIBean

class AIFld(AIBean):
    '''
    要素字段基本信息
    '''
    __name = None # 字段名称
    __alias = None # 字段别名
    __ftype = None # 字段类型
    __scale = 0 # 小数点精度
    __length = 0 # 长度
    __isNullable = True # 是否可为空
    def __init__(self, name = None, alias = None, ftype = None, scale = 0, length = 0, isNullable = True):
        '''
        构造器
        '''
        self.__name = name
        self.__alias = alias
        self.__ftype = ftype
        self.__scale = 0 if AIUtils.isEmpty(scale) else scale
        self.__length = 0 if AIUtils.isEmpty(length) else length
        self.__isNullable = True if AIUtils.isEmpty(isNullable) else isNullable
    
    def setName(self, name):
        self.__name = name
    
    def getName(self):
        return self.__name
    
    def setAlias(self, alias):
        self.__alias = alias
    
    def getAlias(self):
        return self.__alias
    
    def setFtype(self, ftype):
        self.__ftype = ftype
    
    def getFtype(self):
        return self.__ftype
    
    def setScale(self, scale):
        self.__scale = 0 if AIUtils.isEmpty(scale) else scale
    
    def getScale(self):
        return self.__scale
    
    def setLength(self, length):
        self.__length = 0 if AIUtils.isEmpty(length) else length
    
    def getLength(self):
        return self.__length
    
    def setIsNullable(self, isNullable):
        self.__isNullable = True if AIUtils.isEmpty(isNullable) else isNullable
    
    def getIsNullable(self):
        return self.__isNullable
    
if __name__ == '__main__':
    fld = AIFld('code', '编码', 'String ', None, 12, False)
    print fld

    attrs = str(fld)
    fld2 = AIFld()
    fld2 = fld2.fromStr(attrs)
    print fld2
    pass
    
    