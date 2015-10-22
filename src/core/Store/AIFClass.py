# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIFClass
# Description : 要素类
# project : GIS
# author : zhoufl
# create date :2015年8月19日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------

from core.Utils.AIArcSde import *
import arcpy

class AIFClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
if __name__ == '__main__':
    sde = AIArcSde('D:/tmp', '82')
    sdeOutFullName = None
    sdeOutFullName = sde.connect("172.17.212.82/orcl", "gis", "123")
    if sdeOutFullName:
        print sdeOutFullName
        arcpy.env.workspace = sdeOutFullName
        for ds in arcpy.ListDatasets():
            des = arcpy.Describe(ds)
            print des.name
        result = sde.execute("SELECT COUNT(*) FROM WATER_DETECT")
        print result    