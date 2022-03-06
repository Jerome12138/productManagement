from pm import models
from django.db.models import Q      # 导入Q模块
import datetime
import time
import traceback
import uuid

TASK_STATUS_NAME_MAP = {
    'auditing': '正在审核',
    'audit_fail_confirming': '审核未通过',
    'accepting': '正在接受',
    'accept_reject_confirming': '拒绝接受',
    'finishing': '正在执行',
    'finish_confirming': '已完成',
    'not_finish_confirming': '未完成',
    'end': '结束',
}

OPERATION_ROLE_NAME_MAP = {
    "sponsor": "发起人",
    "auditor": "审核人",
    "actor": "执行人",
}
OPERATION_CODE_NAME_MAP = {
    "audit_pass": "审核通过",
    "audit_not_pass": "审核不通过",
    "actor_accept": "接受任务",
    "actor_not_accept": "不接受任务",
    "actor_finish": "完成任务",
    "actor_not_finish": "未完成任务",
    "sponsor_send_audit": "发送审核",
    "sponsor_reject_not_accept": "驳回不接受任务",
    "sponsor_reject_finish": "驳回完成任务",
    "sponsor_reject_not_finish": "驳回未完成任务",
    "sponsor_end": "确认结束",
}

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
def getDataByDBName(db_name, condition={}, values=[], order_by=['-updateDateTime','-id']):
    if hasattr(models, db_name):
        functionData = getattr(models, db_name).objects.filter(**condition).order_by(*order_by).values(*values)
        return list(functionData)
    else:
        return []

# 通用方法，获取db数据，输出db对象
def getDataObjByDBName(db_name, condition={}, order_by=['-updateDateTime','-id']):
    if hasattr(models, db_name):
        functionData = getattr(models, db_name).objects.filter(**condition).order_by(*order_by)
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
    # if 'id' in condition.keys(): # 只接受数字，暂时用不到先屏蔽
    #     condition.pop('id')
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
    productData = models.FmProductInfo.objects.filter(**condition).values()[:10]
    for item in productData:
        productFunctionData = models.FmProductFunction.objects.filter(productSn8=item['sn8'], productCode=item['code']).values('functionId')
        # print("queryProduct联动产品功能查询结果: %s"%list(productFunctionData))
        item['functionIds'] = [ func_item['functionId'] for func_item in productFunctionData]
        item['functionsName'] = getFunctionNamesByIds(item['functionIds'])
    # print("queryProduct查询结果: %s"%list(productData))
    return list(productData)


@decoRet
def saveProduct(productData):
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
    existFuncs = getDataObjByDBName('FmProductFunction', condition=condition)
    allFuncs = getDataByDBName('FmFunction', condition={"typeCode": productInfo.get('productType')})
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
    existFuncs = getDataObjByDBName('FmProductScenario', condition=condition)
    allFuncs = getDataByDBName('FmScenario', condition={"typeCode": productInfo.get('productType')})
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
    existElecInfos = getDataObjByDBName('FmProductElectricBoardInfo', condition=condition)
    allElecInfos = getDataByDBName('FmElectricBoardInfo', condition={"productType": productInfo.get('productType')})
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
    existFuncs = getDataObjByDBName('FmProductEcologyEntrance', condition=condition)
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
    existFuncs = getDataObjByDBName('FmProductVoiceFunction', condition=condition)
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
    existFuncs = getDataObjByDBName('FmProductSensor', condition=condition)
    allFuncs = getDataByDBName('FmSensor', condition={"typeCode": productInfo.get('productType')})
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
@decoRet
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

@decoRet
def saveTask(taskData):
    # 保存任务基本信息
    taskInfoKeys = ['id','title', 'content', 'createUserId', 'status', 'productType', 'productIds', 'actorUserId', 'auditGroupUserIds', 'pm', 'planner', 'hardwareEngineer', 'softwareEngineer']
    # 筛选所需数据
    taskInfo = { key: item for key, item in taskData.items() if key in taskInfoKeys}
    if taskInfo.get('id'):
        # 有id更新任务
        taskInfo['id'] = int(taskInfo['id'])
        # 查询是否已存在该任务
        obj = models.FmDevelopTask.objects.filter(id=taskInfo['id']).first()
        if obj: # 已存在则更新
            obj.__dict__.update(taskInfo)
            obj.save()
            print('任务数据已更新: (title: %s)' % (taskInfo['title']))
            return True
        else:
            print('未知任务id')
            return False
    elif taskInfo.get('id') == "":
        # 无id添加任务，去除id字段
        taskInfo.pop('id')
    # 任务数据预处理
    taskInfo.pop('actorUserId')
    taskInfo['sponsorUserId'] = taskInfo.pop('createUserId')
    currentHandleUserIds = [str(item) for key, item in taskInfo.items() if key in ['pm','planner','hardwareEngineer','softwareEngineer']]
    currentHandleUserIds.extend(taskInfo.pop('auditGroupUserIds').split(','))
    taskInfo['currentHandleUserId'] = ','.join(set(currentHandleUserIds))
    taskInfo['auditUserIds'] = taskInfo['currentHandleUserId']
    taskInfo['sponsorTime'] = datetime.datetime.now()
    taskInfo['status'] = "auditing"
    taskInfo['currentHandlerRole'] = "auditor"
    
    models.FmDevelopTask.objects.create(**taskInfo)
    print('任务数据已添加: (title: %s)' % (taskInfo['title']))
    return True

def queryUnhandledTaskList(userId):
    taskList = models.FmDevelopTask.objects.filter(currentHandleUserId__regex=r'(.+,)*(%s)(,.+)*'%userId).exclude(currentHandleFinishUserId__regex=r'(.+,)*(%s)(,.+)*'%userId).order_by('-updateDateTime').values()
    return list(taskList)

def queryHandledTaskList(userId):
    taskObjList = models.FmDevelopTaskProcessContent.objects.filter(userId=userId)
    taskIdList = [ item.developTaskId for item in taskObjList]
    taskList = models.FmDevelopTask.objects.filter(Q(sponsorUserId=userId) | Q(id__in=taskIdList)).order_by('-updateDateTime').values()
    return list(taskList)

def getTaskDetailById(taskId):
    try:
        if type(taskId) == 'String':
            taskId = int(taskId)
        taskDetailList = models.FmDevelopTask.objects.filter(id=taskId).values()
        if taskDetailList and len(taskDetailList) > 0:
            taskDetail = taskDetailList[0]
            # print(taskDetail[0])
            curUserIdStr = taskDetail.get('currentHandleUserId') or ""
            curUserIdList = curUserIdStr.split(',')
            curFinishUserIdStr = taskDetail.get('currentHandleFinishUserId') or ""
            curFinishUserIdList = curFinishUserIdStr.split(',')
            
            taskDetail['currentHandlerIds'] = list(set(curUserIdList).difference(set(curFinishUserIdList)))
            taskDetail['sponsorTime'] = str(taskDetail['sponsorTime']).split('.')[0]
            # 获取发起人姓名
            allUserInfo = getDataByDBName('FmUser', values=['id', 'userName', 'nickName'])
            taskDetail['sponsorName'] = ''
            currentHandlerNames = []
            for userInfo in allUserInfo:
                if userInfo['id'] == taskDetail.get('sponsorUserId'):
                    taskDetail['sponsorName'] = userInfo['nickName']
                if str(userInfo['id']) in taskDetail.get('currentHandlerIds'):
                    currentHandlerNames.append(userInfo['nickName'])
            taskDetail['currentHandlerNames'] = ','.join(currentHandlerNames)
            # 获取状态名称
            taskDetail['statusName'] = TASK_STATUS_NAME_MAP[taskDetail['status'] or 'auditing']
            # 获取productIds转化为数组
            taskDetail['productIds'] = eval(taskDetail['productIds']) if taskDetail['productIds'] else []
            # 拼接型号名称
            productModelDicts = getDataByDBName('FmProductInfo',condition={"id__in":taskDetail['productIds']})
            productModels = [ item['model'] for item in productModelDicts ]
            taskDetail['productModels'] = ','.join(productModels)
            # 获取处理流程
            taskProcessDicts = getDataByDBName('FmDevelopTaskProcessContent', condition={"developTaskId":taskDetail['id']})
            for item in taskProcessDicts:
                item['userName'] = getDataObjByDBName('FmUser', condition={"id": item['userId']}).first().nickName
                item['roleName'] = OPERATION_ROLE_NAME_MAP[item['role']]
                item['operationName'] = OPERATION_CODE_NAME_MAP[item['operation']]
            taskDetail['taskProcess'] = taskProcessDicts
            return taskDetail
        else:
            return None
    except Exception as e:
        print(traceback.print_exc())
        return None

def saveProcessContent(operation):
    processContent = {
        'developTaskId': operation.get('taskId'),
        'operation': operation.get('operation'),
        'opinion': operation.get('operationOpinion'),
        'role': operation.get('role'),
        'userId': operation.get('userId'),
    }
    models.FmDevelopTaskProcessContent.objects.create(**processContent)
    print('任务评论已添加: (taskId: %s)' % (processContent['developTaskId']))

@decoRet
def handleTaskProcess(taskOperation):
    # 根据任务状态 对任务处理
    taskDataObj = getDataObjByDBName('FmDevelopTask', condition={"id":taskOperation.get('taskId')}).first()
    status = taskDataObj.status
    currentHandleUserIds = taskDataObj.currentHandleUserId

    if not currentHandleUserIds or len(currentHandleUserIds.split(",")) == 0:
        return { 'errorCode': '2', 'msg': '当前用户不是该任务目前的处理用户！'}
    # 当前流程处理用户id合集
    setForCurrentHandleUserId = currentHandleUserIds.split(",")
    userId = str(taskOperation.get('userId'))
    if userId not in setForCurrentHandleUserId:
        return { 'errorCode': '2', 'msg': '当前用户不是该任务目前的处理用户！'}
    # 当前流程处理用户，已完成处理的用户id合集
    setForFinishCurrentHandleUserId = []
    if taskDataObj.currentHandleFinishUserId and len(taskDataObj.currentHandleFinishUserId.split(",")) > 0:
        setForFinishCurrentHandleUserId = taskDataObj.currentHandleFinishUserId.split(",")
    if userId in setForFinishCurrentHandleUserId:
        return { 'errorCode': '3', 'msg': '当前用户已经处理过该任务流程！'}
    #  审核中
    if status == 'auditing':
        # 保存操作内容
        saveProcessContent(taskOperation)
        # 将操作用户id添加到已操作完成的用户id set里面
        setForFinishCurrentHandleUserId.append(userId)
        # 判断是不是所有当前阶段处理人都处理过了
        if set(setForCurrentHandleUserId) <= set(setForFinishCurrentHandleUserId):
            processTask = getDataByDBName('FmDevelopTaskProcessContent', condition={"developTaskId":taskOperation.get('taskId')})
            # 判断是 审核通过 还是 审核不通过，所有审核人都通过，就是审核通过，有一个没通过，就是审核没通过
            auditPass = True
            if not processTask:
                for taskProcessContent in processTask:
                    if taskProcessContent.get('role') != 'auditor':
                        return { 'errorCode': '2', 'msg': '当前用户不是该任务目前的处理用户！'}
                    auditPass = auditPass and taskProcessContent.get('operation') == 'audit_pass'
            if auditPass:
                # 如果审核通过，修改当前处理人角色是执行人，当前处理人id 是 执行人id，已完成处理用户id是空，任务状态是 正在接受
                taskDataObj.currentHandlerRole = 'actor'
                taskDataObj.currentHandleUserId = str(taskDataObj.actorUserId)
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'accepting'
            else:
                # 如果审核不通过，修改当前处理人角色是发起人，当前处理人id 是 发起人id，已完成处理用户id是空，任务状态是 审核没通过
                taskDataObj.currentHandlerRole = 'sponsor'
                taskDataObj.currentHandleUserId = str(taskDataObj.sponsorUserId)
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'audit_fail_confirming'
        else:
            taskDataObj.currentHandleFinishUserId = ",".join(setForFinishCurrentHandleUserId)
        taskDataObj.save()
        print('任务数据已更新: (taskId: %s)' % (taskDataObj.id))
    elif status == 'audit_fail_confirming':
        if taskOperation.get('role') != 'sponsor':
            return { 'errorCode': '4', 'msg': '当前用户不是发起人！'}
        # 判断操作是不是 接受任务 和 不接受任务，如果不是这两个，那么操作是不对的
        if taskOperation.get('operation') != 'sponsor_send_audit' and taskOperation.get('operation') != 'sponsor_end':
            return { 'errorCode': '5', 'msg': '当前操作不是对于审核失败任务的操作！'}
        # 保存操作内容
        saveProcessContent(taskOperation)
        # 将操作用户id添加到已操作完成的用户id set里面
        setForFinishCurrentHandleUserId.append(userId)
        # 判断是不是所有的当前处理人已处理
        if set(setForCurrentHandleUserId) <= set(setForFinishCurrentHandleUserId):
            if taskOperation.get('operation') == 'sponsor_send_audit':
                taskDataObj.currentHandlerRole = 'auditor'
                taskDataObj.currentHandleUserId = taskDataObj.auditUserIds
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'auditing'
            elif taskOperation.get('operation') == 'sponsor_end':
                taskDataObj.currentHandlerRole = ''
                taskDataObj.currentHandleUserId = ''
                taskDataObj.currentHandleFinishUserId = ''
                taskDataObj.status = 'end'
            taskDataObj.save()
            print('任务数据已更新: (taskId: %s)' % (taskDataObj.id))
    elif status == 'accepting':
        if taskOperation.get('role') != 'actor':
            return { 'errorCode': '4', 'msg': '当前用户不是执行人！'}
        # 判断操作是不是 接受任务 和 不接受任务，如果不是这两个，那么操作是不对的
        if taskOperation.get('operation') != 'actor_accept' and taskOperation.get('operation') != 'actor_not_accept':
            return { 'errorCode': '5', 'msg': '当前操作不是接受任务的操作！'}
        # 保存操作内容
        saveProcessContent(taskOperation)
        # 将操作用户id添加到已操作完成的用户id set里面
        setForFinishCurrentHandleUserId.append(userId)
        # 判断是不是所有的当前处理人已处理
        if set(setForCurrentHandleUserId) <= set(setForFinishCurrentHandleUserId):
            if taskOperation.get('operation') == 'actor_accept':
                taskDataObj.currentHandlerRole = 'actor'
                taskDataObj.currentHandleUserId = str(taskDataObj.actorUserId)
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'finishing'
            elif taskOperation.get('operation') == 'actor_not_accept':
                taskDataObj.currentHandlerRole = 'sponsor'
                taskDataObj.currentHandleUserId = str(taskDataObj.sponsorUserId)
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'accept_reject_confirming'
            taskDataObj.save()
            print('任务数据已更新: (taskId: %s)' % (taskDataObj.id))
    elif status == 'accept_reject_confirming':
        if taskOperation.get('role') != 'sponsor':
            return { 'errorCode': '4', 'msg': '当前用户不是发起人！'}
        # 判断操作是不是 接受任务 和 不接受任务，如果不是这两个，那么操作是不对的
        if taskOperation.get('operation') != 'sponsor_reject_not_accept' and taskOperation.get('operation') != 'sponsor_end':
            return { 'errorCode': '5', 'msg': '当前操作不是对于拒绝接受任务的操作！'}
        # 保存操作内容
        saveProcessContent(taskOperation)
        # 将操作用户id添加到已操作完成的用户id set里面
        setForFinishCurrentHandleUserId.append(userId)
        # 判断是不是所有的当前处理人已处理
        if set(setForCurrentHandleUserId) <= set(setForFinishCurrentHandleUserId):
            if taskOperation.get('operation') == 'sponsor_reject_not_accept':
                taskDataObj.currentHandlerRole = 'actor'
                taskDataObj.currentHandleUserId = str(taskDataObj.actorUserId)
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'accepting'
            elif taskOperation.get('operation') == 'sponsor_end':
                taskDataObj.currentHandlerRole = ''
                taskDataObj.currentHandleUserId = ''
                taskDataObj.currentHandleFinishUserId = ''
                taskDataObj.status = 'end'
            taskDataObj.save()
            print('任务数据已更新: (taskId: %s)' % (taskDataObj.id))
    elif status == 'finishing':
        if taskOperation.get('role') != 'actor':
            return { 'errorCode': '4', 'msg': '当前用户不是执行人！'}
        # 判断操作是不是 接受任务 和 不接受任务，如果不是这两个，那么操作是不对的
        if taskOperation.get('operation') != 'actor_finish' and taskOperation.get('operation') != 'actor_not_finish':
            return { 'errorCode': '5', 'msg': '当前操作不是对于完成任务的操作！'}
        # 保存操作内容
        saveProcessContent(taskOperation)
        # 将操作用户id添加到已操作完成的用户id set里面
        setForFinishCurrentHandleUserId.append(userId)
        # 判断是不是所有的当前处理人已处理
        if set(setForCurrentHandleUserId) <= set(setForFinishCurrentHandleUserId):
            if taskOperation.get('operation') == 'actor_finish':
                taskDataObj.currentHandlerRole = 'sponsor'
                taskDataObj.currentHandleUserId = str(taskDataObj.sponsorUserId)
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'finish_confirming'
            elif taskOperation.get('operation') == 'actor_not_finish':
                taskDataObj.currentHandlerRole = 'sponsor'
                taskDataObj.currentHandleUserId = str(taskDataObj.sponsorUserId)
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'not_finish_confirming'
            taskDataObj.save()
            print('任务数据已更新: (taskId: %s)' % (taskDataObj.id))
    elif status == 'finish_confirming':
        if taskOperation.get('role') != 'sponsor':
            return { 'errorCode': '4', 'msg': '当前用户不是发起人！'}
        # 判断操作是不是 接受任务 和 不接受任务，如果不是这两个，那么操作是不对的
        if taskOperation.get('operation') != 'sponsor_reject_finish' and taskOperation.get('operation') != 'sponsor_end':
            return { 'errorCode': '5', 'msg': '当前操作不是对于已完成任务的操作！'}
        # 保存操作内容
        saveProcessContent(taskOperation)
        # 将操作用户id添加到已操作完成的用户id set里面
        setForFinishCurrentHandleUserId.append(userId)
        # 判断是不是所有的当前处理人已处理
        if set(setForCurrentHandleUserId) <= set(setForFinishCurrentHandleUserId):
            if taskOperation.get('operation') == 'sponsor_reject_finish':
                taskDataObj.currentHandlerRole = 'actor'
                taskDataObj.currentHandleUserId = str(taskDataObj.actorUserId)
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'finishing'
            elif taskOperation.get('operation') == 'sponsor_end':
                taskDataObj.currentHandlerRole = ''
                taskDataObj.currentHandleUserId = ''
                taskDataObj.currentHandleFinishUserId = ''
                taskDataObj.status = 'end'
            taskDataObj.save()
            print('任务数据已更新: (taskId: %s)' % (taskDataObj.id))
    elif status == 'not_finish_confirming':
        if taskOperation.get('role') != 'sponsor':
            return { 'errorCode': '4', 'msg': '当前用户不是发起人！'}
        # 判断操作是不是 接受任务 和 不接受任务，如果不是这两个，那么操作是不对的
        if taskOperation.get('operation') != 'sponsor_reject_not_finish' and taskOperation.get('operation') != 'sponsor_end':
            return { 'errorCode': '5', 'msg': '当前操作不是对于未完成任务的操作！'}
        # 保存操作内容
        saveProcessContent(taskOperation)
        # 将操作用户id添加到已操作完成的用户id set里面
        setForFinishCurrentHandleUserId.append(userId)
        # 判断是不是所有的当前处理人已处理
        if set(setForCurrentHandleUserId) <= set(setForFinishCurrentHandleUserId):
            if taskOperation.get('operation') == 'sponsor_reject_not_finish':
                taskDataObj.currentHandlerRole = 'actor'
                taskDataObj.currentHandleUserId = str(taskDataObj.actorUserId)
                taskDataObj.currentHandleFinishUserId = ""
                taskDataObj.status = 'finishing'
            elif taskOperation.get('operation') == 'sponsor_end':
                taskDataObj.currentHandlerRole = ''
                taskDataObj.currentHandleUserId = ''
                taskDataObj.currentHandleFinishUserId = ''
                taskDataObj.status = 'end'
            taskDataObj.save()
            print('任务数据已更新: (taskId: %s)' % (taskDataObj.id))
    elif status == 'end':
        return { 'errorCode': '6', 'msg': '当前任务已结束，不能再进行处理！'}
    return {'errorCode': '0'}



# ============任务队列==============
def saveTaskQueue(queueData):
    # 查询是否已有队列id
    taskQueueObj = models.FmTaskQueue.objects.filter(id=queueData.get('id')).first()
    if queueData.get('id') and taskQueueObj: # 已存在则更新
        taskQueueObj.__dict__.update(queueData)
        taskQueueObj.save()
        print('队列数据已更新: (id: %s, developTaskId: %s, status: %s)' % (queueData['id'],queueData['developTaskId'], queueData['status']))
    else: # 不存在则添加
        taskQueueObj = models.FmTaskQueue.objects.create(**queueData)
        print('队列数据已添加: (developTaskId: %s, status: %s)' % (queueData['developTaskId'], queueData['status']))
    return taskQueueObj

def saveFileMap(file_path, file_name):
    file_data = {
        "fileId": uuid.uuid1(),
        "fileName": file_name,
        "filePath": file_path,
    }
    fileMapObj = models.FmFileMap.objects.create(**file_data)
    return fileMapObj.fileId