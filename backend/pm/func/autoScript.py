# -*- coding:utf-8 -*-

import os,json,re,time
import xlrd
import xlwt
import execjs   # 执行js代码
import json

# 获取js文件
def get_js(file_name):
    f = open(file_name, 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr

# 遍历数据，输出key-value列表
def enumerateObj(data, key_str=""):
    data_list = []
    if isinstance(data, dict):
        # 是字典，则继续遍历下层
        for key, item in data.items():
            next_key = key_str+'.'+key
            next_list = enumerateObj(item, next_key)
            data_list.extend(next_list)
    elif isinstance(data, list):
        # 是列表，逐行拆分
        for index, next_item in enumerate(data):
            list_key = key_str+'.'+str(index)
            next_list = enumerateObj(next_item, list_key)
            data_list.extend(next_list)
    else:
        # 无下层，格式化成字典返回
        data_list.append({"key": key_str, "item": data})
    return data_list
            

# 输出代码配置列表
def output_config(config):
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet(u'sheet', cell_overwrite_ok=True)
    sheet.write(0, 0, '序号')
    sheet.write(0, 1, '路径')
    sheet.write(0, 2, '英语')

    # 遍历对象，输出语料列表
    data_list = enumerateObj(config)
    for index, item in enumerate(data_list):
        print(item['key'],end=':\t')
        print(item['item'])
        key = item['key']
        value = item['item']
        sheet.write(index+1, 0, index)
        sheet.write(index+1, 2, key)
        sheet.write(index+1, 3, str(value))
    
    # 设置第一列的宽度为15，宽度的基本单位为256.所以设置的时候一般用256 × 需要的列宽。
    sheet.col(0).width = 256 * 10
    sheet.col(1).width = 256 * 50
    sheet.col(2).width = 256 * 50
    sheet.col(3).width = 256 * 60
    # 设置行高为可以修改，并修改为 40，行高的基本单位为20，设置同行高。
    # sheet.row(1).height_mismatch = True
    # sheet.row(1).height = 20 * 40

    # 输出excel文件
    now_date = time.strftime("%Y%m%d", time.localtime()) 
    workbook.save('translate_output_%s.xls'%now_date)

def parseJs2Excel(file_name):
    jsstr = get_js(file_name)
    jsstr = re.sub('export default', 'let exportObj =', jsstr) # 替换export default
    ctx = execjs.compile(jsstr)
    config = ctx.eval('exportObj') # 获取setting中的sn8
    # print(config)
    output_config(config)
