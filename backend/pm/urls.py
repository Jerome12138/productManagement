__author__ = "Jerome"
from django.contrib import admin
from django.urls import path, include
from pm import views

urlpatterns = [
    path('login', views.login),
    path('get_info', views.getUserInfo),
    path('function/getFunctionByType', views.getFunctionByType),
    path('product/saveProduct', views.saveProduct),
    path('function/saveFunction', views.saveFunction),
    path('dict/getProductType', views.getProductType),
    path('function/getFunctionType', views.getFunctionType),
    path('product/queryProduct', views.queryProduct),
    path('product/getProductModel', views.getProductModel),
    path('task/saveTask', views.saveTask),
    path('task/queryUnhandledTaskList', views.queryUnhandledTaskList),
    path('task/getTaskDetailById', views.getTaskDetailById),
]
