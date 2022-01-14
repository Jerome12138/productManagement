from pm import models

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
        # if productData.get('id'):
        #     productData['id'] = int(productData['id'])
        # elif productData.get('id') == "":
        #     productData['id'] = -1
        # obj = models.ProductData.objects.filter(
        #     id=productData.get('id')).first()
        # if obj:
        #     obj.__dict__.update(productData)
        #     obj.save()
        #     print('数据已更新:%s' % productData['sN8'])
        # else:
        #     productData.pop('id')
        #     models.ProductData.objects.create(**productData)
        #     print('数据已添加：%s' % productData['sN8'])
        return True
    except Exception as e:
        print(e)
        return False


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