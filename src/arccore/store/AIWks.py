# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# script name : AIWks
# Description : 工作空间类
# project : GIS
# author : zhoufl3
# create date :2016年1月4日
# ---------------------------------------------------------------------------
# Modify record
# author :
# Modify date :
# Description :
# ---------------------------------------------------------------------------

import os
import arcpy
from arccore.utils.AIUtils import AIUtils
from arccore.utils.AIStrUtils import AIStrUtils
from arccore.store.AISde import AISde
from arccore.store.AIFds import AIFds
from arccore.store.AIFc import AIFc
from arccore.store.AIFld import AIFld

class AIWks(object):
    '''
    工作空间类
    '''
    __wksName = None
    __userName = None
    
    def __init__(self, wksName, userName = None):
        '''
        构造器
        '''
        if not AIUtils.isEmpty(wksName):
            arcpy.env.workspace = self.__wksName = wksName.replace('\\', '/')
            self.__userName = userName
    
    ############### 要素集管理(暂时不提供更改操作)################    
    def queryFds(self, fds):
        '''
    查询要素集
        '''
        qr = None
        if isinstance(fds, AIFds):
            name = fds.getName()
            if not AIUtils.isEmpty(name):
                name = name if ('.' in name) else name if AIUtils.isEmpty(self.__userName) else (self.__userName + '.') + name
                datasets = arcpy.ListDatasets(name, 'Feature')
                if len(datasets) > 0 and not AIUtils.isEmpty(datasets[0]):
                    dataset = datasets[0]
                    desc = arcpy.Describe(dataset)
                    sr = desc.spatialReference
                    qr = AIFds(AIUtils.unicode2utf8(desc.name), None if AIUtils.isEmpty(sr) else sr.factoryCode)
            else:
                raise Exception('dataset name cannot be empty!')
        else:
            raise Exception('input parameter type not correct!')
        
        return qr
    
    def addFds(self, fds):
        '''
    保存要素集
        '''  
        flag = False
        if isinstance(fds, AIFds):
            name = fds.getName()
            if not AIUtils.isEmpty(name):
                if not arcpy.Exists(name):
                    wkid = fds.getWkid()
                    sr = 4326 if not AIUtils.isInt(wkid) else arcpy.SpatialReference(wkid)
                    try:
                        arcpy.CreateFeatureDataset_management(self.__wksName, name, sr)
                        flag = True
                    except:
                        raise
                else:
                    raise Exception('dataset name cannot be duplicated!')
            else:
                raise Exception('dataset name cannot be empty!')
        else:
            raise Exception('input parameter type not correct!')
        
        return flag
    
    def __updateFds(self, fds):
        pass
    
    def removeFds(self, fds):
        '''
    删除要素集
        '''
        flag = False
        if isinstance(fds, AIFds):
            name = fds.getName()
            if not AIUtils.isEmpty(name):
                if arcpy.Exists(name):
                    try:
                        arcpy.Delete_management(name)
                        flag = True
                    except:
                        raise
                else:
                    raise Exception('dataset not exist!')
            else:
                raise Exception('dataset name cannot be empty!')
        else:
            raise Exception('input parameter type not correct!')
                    
        return flag
    
    def queryFdsList(self, fds):
        '''
    查询要素集列表
        '''
        qrs = []
        if isinstance(fds, AIFds):
            name = fds.getName()
            datasets = arcpy.ListDatasets(None if AIUtils.isEmpty(name) else ('*'+ name + '*'), \
                                          'Feature')
            for dataset in datasets:
                desc = arcpy.Describe(dataset)
                sr = desc.spatialReference
                qrs.append(AIFds(AIUtils.unicode2utf8(desc.name), None if AIUtils.isEmpty(sr) else sr.factoryCode)) 
        else:
            raise Exception('input parameter type not correct!')
        
        return qrs
    
    ###############要素类管理################
    def queryFc(self, fc):
        '''
    查询要素类
        '''
        qr = None
        if isinstance(fc, AIFc):
            name = fc.getName()
            ftype = fc.getFtype()
            fds = fc.getFds()
            if not AIUtils.isEmpty(name):
                name = name if ('.' in name) else name if AIUtils.isEmpty(self.__userName) else (self.__userName + '.') + name
                ftype = 'All' if AIUtils.isEmpty(ftype) else ftype
                # 要素集名称
                fdsName = None
                if not AIUtils.isEmpty(fds) and isinstance(fds, AIFds) and not AIUtils.isEmpty(fds.getName()):
                    fdsName = fds.getName()
                    fdsName = fdsName if ('.' in fdsName) else fdsName if AIUtils.isEmpty(self.__userName) else (self.__userName + '.') + fdsName
                    fds = self.queryFds(fds)
                featureclasses = arcpy.ListFeatureClasses(name, ftype, fdsName)
                
                if len(featureclasses) > 0 and not AIUtils.isEmpty(featureclasses[0]):
                    featureclass = featureclasses[0]
                    desc = arcpy.Describe(featureclass)
                    flds = []
                    for field in desc.fields:
                        fld = AIFld(AIUtils.unicode2utf8(field.name), AIUtils.unicode2utf8(field.aliasName), \
                                    AIUtils.unicode2utf8(field.type), field.scale, \
                                    field.length, field.isNullable)
                        flds.append(fld)
                    
                    qr = AIFc(AIUtils.unicode2utf8(desc.name), AIUtils.unicode2utf8(desc.aliasName), \
                              AIUtils.unicode2utf8(desc.shapeType), None if AIUtils.isEmpty(desc.spatialReference) else desc.spatialReference.factoryCode, \
                              fds, flds)
            else:
                raise Exception('featureclass name cannot be empty!')
        else:
            raise Exception('input parameter type not correct!')
                       
        return qr
    
    def addFc(self, fc):
        '''
    保存要素类
        '''
        flag = False
        if isinstance(fc, AIFc):
            name = fc.getName()
            ftype = fc.getFtype()
            alias = fc.getAlias()
            wkid = fc.getWkid()
            fds = fc.getFds()
            if not AIUtils.isEmpty(name) and not AIUtils.isEmpty(ftype):
                if not arcpy.Exists(name):
                    # 要素集名称
                    fdsName = None
                    if not AIUtils.isEmpty(fds) and isinstance(fds, AIFds) and not AIUtils.isEmpty(fds.getName()):
                        fdsName = fds.getName()
                        fdsName = fdsName if ('.' in fdsName) else fdsName if AIUtils.isEmpty(self.__userName) else (self.__userName + '.') + fdsName
                    wksName = self.__wksName if AIUtils.isEmpty(fdsName) else os.path.join(self.__wksName, fdsName).replace('\\', '/')
                    fields = fc.getFields()
                    sr = arcpy.SpatialReference(4326) if not AIUtils.isInt(wkid) else arcpy.SpatialReference(wkid)
                    try:
                        # 创建要素类
                        arcpy.CreateFeatureclass_management(wksName, name, ftype, None, "DISABLED", "DISABLED", sr)
                        # 更改别名
                        if not AIUtils.isEmpty(alias):
                            arcpy.AlterAliasName(name, alias)
                        # 添加字段(排除保留字段)
                        for field in fields:
                            fldName = AIStrUtils.toUpper(field.getName())
                            if not AIStrUtils.isEqual(fldName, 'OBJECTID') and \
                                not AIStrUtils.isEqual(fldName, 'NAME') and \
                                not AIStrUtils.isEqual(fldName, 'SHAPE') and \
                                not 'AREA' in fldName and \
                                not 'LEN' in fldName:
                                # 字段名
                                fldName = arcpy.ValidateFieldName(fldName, self.__wksName)
                                # 字段别名
                                fldAlias = field.getAlias()
                                # 字段类型 Integer--LONG  Double--DOUBLE  String--TEXT Date--DATE
                                fldType = 'TEXT' if AIStrUtils.isEqual(AIStrUtils.toUpper(field.getFtype()), 'STRING') else field.getFtype()
                                # 字段小数点位数（浮点型）
                                fldScale = field.getScale()
                                # 字段长度（文本型）
                                fldLength = field.getLength()
                                # 字段是否允许为空
                                fldIsNullable = field.getIsNullable()
                                
                                arcpy.AddField_management(name, fldName, fldType, None, fldScale, \
                                                          fldLength, fldAlias, fldIsNullable, False)
                        flag = True
                    except:
                        raise
                else:
                    raise Exception('featureclass name cannot be duplicated!')
            else:
                raise Exception('featureclass name and geometry type cannot be empty!')
        else:
            raise Exception('input parameter type not correct!')
    
        return flag
    
    def updateFc(self, fc):
        '''
    更新要素类
        '''
        flag = False
        if isinstance(fc, AIFc):
            name = fc.getName()
            nalias = fc.getAlias() #新字段别名集合
            nFields = fc.getFields() #新字段集合
            nFieldNames = [nfld.getName() for nfld in nFields] #新字段名集合
            if not AIUtils.isEmpty(name):
                if arcpy.Exists(name):
                    ofc = self.queryFc(fc)
                    oalias = ofc.getAlias() # 旧字段别名集合
                    oFields = ofc.getFields() # 旧字段集合
                    oFieldNames = [ofld.getName() for ofld in oFields] #旧字段名集合
                    try:
                        # 更改别名
                        if not AIUtils.isEmpty(nalias) and not AIStrUtils.isEqual(oalias, nalias):
                            arcpy.AlterAliasName(name, nalias)
                        # 比对字段
                        # 删除字段(排除保留字段)
                        for ofn in oFieldNames:
                            if ofn not in nFieldNames and \
                            not AIStrUtils.isEqual(ofn, 'OBJECTID') and \
                            not AIStrUtils.isEqual(ofn, 'NAME') and \
                            not AIStrUtils.isEqual(ofn, 'SHAPE') and \
                            not 'AREA' in ofn and \
                            not 'LEN' in ofn:
                                arcpy.DeleteField_management(name, ofn)
                                
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
                                        if AIStrUtils.isEqual(nfld.getName(), nfn):
                                            field = nfld
                                            break
                                    # 字段名
                                    fldName = arcpy.ValidateFieldName(fldName, self.__wksName)
                                    # 字段别名
                                    fldAlias = field.getAlias()
                                    # 字段类型 Integer--LONG  Double--DOUBLE  String--TEXT Date--DATE
                                    fldType = AIStrUtils.toUpper(AIStrUtils.trim(field.getFtype()))
                                    fldType = 'LONG' if AIStrUtils.isEqual(fldType, 'INTEGER') else \
                                    'TEXT' if AIStrUtils.isEqual(fldType, 'STRING') else fldType
                                    # 字段小数点位数（浮点型）
                                    fldScale = field.getScale()
                                    # 字段长度（文本型）
                                    fldLength = field.getLength()
                                    # 字段是否允许为空
                                    fldIsNullable = field.getIsNullable()
                                    
                                    arcpy.AddField_management(name, fldName, fldType, None, fldScale, \
                                                              fldLength, fldAlias, fldIsNullable, False)
                            
                        flag = True
                    except:
                        raise
                else:
                    raise Exception('featureclass not exist!')
            else:
                raise Exception('featureclass name cannot be empty!')
        else:
            raise Exception('input parameter type not correct!')
    
        return flag
    
    def removeFc(self, fc):
        '''
    删除要素类
        '''
        flag = False
        if isinstance(fc, AIFc):
            name = fc.getName()
            if not AIUtils.isEmpty(name):
                if arcpy.Exists(name):
                    try:
                        arcpy.Delete_management(name)
                        flag = True
                    except:
                        raise
                else:
                    raise Exception('featureclass not exist!')
            else:
                raise Exception('featureclass name cannot be empty!')
        else:
            raise Exception('input parameter type not correct!')
                    
        return flag
    
    def queryFcList(self, fc):
        '''
    查询要素类列表
        '''
        qrs = []
        if isinstance(fc, AIFc):
            name = fc.getName()
            ftype = fc.getFtype()
            ftype = 'All' if AIUtils.isEmpty(ftype) else ftype
            fds = fc.getFds()
            # 要素集名称
            fdsName = None
            if not AIUtils.isEmpty(fds) and isinstance(fds, AIFds) and not AIUtils.isEmpty(fds.getName()):
                fdsName = fds.getName()
                fdsName = fdsName if ('.' in fdsName) else fdsName if AIUtils.isEmpty(self.__userName) else (self.__userName + '.') + fdsName
                fds = self.queryFds(fds)
            featureclasses = arcpy.ListFeatureClasses(None if AIUtils.isEmpty(name) else ('*'+ name + '*'), ftype, fdsName)
            for featureclass in featureclasses:
                desc = arcpy.Describe(featureclass)
                flds = []
                for field in desc.fields:
                    fld = AIFld(AIUtils.unicode2utf8(field.name), AIUtils.unicode2utf8(field.aliasName), \
                                AIUtils.unicode2utf8(field.type), field.scale, \
                                field.length, field.isNullable)
                    flds.append(fld)
                
                qrs.append(AIFc(AIUtils.unicode2utf8(desc.name), AIUtils.unicode2utf8(desc.aliasName), \
                          AIUtils.unicode2utf8(desc.shapeType), None if AIUtils.isEmpty(desc.spatialReference) else desc.spatialReference.factoryCode, \
                          fds, flds))
        else:
            raise Exception('input parameter type not correct!')
        
        return qrs
    
if __name__ == '__main__':
    try:
        sde = AISde('D:\\tmp\\sde', 'orcl21', '192.168.0.21/arcgis', 'gis', 'gis123')
        sdeOutFullName = sde.connect()
        print sdeOutFullName
        if not AIUtils.isEmpty(sdeOutFullName):
            wks = AIWks(sdeOutFullName, 'gis')
#             # query fds
#             qr = wks.queryFds(AIFds('gis.test'))
#             print qr
            
#             # add fds
#             flag = wks.addFds(AIFds('test334', 3857))
#             print flag

#             # delete fds
#             flag = wks.removeFds(AIFds('test334', 3857))
#             print flag

#             # query fds list
#             qrs = wks.queryFdsList(AIFds())
#             print '[' + ','.join([str(qr) for qr in qrs]) + ']'

#             # query fc
#             qr = wks.queryFc(AIFc('fuzhou', None, None, None, AIFds('test333')))
#             print qr

#             # add fc
#             flds = []
#             flds.append(AIFld('name', '名称', 'String', None, 32, True))
#             flds.append(AIFld('len2', '面积', 'Double', 6, 0, True))
#             flag = wks.addFc(AIFc('ent_4326_5', None, 'point', 4326, AIFds(), flds))
#             print flag

#             # update fc
#             flds = []
#             flds.append(AIFld('peo', '人员', 'Integer', None, None, True))
#             flds.append(AIFld('leader', '领导', 'String ', None, 30, True))
#             flds.append(AIFld('foundingTime', '创建时间', 'Date ', None, None, True))
#             flds.append(AIFld('name', '名称2', 'String ', None, 100, True))
#             flag = wks.updateFc(AIFc('ent_4326_4', '新企业', 'point', 4326, AIFds('test_1'), flds))
#             print flag

#             # delete fc
#             flag = wks.removeFc(AIFc('ent_4326_4', '新企业', 'point', 4326, AIFds('test_1'), []))
#             print flag

            # query fc list
#             qrs = wks.queryFcList(AIFc('4326', '新企业', 'point', 4326, AIFds('gis.test'), []))
#             print '[' + ','.join([str(qr) for qr in qrs]) + ']'
#             param2 = "{'name':'test','wkid':''}"
#             fds = AIFds()
#             fds = fds.fromStr(param2)
#             print fds
#             fdss = wks.queryFdsList(fds)
#             print fdss[0]
#             qr = str([AIUtils.dict2json(AIUtils.str2dict(str(fds))) for fds in fdss])
#             print qr
            param2 = "{'name':'4326','alias':'企业nb2','ftype':'point','fds':{'name':'test'}}"
            fc = AIFc()
            fc = fc.fromStr(param2)
            print fc
            fcs = wks.queryFcList(fc)
            print fcs


    except Exception as e:            
        print unicode(e.message).encode("utf-8") 
    
    