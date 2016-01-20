# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIStrUtils
# Description : 存放字符串通用方法的类
# project : GIS
# author : zhoufl3
# create date :2016年01月04日
# ---------------------------------------------------------------------------
# Modify record
# author : 
# Modify date :
# Description :
# ---------------------------------------------------------------------------
from arccore.utils.AIUtils import AIUtils

class AIStrUtils(object):
    '''
    存放字符串通用方法的类
    '''
    def __init__(self, params):
        '''
        构造器
        '''
    
    '''
    字符串是否相等
    '''
    @staticmethod 
    def isEqual(v1, v2):
        return not AIUtils.isEmpty(v1) and not AIUtils.isEmpty(v2)  and v1 == v2
    
    
    '''
    字符串转大写
    '''
    @staticmethod 
    def toUpper(v):
        return None if not AIUtils.isStr(v) else v.upper()
    
    '''
    字符串转小写
    '''
    @staticmethod 
    def toLower(v):
        return None if not AIUtils.isStr(v) else v.lower()
    
    '''
    字符串首字母转大写
    '''
    @staticmethod 
    def toUpperF(v):
        return None if not AIUtils.isStr(v) else (v[0].upper() + v[1:])
    
    '''
    字符串首字母转小写
    '''
    @staticmethod 
    def toLowerF(v):
        return None if not AIUtils.isStr(v) else (v[0].lower() + v[1:])
    
    '''
    字符串去除首尾空格
    '''
    @staticmethod 
    def trim(v):
        return None if not AIUtils.isStr(v) else v.strip()
    
if __name__ == '__main__':
    print AIUtils.dict2str({'a':1, 'b':'333', 'c': 'aaaa'})
    
    