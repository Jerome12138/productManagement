__author__ = "Jerome"
from django.contrib import admin
from django.urls import path, include
from pm import views

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),
    path('get_info', views.getUserInfo),
    path('function/getFunctionByType', views.getFunctionByType),
    path('product/saveProduct', views.saveProduct),
    path('function/saveFunction', views.saveFunction),

    path('dict/getProductType', views.getProductType),
    path('dict/getProductBranch', views.getProductBranch),
    path('function/getFunctionType', views.getFunctionType),
    path('function/getHeatingTubeType', views.getHeatingTubeType),
    path('function/getWifiModuleType', views.getWifiModuleType),
    path('product/queryProduct', views.queryProduct),
    path('product/getProductModel', views.getProductModel),
    path('task/saveTask', views.saveTask),
    path('task/queryUnhandledTaskList', views.queryUnhandledTaskList),
    path('task/queryHandledTaskList', views.queryHandledTaskList),
    path('task/getTaskDetailById', views.getTaskDetailById),
    path('ecologyEntrance/getEcologyEntrance', views.getEcologyEntrance),
    path('electricBoardInfo/getElectricBoardInfo', views.getElectricBoardInfo),
    path('selectOption/getSelectOption', views.getSelectOption),
    # 自动化脚本
    path('autoScript/uploadFile', views.uploadFile),
    path('autoScript/parseJs2Excel', views.parseJs2Excel),
]
