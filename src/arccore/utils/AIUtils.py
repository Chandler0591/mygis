# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIUtils
# Description : 存放通用方法的类
# project : GIS
# author : zhoufl3
# create date :2015年10月20日
# ---------------------------------------------------------------------------
# Modify record
# author : zhoufl3
# Modify date :2016年01月04日
# Description :
# ---------------------------------------------------------------------------
import string
import json
class AIUtils(object):
    '''
    存放通用方法的类
    '''
    def __init__(self, params):
        '''
        构造器
        '''
    
        '''
    变量是否为空
    '''
    @staticmethod 
    def isEmpty(v):
        return v is None or v == ''
    
    '''
    判断是否为字符串
    '''
    @staticmethod 
    def isStr(v):
        return isinstance(v, str)
    
    '''
    判断是否布尔型
    '''
    @staticmethod 
    def isBool(v):
        return not AIUtils.isEmpty(v) and isinstance(v, bool)
    
    '''
    判断是否整型
    '''
    @staticmethod 
    def isInt(v):
        return not AIUtils.isEmpty(v) and isinstance(v, int)
    
    '''
    判断是否浮点型
    '''
    @staticmethod 
    def isFloat(v):
        return not AIUtils.isEmpty(v) and isinstance(v, float)
    
    '''
    判断是否数字
    '''
    @staticmethod 
    def isNumber(v):
        return not AIUtils.isEmpty(v) and isinstance(v, int) or isinstance(v, float)
    
    '''
    判断是否列表
    '''
    @staticmethod 
    def isList(v):
        return not AIUtils.isEmpty(v) and isinstance(v, list)
    
    '''
    判断是否元组
    '''
    @staticmethod 
    def isTuple(v):
        return not AIUtils.isEmpty(v) and isinstance(v, tuple)
    '''
    判断是否字典
    '''
    @staticmethod 
    def isDict(v):
        return not AIUtils.isEmpty(v) and isinstance(v, dict)
        '''
    判断是否函数
    '''
    @staticmethod 
    def isFunc(v):
        return not AIUtils.isEmpty(v) and callable(v)
    
    '''
    字符串转数字
    '''
    @staticmethod 
    def toNumber(v):
        return v if AIUtils.isNumber(v) else 0 if not AIUtils.isStr(v) else string.atof(v)
    
    '''
    字符串转整数
    '''
    @staticmethod 
    def toInt(v):
        return v if AIUtils.isInt(v) else 0 if not AIUtils.isStr(v) else string.atoi(v)
    
    '''
    字符串转布尔
    '''
    @staticmethod 
    def toBool(v):
        return v if AIUtils.isBool(v) else False if AIUtils.isStr(v) and v.upper() == 'FALSE'  else True
    
    '''
    转字符串
    '''
    @staticmethod
    def toStr(v):
        return '' if AIUtils.isEmpty(v) else str(v)
    
    '''
    字符串转数组
    '''
    @staticmethod
    def str2list(v):
        return None if not AIUtils.isStr(v) else eval(v)
    
    '''
    数组转字符串
    '''
    @staticmethod
    def list2str(v):
        result = None
        if not AIUtils.isList(v):
            return result
        result = [AIUtils.toStr(item) for item in v]
        result = '[' + ','.join(result) + ']'
        
        return result  
    
    '''
    字符串转字典
    '''
    @staticmethod
    def str2dict(v):
        return None if not AIUtils.isStr(v) else eval(v)
    
    '''
    字典转字符串
    '''
    @staticmethod
    def dict2str(v):
        result = None
        if not AIUtils.isDict(v):
            return result
        result = ['\'%s\':\'%s\'' % (key, AIUtils.toStr(v[key])) for key in v.keys()]
        result = '{' + ','.join(result) + '}'
        
        return result 
    
    '''
    json转字典
    '''
    @staticmethod
    def json2dict(v):
        return None if not AIUtils.isStr(v) else json.loads(v)
    
    '''
    字典转json
    '''
    @staticmethod
    def dict2json(v):
        return None if not AIUtils.isDict(v) else json.dumps(v)
    
    '''
    json转字典
    '''
    @staticmethod
    def json2list(v):
        return None if not AIUtils.isStr(v) else json.loads(v)
    
    '''
    字典转json
    '''
    @staticmethod
    def list2json(v):
        return None if not AIUtils.isList(v) else json.dumps(v)
    
    '''
    unicode转utf-8
    '''
    @staticmethod
    def unicode2utf8(v):
        return unicode(v).encode('utf8')
    
    '''
    utf-8转unicode
    '''
    @staticmethod
    def utf82unicode(v):
        return None if not AIUtils.isStr(v) else v.decode('utf8')
    
if __name__ == '__main__':
    pass
    param1 = '{"id":"arcgis21","type":123}'
    param1 = param1.replace('null', '\'\'')
    wksDict = AIUtils.str2dict(param1)
    print wksDict
    jsn = AIUtils.dict2json(wksDict)
    print jsn
#     
#     param2 = '{"name":"test","wkid":null}'
#     param2 = param2.replace('null', '\'\'')
#     fdsDict = AIUtils.str2dict(param2)
#     print fdsDict   