# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIConstant
# Description : 存放常量的类
# project : GIS
# author : zhoufl
# create date :2015年9月20日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------

class _AIConstant(object):
    '''
    存放常量
    '''

    def __init__(self):
        '''
        构造函数
        '''
        
    def __setattr__(self, key, value):
        if not self.__dict__.has_key(key):
            self.__dict__[key] = value
                
    def __getattr__(self, key):
        if self.__dict__.has_key(key):
            return self.key
        else:
            return None  
    
AIConstant = _AIConstant()  