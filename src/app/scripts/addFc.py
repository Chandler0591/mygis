# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : addFc
# Description : 新增要素类
# project : GIS
# author : zhoufl3
# create date :2016年1月13日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------
import sys
import os
import logging.config
import ConfigParser
import arcpy
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIStrUtils import AIStrUtils
if __name__ == '__main__':
    flag = 'false'
    # 获取python服务端根目录
    path = sys.argv[0]
    if os.path.isfile(path):
        path = os.path.dirname(path)
    rootPath = os.path.abspath(os.path.join(path, os.pardir))
    # 读取日志配置
    logging.config.fileConfig(os.path.join(rootPath, 'resources', 'conf', 'logging.conf'))
    logger = logging.getLogger('app.scripts.addFc')
    logger.info('读取Python服务端日志配置成功')
    # 获取参数
    param1 = sys.argv[1]
    param1 = param1.replace('null', '\'\'')
    wksDict = AIUtils.str2dict(param1)
    # 设置工作空间
    wksId = wksDict['id']
    wksType = wksDict['type']
    if AIStrUtils.isEqual(wksType, 'sde'):
        # 建立相关连接
        cf = ConfigParser.ConfigParser()
        cf.read(os.path.join(rootPath, 'resources', 'conf', 'config.conf'))     
        # 获取sde连接文件
        sdeIds = cf.options('sde')
        if wksId in sdeIds:
            sdeInfo = cf.get('sde', wksId)
            sdeInfos = sdeInfo.split('/')
            sdeServer = sdeInfos[0]
            sdeInstance = sdeInfos[1]
            sdeUsername = sdeInfos[2]
            sdePassword = sdeInfos[3]
            
            # 默认文件已经存在
            sdeOutFullName = os.path.join(rootPath, 'resources', 'sde', wksId + ".sde").replace('\\', '/')
            # 设置当前工作空间
            arcpy.env.workspace = sdeOutFullName
            logger.info('工作空间' + sdeOutFullName + '初始化成功')
            # 新增要素类
            param2 = sys.argv[2]
            param2 = param2.replace('null', '\'\'')
            param2 = param2.replace('true', 'True')
            param2 = param2.replace('false', 'False')
            fcDict = AIUtils.str2dict(param2)
            keys = fcDict.keys()
            fcName = None if 'name' not in keys else fcDict['name']
            fcAlias = None if 'alias' not in keys else fcDict['alias']
            fcFtype = None if 'ftype' not in keys else fcDict['ftype']
            fcWkid = None if 'wkid' not in keys else fcDict['wkid']
            fcFds = None if 'fds' not in keys else fcDict['fds']
            fcFields = None if 'fields' not in keys else fcDict['fields']
            
            try:
                if not AIUtils.isEmpty(fcName) and not AIUtils.isEmpty(fcFtype):
                    # 要素集名称
                    fdsName = None
                    if AIUtils.isDict(fcFds) and 'name' in fcFds.keys() and not AIUtils.isEmpty(fcFds['name']):
                        fdsName = fcFds['name']
                        fdsName = fdsName if ('.' in fdsName) else fdsName if AIUtils.isEmpty(sdeUsername) else (sdeUsername + '.') + fdsName
                    wksName = sdeOutFullName if AIUtils.isEmpty(fdsName) else os.path.join(sdeOutFullName, fdsName).replace('\\', '/')
                    fcWkid = 4326 if not AIUtils.isInt(fcWkid) else fcWkid
                    # 创建要素类
                    arcpy.CreateFeatureclass_management(wksName, fcName, fcFtype, None, "DISABLED", "DISABLED", arcpy.SpatialReference(fcWkid))
                    # 更改别名
                    if not AIUtils.isEmpty(fcAlias):
                        arcpy.AlterAliasName(fcName, fcAlias)
                    # 添加字段(排除保留字段)
                    if AIUtils.isList(fcFields):
                        for field in fcFields:
                            keys = field.keys()
                            fldName = AIStrUtils.toUpper(field['name'])
                            if not AIStrUtils.isEqual(fldName, 'OBJECTID') and \
                                not AIStrUtils.isEqual(fldName, 'NAME') and \
                                not AIStrUtils.isEqual(fldName, 'SHAPE') and \
                                not 'AREA' in fldName and \
                                not 'LEN' in fldName:
                                # 字段名
                                fldName = arcpy.ValidateFieldName(fldName, wksName)
                                # 字段别名
                                fldAlias = fldName if not 'alias' in keys else field['alias']
                                # 字段类型 Integer--LONG  Double--DOUBLE  String--TEXT Date--DATE
                                fldType = 'TEXT' if AIStrUtils.isEqual(AIStrUtils.toUpper(field['ftype']), 'STRING') else field['ftype']
                                # 字段小数点位数（浮点型）
                                fldScale = 0 if not 'scale' in keys else field['scale']
                                # 字段长度（文本型）
                                fldLength = 50 if not 'length' in keys else field['length']
                                # 字段是否允许为空
                                fldIsNullable = True if not 'isNullable' in keys else field['isNullable']
                                
                                arcpy.AddField_management(fcName, fldName, fldType, None, fldScale, \
                                                          fldLength, fldAlias, fldIsNullable, False)
                    flag = 'true'            
            except Exception as e:            
                logger.info(unicode(e.message).encode("utf-8"))
                logger.info('要素类' + fcName + '新增失败')
    print flag