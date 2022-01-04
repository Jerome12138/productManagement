from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
import json
from .func import DBHandler
from .func import codeSettingHandler

# Create your views here.

# 返回函数装饰器
def decoRet(func):
    def inner_func(request, *args, **kwargs):
        ret = {'errorCode': '-1', 'error': None, 'result': None}
        try:
            i = func(request, *args, **kwargs)   # 运行原函数
            ret.update(i)
        except Exception as e:
            print('Exception: ', e)
            ret['errorCode'] = '-1'
            ret['error'] = '遇到异常: '+e
        finally:
            return JsonResponse(ret)
        return JsonResponse(i)
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
        ret['errorCode'] = '1'
        req_data = json.loads(request.body)
        print('saveProduct: %s'%req_data)
        DBHandler.saveProduct(req_data)
        codeSettingHandler.settingFileEdit(req_data)
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
        ret['result'] = DBHandler.queryProduct(**{})
    return ret

@decoRet
def saveTask(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        taskData = json.loads(request.body)
        ret['result'] = DBHandler.saveTask(taskData)
    return ret

@decoRet
def queryUnhandledTaskList(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        userId = request.POST.get('userId')
        ret['result'] = DBHandler.queryUnhandledTaskList(userId)
    return ret

@decoRet
def getTaskDetailById(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        taskId = request.GET.get('taskId')
        ret['result'] = DBHandler.getTaskDetailById(taskId)
    return ret