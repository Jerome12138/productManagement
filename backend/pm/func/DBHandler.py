from pm import models

# ========== 产品类型 ==========

# 获取产品类型列表
def getProductType():
    # functionData = models.FunctionData.objects.filter(productType=productType).values()
    # print(functionData)
    return [{
        "code": 'electric_heater',
        "value": '电热水器'
    }]

# ========== 产品 ==========

# 获取产品列表
def queryProduct(**condition):
    print(condition)
    if condition.get('productType'):
        condition['productType__in'] = condition['productType']
        condition.pop('productType')
    if condition.get('model'):
        condition['model__in'] = condition['model']
        condition.pop('model')
    if condition.get('functionIds'):
        condition.pop('functionIds')
    productData = list(models.ProductData.objects.filter().values())
    for item in productData:
        if item.get('functionIds'):
            item['functionIds'] = eval(item['functionIds'])
    # print(productData)
    return list(productData)

def saveProduct(productData):
    try:
        if productData.get('id'):
            productData['id'] = int(productData['id'])
        elif productData.get('id') == "":
            productData['id'] = -1
        obj = models.ProductData.objects.filter(
            id=productData.get('id')).first()
        if obj:
            obj.__dict__.update(productData)
            obj.save()
            print('数据已更新:%s' % productData['sN8'])
        else:
            productData.pop('id')
            models.ProductData.objects.create(**productData)
            print('数据已添加：%s' % productData['sN8'])
        return True
    except Exception as e:
        print(e)
        return False

# ========== 功能类型 ==========

# 获取功能类型列表
def getFunctionTypeList(productType):
    functionTypeData = models.FunctionTypeData.objects.filter(productType=productType).values()
    return list(functionTypeData)

# ========== 功能 ==========

# 获取功能列表
def getFunctionList(productType):
    functionData = models.FunctionData.objects.filter(productType=productType).values()
    # print(functionData)
    return list(functionData)

# 保存功能数据
def saveFunction(functionData):
    # print(functionData)
    try:
        if functionData.get('id') == "":
            functionData['id'] = -1
        obj = models.FunctionData.objects.filter(
            id=functionData.get('id')).first()
        if obj:
            obj.__dict__.update(functionData)
            obj.save()
            print('数据已更新:%s' % functionData['functionName'])
        else:
            functionData.pop('id')
            models.FunctionData.objects.create(**functionData)
            print('数据已添加：%s' % functionData['functionName'])
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
    taskList = models.TaskData.objects.filter().values()
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