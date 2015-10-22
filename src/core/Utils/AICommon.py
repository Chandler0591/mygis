# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AICommon
# Description : 存放通用方法的类
# project : GIS
# author : zhoufl
# create date :2015年10月20日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------
class AICommon(object):
    '''
    存放通用方法的类
    '''


    def __init__(self, params):
        '''
        构造器
        '''
    
    '''
    字符串是否为空
    '''
    @staticmethod 
    def IsEmpty(sti):
        return sti is None or sti == ''
    
    
        