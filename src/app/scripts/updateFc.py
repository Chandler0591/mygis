# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : updateFc
# Description : 更新要素类
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
    logger = logging.getLogger('app.scripts.updateFc')
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
            # 更新要素类
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
                nalias = fcAlias # 要素新别名
                nFields = fcFields # 新字段集合
                nFieldNames = None
                if AIUtils.isList(fcFields):
                    nFieldNames = [nfld['name'] for nfld in fcFields] # 新字段名集合
                if not AIUtils.isEmpty(fcName):
                    fcName = fcName if ('.' in fcName) else fcName if AIUtils.isEmpty(sdeUsername) else (sdeUsername + '.') + fcName
                    fcFtype = 'All' if AIUtils.isEmpty(fcFtype) else fcFtype
                    # 要素集名称
                    fdsName = None
                    if AIUtils.isDict(fcFds) and 'name' in fcFds.keys() and not AIUtils.isEmpty(fcFds['name']):
                        fdsName = fcFds['name']
                        fdsName = fdsName if ('.' in fdsName) else fdsName if AIUtils.isEmpty(sdeUsername) else (sdeUsername + '.') + fdsName
                    wksName = sdeOutFullName if AIUtils.isEmpty(fdsName) else os.path.join(sdeOutFullName, fdsName).replace('\\', '/')
                    
                    featureclasses = arcpy.ListFeatureClasses(fcName, fcFtype, fdsName)
                    if len(featureclasses) > 0 and not AIUtils.isEmpty(featureclasses[0]):
                        featureclass = featureclasses[0]
                        desc = arcpy.Describe(featureclass)
                            
                        oalias = AIUtils.unicode2utf8(desc.aliasName) # 要素旧别名
                        oFields = desc.fields # 旧字段集合
                        oFieldNames = None
                        if AIUtils.isList(oFields):
                            oFieldNames = [ofld.name for ofld in oFields] # 旧字段名集合
                        # 更改别名
                        if not AIUtils.isEmpty(nalias) and not AIStrUtils.isEqual(oalias, nalias):
                            arcpy.AlterAliasName(fcName, nalias)
                        # 比对字段
                        if AIUtils.isList(oFieldNames) and AIUtils.isList(nFieldNames):
                            # 删除字段(排除保留字段)
                            for ofn in oFieldNames:
                                if ofn not in nFieldNames and \
                                not AIStrUtils.isEqual(ofn, 'OBJECTID') and \
                                not AIStrUtils.isEqual(ofn, 'NAME') and \
                                not AIStrUtils.isEqual(ofn, 'SHAPE') and \
                                not 'AREA' in ofn and \
                                not 'LEN' in ofn:
                                    arcpy.DeleteField_management(fcName, ofn)
                                    
                            # 添加字段(排除保留字段)
                            for nfn in nFieldNames:
                                if nfn not in oFieldNames:
                                    fldName = AIStrUtils.toUpper(nfn)
                                    if not AIStrUtils.isEqual(fldName, 'OBJECTID') and \
                                        not AIStrUtils.isEqual(fldName, 'NAME') and \
                                        not AIStrUtils.isEqual(fldName, 'SHAPE') and \
                                        not 'AREA' in fldName and \
                                        not 'LEN' in fldName:
                                        # 需要添加的字段
                                        field = None
                                        # 查找需要添加的字段
                                        for nfld in nFields:
                                            if AIStrUtils.isEqual(nfld['name'], nfn):
                                                field = nfld
                                                break
                                        keys = field.keys()
                                        # 字段名
                                        fldName = arcpy.ValidateFieldName(fldName, wksName)
                                        # 字段别名
                                        fldAlias = fldName if not 'alias' in keys else field['alias']
                                        # 字段类型 Integer--LONG  Double--DOUBLE  String--TEXT Date--DATE
                                        fldType = AIStrUtils.toUpper(AIStrUtils.trim(None if not 'ftype' in keys else field['ftype']))
                                        fldType = 'LONG' if AIStrUtils.isEqual(fldType, 'INTEGER') else \
                                        'TEXT' if AIStrUtils.isEqual(fldType, 'STRING') else fldType
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
                logger.info('要素类' + fcName + '更新失败')
    print flag