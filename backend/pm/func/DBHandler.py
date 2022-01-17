from pm import models
import traceback

# 返回函数装饰器
def decoRet(func):
    def inner_func(request, *args, **kwargs):
        ret = False
        try:
            ret = func(request, *args, **kwargs)   # 运行原函数
        except Exception as e:
            print(traceback.print_exc())
        finally:
            return ret
    return inner_func


# 通用方法，获取db数据，输出字典类型
def getDataByDBName(db_name, **condition):
    if hasattr(models, db_name):
        functionData = getattr(models, db_name).objects.filter(**condition).values()
        return list(functionData)
    else:
        return []

# 通用方法，获取db数据，输出db对象
def getDataObjByDBName(db_name, **condition):
    if hasattr(models, db_name):
        functionData = getattr(models, db_name).objects.filter(**condition)
        return functionData
    else:
        return []

# ========== 产品类型 ==========

# 获取产品类型列表
def getProductType():
    productTypeObjs = models.FmDictionary.objects.filter(keyCode="product_type").values()
    return [ {"code": item['valueCode'], 'value': item['valueName']} for item in productTypeObjs ]


def getEcologyEntrance():
    ecologyObjs = models.FmEncologyEntrance.objects.values()
    return list(ecologyObjs)

def getProductBranch():
    productBranchObjs = models.FmDictionary.objects.filter(keyCode="branch").values()
    return [ {"code": item['valueCode'], 'value': item['valueName']} for item in productBranchObjs ]

# ========== 产品 ==========

# 获取产品列表
def getProductModel():
    productDataObjs = models.FmProductInfo.objects.filter().values()
    return list(productDataObjs)


# 根据条件查询产品全信息
def queryProduct(**condition):
    print("queryProduct查询条件: %s"%condition)
    # 传进来的空字段先删除
    condition = { key: item for key, item in condition.items() if item }
    if 'productType' in condition.keys():
        condition['productType__in'] = condition['productType']
        condition.pop('productType')
    if 'ecologyEntrance' in condition.keys():
        condition.pop('ecologyEntrance')
    if 'id' in condition.keys(): # 只接受数字，暂时用不到先屏蔽
        condition.pop('id')
    if 'function' in condition.keys():
        condition.pop('function')
    if 'scenario' in condition.keys():
        condition.pop('scenario')
    if 'voiceFunction' in condition.keys():
        condition.pop('voiceFunction')
    if 'sensor' in condition.keys():
        condition.pop('sensor')
    if 'pageSize' in condition.keys():
        condition.pop('pageSize')
    if 'pageNumber' in condition.keys():
        condition.pop('pageNumber')
    if 'productModel' in condition.keys():
        condition['model'] = condition['productModel']
        condition.pop('productModel')
    if 'productSN8' in condition.keys():
        condition['sn8'] = condition['productSN8']
        condition.pop('productSN8')
    if 'productCode' in condition.keys():
        condition['code'] = condition['productCode']
        condition.pop('productCode')
    print("queryProduct转化后的条件: %s"%condition)
    # productData = list(models.ProductData.objects.filter().values())
    # for item in productData:
    #     if item.get('functionIds'):
    #         item['functionIds'] = eval(item['functionIds'])
    #         item['functionsName'] = getFunctionNamesByIds(item['functionIds'])

    productData = models.FmProductInfo.objects.filter(**condition).values()[:10]
    for item in productData:
        productFunctionData = models.FmProductFunction.objects.filter(productSn8=item['sn8'], productCode=item['code']).values('functionId')
        # print("queryProduct联动产品功能查询结果: %s"%list(productFunctionData))
        item['functionIds'] = [ func_item['functionId'] for func_item in productFunctionData]
        item['functionsName'] = getFunctionNamesByIds(item['functionIds'])
    # print("queryProduct查询结果: %s"%list(productData))
    return list(productData)


def saveProduct(productData):
    try:
        # 保存产品基本信息
        productInfoKeys = ['id','branch', 'code', 'model', 'productType', 'sn8', 'appStatus', 'lifecycleStage', 'productVersion']
        productInfo = { key: item for key, item in productData.items() if key in productInfoKeys}
        # 这几项暂时不加： , 'productCategory', 'saleChannel', 'pic', 'dishwasherProperty'
        if productInfo.get('id'):
            productInfo['id'] = int(productInfo['id'])
        elif productInfo.get('id') == "":
            productInfo.pop('id')
        # 组装搜索条件
        condition = {
            'sn8': productInfo.get('sn8'),
            'code': productInfo.get('code'),
            'productType': productInfo.get('productType'),
        }
        if productInfo.get('productVersion'):
            condition['productVersion'] = productInfo['productVersion']
        # 查询是否已有产品
        obj = models.FmProductInfo.objects.filter(**condition).first()
        if obj: # 已存在则更新
            obj.__dict__.update(productInfo)
            obj.save()
            print('产品数据已更新: (sn8: %s, code: %s)' % (productInfo['sn8'],productInfo['code']))
        else: # 不存在则添加
            models.FmProductInfo.objects.create(**productInfo)
            print('产品数据已添加: (sn8: %s, code: %s)' % (productInfo['sn8'],productInfo['code']))
        # 保存功能
        saveProductFunction(productInfo, productData.get('functionIds'))
        # 保存场景
        saveProductScenario(productInfo, productData.get('scenarioIds'))
        # 保存电控信息
        saveProductElectricBoardInfo(productInfo, productData.get('electricBoardInfo'))
        # 保存产品语音功能
        saveProductVoiceFunctions(productInfo, productData.get('voiceFunctionIds'))
        # 保存产品生态入口
        saveProductEcologyEntrance(productInfo, productData.get('ecologyEntranceIds'))
        # 保存产品传感器
        saveProductSensor(productInfo, productData.get('sensorIds'))
        return True
    except Exception as e:
        print(e)
        return False


@decoRet
def saveProductFunction(productInfo, functionIds):
    print('--------start: saveProductFunction--------')
    condition = {
        'productSn8':productInfo.get('sn8'),
        'productCode':productInfo.get('code')
    }
    if productInfo.get('productVersion'):
        condition['productVersion'] = productInfo['productVersion']
    # 查询已存在的功能
    existFuncs = getDataObjByDBName('FmProductFunction', **condition)
    allFuncs = getDataByDBName('FmFunction', **{"typeCode": productInfo.get('productType')})
    allFuncIds = [ item['id'] for item in allFuncs ]
    for prodFuncObj in existFuncs:
        funcId = prodFuncObj.functionId
        if funcId in functionIds: # 对于列表中已存在的id从列表中删除
            functionIds.remove(funcId)
        else: # 对于列表中不存在的id将prodFuncObj数据删除
            print('已删除产品功能：%s' % funcId)
            prodFuncObj.delete()
    for funcId in functionIds:
        if funcId not in allFuncIds:
            print("存在非法功能id: %s, 请核查" % funcId)
            continue
        newProdFunc = {
            **condition,
            'functionId': funcId,
        }
        models.FmProductFunction.objects.create(**newProdFunc)
        print('已添加产品功能：%s' % funcId)
    print('--------done: saveProductFunction--------')
    return True


@decoRet
def saveProductScenario(productInfo, scenarioIds):
    print('--------start: saveProductScenario--------')
    condition = {
        'productSn8': productInfo.get('sn8'),
        'productCode': productInfo.get('code')
    }
    if productInfo.get('productVersion'):
        condition['productVersion'] = productInfo['productVersion']
    # 查询已存在的功能
    existFuncs = getDataObjByDBName('FmProductScenario', **condition)
    allFuncs = getDataByDBName('FmScenario', **{"typeCode": productInfo.get('productType')})
    allFuncIds = [ item['id'] for item in allFuncs ]
    for prodFuncObj in existFuncs:
        funcId = prodFuncObj.scenarioId
        if funcId in scenarioIds: # 对于列表中已存在的id从列表中删除
            scenarioIds.remove(funcId)
        else: # 对于列表中不存在的id将prodFuncObj数据删除
            print('已删除产品场景功能：%s' % funcId)
            prodFuncObj.delete()
    for funcId in scenarioIds:
        if funcId not in allFuncIds:
            print("存在非法场景功能id: %s, 请核查" % funcId)
            continue
        newProdFunc = {
            **condition,
            'scenarioId': funcId,
        }
        models.FmProductScenario.objects.create(**newProdFunc)
        print('已添加产品场景功能：%s' % funcId)
    print('--------done: saveProductScenario--------')
    return True


@decoRet
def saveProductElectricBoardInfo(productInfo, electricBoardInfo):
    print('--------start: saveProductElectricBoardInfo--------')
    condition = {
        'productSn8':productInfo.get('sn8'),
        'productCode':productInfo.get('code'),
        'productType': productInfo.get('productType'),
    }
    if productInfo.get('productVersion'):
        condition['productVersion'] = productInfo['productVersion']
    # 查询已存在的电控信息
    existElecInfos = getDataObjByDBName('FmProductElectricBoardInfo', **condition)
    allElecInfos = getDataByDBName('FmElectricBoardInfo', **{"productType": productInfo.get('productType')})
    allElecInfoKeys = [ item['typeKey'] for item in allElecInfos ]
    # 先针对已存在的数据看是否需要删除或修改
    for prodElecInfoObj in existElecInfos:
        infoKey = prodElecInfoObj.infoKey
        if infoKey in electricBoardInfo.keys(): # 对于列表中已存在的id从列表中删除，数据不一样的进行更改
            if prodElecInfoObj.infoValue != electricBoardInfo[infoKey]:
                prodElecInfoObj.infoValue = electricBoardInfo[infoKey]
                prodElecInfoObj.save()
                print('已更新产品电控信息：%s -> %s' % (infoKey, electricBoardInfo[infoKey]))
            electricBoardInfo.pop(infoKey)
        else: # 对于列表中不存在的id将prodElecInfoObj数据删除
            prodElecInfoObj.delete()
            print('已删除产品电控信息：%s' % (infoKey))
    # 再添加不存在的数据
    for infoKey in electricBoardInfo.keys():
        if infoKey not in allElecInfoKeys:
            print("存在非法电控信息key: %s, 请核查" % infoKey)
            continue
        newProdElecInfo = {
            **condition,
            'infoKey': infoKey,
            'infoValue': productInfo[infoKey],
        }
        models.FmProductElectricBoardInfo.objects.create(**newProdElecInfo)
        print('已添加产品电控信息：%s -> %s' % (infoKey, productInfo[infoKey]))
    print('--------done: saveProductElectricBoardInfo--------')
    return True


@decoRet
def saveProductEcologyEntrance(productInfo, ecologyEntranceIds):
    print('--------start: saveProductEcologyEntrance--------')
    condition = {
        'productSn8': productInfo.get('sn8'),
        'productCode': productInfo.get('code')
    }
    if productInfo.get('productVersion'):
        condition['productVersion'] = productInfo['productVersion']
    # 查询已存在的功能
    existFuncs = getDataObjByDBName('FmProductEcologyEntrance', **condition)
    allFuncs = getDataByDBName('FmEncologyEntrance')
    allFuncIds = [ item['id'] for item in allFuncs ]
    for prodFuncObj in existFuncs:
        funcId = prodFuncObj.ecologyEntranceId
        if funcId in ecologyEntranceIds: # 对于列表中已存在的id从列表中删除
            ecologyEntranceIds.remove(funcId)
        else: # 对于列表中不存在的id将prodFuncObj数据删除
            print('已删除产品生态入口：%s' % funcId)
            prodFuncObj.delete()
    for funcId in ecologyEntranceIds:
        if funcId not in allFuncIds:
            print("存在非法生态入口id: %s, 请核查" % funcId)
            continue
        newProdFunc = {
            **condition,
            'ecologyEntranceId': funcId,
        }
        models.FmProductEcologyEntrance.objects.create(**newProdFunc)
        print('已添加产品生态入口：%s' % funcId)
    print('--------done: saveProductEcologyEntrance--------')
    return True


@decoRet
def saveProductVoiceFunctions(productInfo, voiceFunctionIds):
    print('--------start: saveProductVoiceFunctions--------')
    condition = {
        'productSn8': productInfo.get('sn8'),
        'productCode': productInfo.get('code')
    }
    if productInfo.get('productVersion'):
        condition['productVersion'] = productInfo['productVersion']
    # 查询已存在的功能
    existFuncs = getDataObjByDBName('FmProductVoiceFunction', **condition)
    allFuncs = getDataByDBName('FmVoiceFunction')
    allFuncIds = [ item['id'] for item in allFuncs ]
    for prodFuncObj in existFuncs:
        funcId = prodFuncObj.voiceFunctionId
        if funcId in voiceFunctionIds: # 对于列表中已存在的id从列表中删除
            voiceFunctionIds.remove(funcId)
        else: # 对于列表中不存在的id将prodFuncObj数据删除
            print('已删除产品语音功能：%s' % funcId)
            prodFuncObj.delete()
    for funcId in voiceFunctionIds:
        if funcId not in allFuncIds:
            print("存在非法语音功能id: %s, 请核查" % funcId)
            continue
        newProdFunc = {
            **condition,
            'voiceFunctionId': funcId,
        }
        models.FmProductVoiceFunction.objects.create(**newProdFunc)
        print('已添加产品语音功能：%s' % funcId)
    print('--------done: saveProductVoiceFunctions--------')
    return True


@decoRet
def saveProductSensor(productInfo, sensorIds):
    print('--------start: saveProductSensor--------')
    condition = {
        'productSn8': productInfo.get('sn8'),
        'productCode': productInfo.get('code')
    }
    if productInfo.get('productVersion'):
        condition['productVersion'] = productInfo['productVersion']
    # 查询已存在的功能
    existFuncs = getDataObjByDBName('FmProductSensor', **condition)
    allFuncs = getDataByDBName('FmSensor', **{"typeCode": productInfo.get('productType')})
    allFuncIds = [ item['id'] for item in allFuncs ]
    for prodFuncObj in existFuncs:
        funcId = prodFuncObj.sensorId
        if funcId in sensorIds: # 对于列表中已存在的id从列表中删除
            sensorIds.remove(funcId)
        else: # 对于列表中不存在的id将prodFuncObj数据删除
            print('已删除产品传感器：%s' % funcId)
            prodFuncObj.delete()
    for funcId in sensorIds:
        if funcId not in allFuncIds:
            print("存在非法传感器id: %s, 请核查" % funcId)
            continue
        newProdFunc = {
            **condition,
            'sensorId': funcId,
        }
        models.FmProductSensor.objects.create(**newProdFunc)
        print('已添加产品传感器：%s' % funcId)
    print('--------done: saveProductSensor--------')
    return True


# ========== 功能类型 ==========

# 获取功能类型列表
def getFunctionTypeList(productType, orderBy="displayPriority"):
    functionTypeData = models.FmFunctionType.objects.filter(productType=productType).order_by(orderBy).values()
    return list(functionTypeData)

def getHeatingTubeType():
    heatingTubeTypeData = models.HeatingTubeTypeData.objects.values()
    return list(heatingTubeTypeData)

def getWifiModuleType():
    wifiModuleType = models.WifiModuleTypeData.objects.values()
    return list(wifiModuleType)

# ========== 功能 ==========

# 获取功能列表
def getFunctionList(productType):
    functionData = models.FmFunction.objects.filter(typeCode=productType).values()
    # print(list(functionData))
    return list(functionData)

# 获取功能列表
def getFunctionNamesByIds(ids):
    # print(ids)
    functionData = models.FmFunction.objects.filter(id__in=ids).values('functionName')
    # print(list(functionData))
    functionNames = [ item['functionName'] for item in functionData]
    # print(functionNames)
    return ",".join(functionNames)

# 保存功能数据
def saveFunction(functionData):
    # print(functionData)
    try:
        # todo: 待修改数据库指向
        # if functionData.get('id') == "":
        #     functionData['id'] = -1
        # obj = models.FunctionData.objects.filter(
        #     id=functionData.get('id')).first()
        # if obj:
        #     obj.__dict__.update(functionData)
        #     obj.save()
        #     print('数据已更新:%s' % functionData['functionName'])
        # else:
        #     functionData.pop('id')
        #     models.FunctionData.objects.create(**functionData)
        #     print('数据已添加：%s' % functionData['functionName'])
        return True
    except Exception as e:
        print(e)
        return False

# ========== 任务 ==========

def saveTask(taskData):
    print(taskData)
    try:
        if not taskData.get('id') or taskData.get('id') == "":
            taskData['id'] = -1
        obj = models.TaskData.objects.filter(
            id=taskData.get('id')).first()
        if obj:
            obj.__dict__.update(taskData)
            obj.save()
            print('数据已更新：%s' % taskData['title'])
        else:
            taskData.pop('id')
            models.TaskData.objects.create(**taskData)
            print('数据已添加：%s' % taskData['title'])
        return True
    except Exception as e:
        print(e)
        return False

def queryUnhandledTaskList(userId):
    print(userId)
    taskList = models.FmDevelopTask.objects.filter(currentHandleUserId=userId).exclude(currentHandleFinishUserId=userId).order_by('-updateDateTime').values()
    return list(taskList)

def getTaskDetailById(taskId):
    print(taskId)
    try:
        if type(taskId) == 'String':
            taskId = int(taskId)
        taskDetail = models.TaskData.objects.filter(id=taskId).values()
        # print(taskDetail[0])
        return taskDetail[0]
    except Exception as e:
        print(e)
        return None