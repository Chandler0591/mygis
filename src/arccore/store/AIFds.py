# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIFds
# Description : 要素集基础类
# project : GIS
# author : zhoufl3
# create date :2016年1月4日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIBean import AIBean

class AIFds(AIBean):
    '''
    要素集基本信息
    '''
    __name = None # 要素集名称
    __wkid = 4326 # 参考系
    def __init__(self, name = None, wkid = 4326):
        '''
        构造器
        '''
        self.__name = name
        self.__wkid = 4326 if AIUtils.isEmpty(wkid) else wkid
        
    def setName(self, name):
        self.__name = name
    
    def getName(self):
        return self.__name
    
    def setWkid(self, wkid):
        self.__wkid = 4326 if AIUtils.isEmpty(wkid) else wkid
    
    def getWkid(self):
        return self.__wkid
    
if __name__ == '__main__':
#     fd = AIFds('test', 3857)
#     print fd
# 
#     attrs = str(fd)
#     fd2 = AIFds()
#     fd2 = fd2.fromStr(attrs)
#     print fd2
    pass 