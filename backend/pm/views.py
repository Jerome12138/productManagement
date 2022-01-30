from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
import json
import traceback
from .func import DBHandler
from .func import codeSettingHandler
# from .func import autoScript
import re

# Create your views here.

# 返回函数装饰器
def decoRet(func):
    def inner_func(request, *args, **kwargs):
        ret = {'errorCode': '-1', 'error': None, 'result': None}
        try:
            i = func(request, *args, **kwargs)   # 运行原函数
            ret.update(i)
        except Exception as e:
            print(traceback.print_exc())
            ret['errorCode'] = '-1'
            ret['error'] = '遇到异常: '+e
        finally:
            return JsonResponse(ret)
    return inner_func

@decoRet
def login(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['token'] = 'admin'
    return ret

@decoRet
def logout(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
    return ret

@decoRet
def getUserInfo(request):
    ret = {}
    if request.method == "GET":
        ret['errorCode'] = '0'
        ret = {
            **ret,
            "name": 'admin',
            "user_id": '2',
            "access": ['admin'],
            "token": 'admin',
            "avator": 'https://avatars0.githubusercontent.com/u/20942571?s=460&v=4'
        }
    return ret

@decoRet
def getAllUserIdAndName(request):
    ret = {}
    ret['errorCode'] = '0'
    ret['result'] = DBHandler.getDataByDBName('FmUser', values=['id', 'userName', 'nickName'])
    return ret

@decoRet
def getFunctionByType(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getFunctionList('electric_heater')
    return ret

@decoRet
def saveProduct(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        req_data = json.loads(request.body)
        print('views-saveProduct: %s'%req_data)
        DBHandler.saveProduct(req_data)
        # codeSettingHandler.settingFileEdit(req_data)
    return ret

@decoRet
def saveFunction(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        req_data = json.loads(request.body)
        print('saveFunction: %s'%req_data)
        DBHandler.saveFunction(req_data)
    return ret

@decoRet
def getProductType(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getProductType()
    return ret

@decoRet
def getFunctionType(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getFunctionTypeList('electric_heater')
    return ret

@decoRet
def queryProduct(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        condition = json.loads(request.body)
        ret['result'] = DBHandler.queryProduct(**condition)
    return ret

@decoRet
def getProductModel(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getDataByDBName('FmProductInfo')
    return ret

@decoRet
def saveTask(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        taskData = json.loads(request.body)
        print('saveTask: %s'%taskData)
        ret['result'] = DBHandler.saveTask(taskData)
    return ret

@decoRet
def queryUnhandledTaskList(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        userId = request.GET.get('userId')
        ret['result'] = DBHandler.queryUnhandledTaskList(userId)
    return ret

@decoRet
def queryHandledTaskList(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        userId = request.GET.get('userId')
        ret['result'] = DBHandler.queryHandledTaskList(userId)
    return ret

@decoRet
def getTaskDetailById(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        taskId = request.GET.get('taskId')
        ret['result'] = DBHandler.getTaskDetailById(taskId)
        if not ret['result']:
            ret['errorCode'] = '1'
    return ret
    
@decoRet
def getEcologyEntrance(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getEcologyEntrance()
    return ret

@decoRet
def getProductBranch(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getProductBranch()
    return ret

@decoRet
def getHeatingTubeType(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getHeatingTubeType()
    return ret

@decoRet
def getWifiModuleType(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getWifiModuleType()
    return ret

@decoRet
def getElectricBoardInfo(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        productType = request.GET.get('productType')
        ret['result'] = DBHandler.getDataByDBName('FmElectricBoardInfo', condition={"productType":productType})
    return ret

@decoRet
def getSelectOption(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        productType = request.GET.get('productType')
        # key = request.GET.get('key')
        ret['result'] = DBHandler.getDataByDBName('FmSelectOption', condition={"productType":productType})
    return ret

# 文件上传
@decoRet
def uploadFile(request):
    ret = {}
    if request.method == 'POST':
        obj = request.FILES.get('file')

        #  上传文件类型过滤
        file_type = re.match(r'.*\.js', obj.name)
        if not file_type:
            ret['errorCode'] = 2
            ret['result'] = '文件类型不匹配, 请重新上传'
            return ret
        with open('./pm/upload/'+obj.name, 'wb+') as f:
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()
        ret['errorCode'] = '0'
    return ret

@decoRet
def parseJs2Excel(request):
    ret = {}
    if request.method == 'POST':
        obj = request.FILES.get('file')

        #  上传文件类型过滤
        file_type = re.match(r'.*\.js', obj.name)
        if not file_type:
            ret['errorCode'] = 2
            ret['result'] = '文件类型不匹配, 请重新上传'
            return ret
        with open('./pm/upload/'+obj.name, 'wb+') as f:
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()
        # autoScript.parseJs2Excel(obj)
        ret['errorCode'] = '0'
    return ret