from django.shortcuts import render, HttpResponse
from django.http import FileResponse, Http404
from django.http.response import JsonResponse
import json, os
import traceback
from .func import DBHandler
from .func import codeSettingHandler
from .func import taskQueue
# from .func import autoScript
import re
import requests
import urllib

# Create your views here.

session = requests.session()
session.headers['Host'] = "product-function.midea-hotwater.com"
midea_url = 'https://product-function.midea-hotwater.com/pm/%s'

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


# @decoRet
def login(request):
    res = session.post(midea_url%'login', json=json.loads(request.body))
    result = json.loads(res.content.decode())
    return JsonResponse(result)
    # ret = {}
    # if request.method == "POST":
    #     ret['errorCode'] = '0'
    #     ret['token'] = 'admin'
    # return ret

@decoRet
def logout(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
    return ret

# @decoRet
def getUserInfo(request):
    token = request.GET.get('token')
    session.headers['Cookie'] = "token=%s"%token
    # print(session.headers)
    token_encode = urllib.parse.quote(token)
    # print(token_encode)
    response = session.get(midea_url%'get_info?token=%s'%token_encode)
    print(response.content)
    result = json.loads(response.content.decode())
    res = JsonResponse(result)
    # res_cookie = response.cookies['token']
    # print(res_cookie)
    # res.set_cookie('token',res_cookie)
    return res
    # return JsonResponse(result)
    # ret = {}
    # if request.method == "GET":
    #     ret['errorCode'] = '0'
    #     ret = {
    #         **ret,
    #         "name": 'admin',
    #         "user_id": '2',
    #         "access": ['admin'],
    #         "token": 'admin',
    #         "avator": 'https://avatars0.githubusercontent.com/u/20942571?s=460&v=4'
    #     }
    # return ret


def getAllUser(request):
    # token = request.COOKIES.get('token')
    # print(request.COOKIES)
    # session.headers['Cookie'] = "token=%s"%token
    res = session.post(midea_url%'user/getAllUser')
    result = json.loads(res.content.decode())
    return JsonResponse(result)


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
def getVoiceFunction(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getDataByDBName('FmVoiceFunction')
    return ret

@decoRet
def queryAuditGroupByUserId(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        createUserId = request.GET.get('id')
        groups = DBHandler.getDataByDBName('FmDevelopTaskAuditGroup', condition={"createUserId": createUserId})
        allUsers = DBHandler.getDataByDBName('FmUser', values=['id', 'userName', 'nickName'])
        groupUsers = DBHandler.getDataByDBName('FmDevelopTaskAuditGroupUser')
        if len(groups):
            for group in groups:
                group['userIds'] = [ groupUser['userId'] for groupUser in groupUsers if groupUser['auditGroupId'] == group['id']]
                userNames = [ user['userName'] for user in allUsers if user['id'] in group['userIds'] ]
                group['userNames'] = ','.join(userNames)
                nickNames = [ user['nickName'] for user in allUsers if user['id'] in group['userIds'] ]
                group['nickNames'] = ','.join(nickNames)
        ret['result'] = groups
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
def handleTaskProcess(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        taskOperation = json.loads(request.body)
        print('handleTaskProcess: %s'%taskOperation)
        ret.update(DBHandler.handleTaskProcess(taskOperation))
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


@decoRet
def getQueue(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        ret['result'] = DBHandler.getDataByDBName('FmTaskQueue')
    return ret

@decoRet
def pushCompileQueue(request):
    ret = {}
    if request.method == "POST":
        ret['errorCode'] = '0'
        taskId = request.GET.get('taskId')
        taskData = DBHandler.getDataObjByDBName('FmDevelopTask',condition={"id": taskId}).first()
        print('pushCompileQueue: %s'%taskData)
        taskQueue.pushQueue(taskData)
        taskQueue.startQueue()
    return ret

def fileDownload(request):
    file_id = request.GET.get('fileId')
    file_obj = DBHandler.getDataObjByDBName('FmFileMap',condition={"fileId": file_id}).first()
    if file_obj:
        file_path = file_obj.filePath
        file_name = file_obj.fileName
        is_file = os.path.isfile(file_path+file_name)
        if is_file:
            print("下载: "+file_path+file_name)
            response = FileResponse(open(file_path+file_name, 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            return response
        else:
            print('文件不存在: '+file_path+file_name)
            return Http404
    else:
        print('非法文件id: '+file_id)
        return Http404