from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
import json
from .func import DBHandler
from .func import codeSettingHandler

# Create your views here.

def getFunctionByType(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '0'
            ret['result'] = DBHandler.getFunctionList('electric_heater')
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)

def saveProduct(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '1'
            req_data = json.loads(request.body)
            print('saveProduct: %s'%req_data)
            DBHandler.saveProduct(req_data)
            codeSettingHandler.settingFileEdit(req_data)
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)

def saveFunction(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '0'
            req_data = json.loads(request.body)
            print('saveFunction: %s'%req_data)
            DBHandler.saveFunction(req_data)
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)

def getProductType(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '0'
            ret['result'] = DBHandler.getProductType()
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)

def getFunctionType(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '0'
            ret['result'] = DBHandler.getFunctionTypeList('electric_heater')
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)

def queryProduct(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '0'
            condition = json.loads(request.body)
            ret['result'] = DBHandler.queryProduct(**condition)
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)

def getProductModel(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '0'
            ret['result'] = DBHandler.queryProduct(**{})
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)

def saveTask(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '0'
            taskData = json.loads(request.body)
            ret['result'] = DBHandler.saveTask(taskData)
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)

def queryUnhandledTaskList(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '0'
            userId = request.POST.get('userId')
            ret['result'] = DBHandler.queryUnhandledTaskList(userId)
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)

def getTaskDetailById(request):
    ret = {'errorCode': '-1', 'error': None, 'result': None}
    try:
        if request.method == "POST":
            ret['errorCode'] = '0'
            taskId = request.GET.get('taskId')
            ret['result'] = DBHandler.getTaskDetailById(taskId)
    except Exception as e:
        print('Exception:', e)
        ret['errorCode'] = '-1'
        ret['error'] = '遇到异常'+e
    finally:
        return JsonResponse(ret)