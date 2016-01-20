# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIBean
# Description : bean基类
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
from arccore.utils.AIStrUtils import AIStrUtils

class AIBean(object):
    '''
    bean基类
    '''

    def __init__(self):
        '''
        构造函数
        '''
        
    '''
    对象转字符串
    '''
    def toStr(self, obj):
        result = None
        if not AIUtils.isEmpty(obj):
            attrs = dir(obj)
            result = []
            for attr in attrs:
                if attr.startswith('get'):
                    prop = AIStrUtils.toLowerF(attr[3:])
                    func = getattr(obj, attr)
                    value = apply(func, [])
                    # 判断类型，不同的字符串转换方式
                    propValue = AIUtils.list2str(value) if AIUtils.isList(value) \
                    else AIUtils.dict2str(value) if AIUtils.isDict(value) \
                    else ('\'' + AIUtils.toStr(value) + '\'') if AIUtils.isStr(value) \
                    else AIUtils.toStr(value)
                    result.append('\'' + prop + '\':' + propValue + '')
            result = '{' + ','.join(result) + '}'
        else:
            raise Exception('input parameter type not correct!')
        
        return result
    '''
    字符串转对象
    '''
    def fromStr(self, attrs):
        obj = None
        if AIUtils.isStr(attrs):
            attrs = AIUtils.str2dict(attrs)
            obj = self
            if AIUtils.isDict(attrs):
                for key in attrs:
                    func = getattr(obj, 'set' + AIStrUtils.toUpperF(key))
                    if AIUtils.isFunc(func):
                        apply(func, [attrs[key]])
        else:
            raise Exception('input parameter type not correct!')
        
        return obj
    
    '''
    对象转字符串
    '''   
    def __str__(self):
        return self.toStr(self)
    
    