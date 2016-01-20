# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIFc
# Description : 要素类基础类
# project : GIS
# author : zhoufl
# create date :2016年1月4日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIStrUtils import AIStrUtils
from arccore.utils.AIBean import AIBean
from arccore.store.AIFds import AIFds
from arccore.store.AIFld import AIFld

class AIFc(AIBean):
    '''
    要素类基本信息
    '''
    __name = None # 要素类名称
    __alias = None # 要素类别名
    __ftype = None # 要素类类型
    __wkid = 4326 # 参考系
    __fds = None # 所在要素集
    __fields = [] # 要素类字段
    def __init__(self, name = None, alias = None, ftype = None, wkid = 4326, fds = None, fields = []):
        '''
        构造器
        '''
        self.__name = name
        self.__alias = alias
        self.__ftype = ftype
        self.__wkid = 4326 if AIUtils.isEmpty(wkid) else wkid
        self.__fds = None if AIUtils.isEmpty(fds) else fds
        self.__fields = [] if AIUtils.isEmpty(fields) else fields
    
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
    
    def setWkid(self, wkid):
        self.__wkid = 4326 if AIUtils.isEmpty(wkid) else wkid
    
    def getWkid(self):
        return self.__wkid
    
    def setFds(self, fds):
        nfds = AIFds()
        for key in fds:
            func = getattr(nfds, 'set' + AIStrUtils.toUpperF(key))
            if AIUtils.isFunc(func):
                apply(func, [fds[key]])
                
        self.__fds = nfds
    
    def getFds(self):
        return self.__fds
    
    def setFields(self, fields):
        nflds = [] 
        if not AIUtils.isEmpty(fields) and AIUtils.isList(fields):
            for fld in fields:
                nfld = AIFld()
                for key in fld:
                    func = getattr(nfld, 'set' + AIStrUtils.toUpperF(key))
                    if AIUtils.isFunc(func):
                        apply(func, [fld[key]])
                nflds.append(nfld)
            
        self.__fields = nflds
    
    def getFields(self):
        return self.__fields
    
if __name__ == '__main__':
    
    fds = AIFds('test')
    
    flds = []
    flds.append(AIFld('objectid', '标识', 'Integer', None, 0, False))
#     flds.append(AIFld('name', '名称', 'String', None, 32, True))
#     flds.append(AIFld('shape', '几何字段', 'Geometry', None, 0, False))
#     flds.append(AIFld('area', '面积', 'Double', 6, 0, True))
       
    fc = AIFc('building', '建筑物面', 'Polygon', 4326, fds, flds)
    print fc

    attrs = str(fc)
    
#     print attrs
    
#     dic = AIUtils.str2dict(attrs)  
#     print type(dic['fields'][0]['scale'])
       
    fc2 = AIFc()
    fc2.fromStr(attrs)
    
    print fc2
#      
#     print type(fc2.getFields()[0].getLength())
#     print type(fc2.getWkid())
    
    
    
    