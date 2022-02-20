from git.repo import Repo
import os, time
import subprocess
from . import DBHandler

weex_path = "/home/lighthouse/weex-kh-widgets"

publish_path = weex_path + "/publish/"

# ========== 配置文件处理 ==========

# 编辑配置文件
def settingFileEdit(productData={}):
    print('开始处理配置文件')
    repo = Repo(weex_path)
    file_name = weex_path + '/src/widgets/T0xE2/config/setting.js'
    new_lines = []
    # 读取配置文件
    with open(file_name,'r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if '#end 新品自动配置#' in line:
                # 新品配置项处理
                new_line_list = handleSetting(productData)
                new_lines.extend(new_line_list)
                new_lines.append('\n')
            # 复制原来的行
            new_lines.append(line)
    # 更新配置文件
    print('配置写入setting')
    with open(file_name,'w',encoding='utf-8') as f:
        f.writelines(''.join(new_lines))
    
    print('git代码上传')
    # git代码上传
    repo.git.add('.')
    # repo.git.commit('-m','add')
    # repo.remote().pull()
    # repo.remote().push()
    # print('代码打包')
    # compile()
    

# 代码打包
def compile(cate="e2", outputPrefix=""):
    print('开始打包...')
    start_time = time.time()
    log_time = time.strftime("%Y%m%d%H%M", time.localtime(start_time))
    stdout_file_name = "pm/log/%s/compile_log_%s_stdout.txt"%(cate, log_time)
    stderr_file_name = "pm/log/%s/compile_log_%s_stderr.txt"%(cate, log_time)
    with open(stdout_file_name,"wb") as f_out, open(stderr_file_name,"wb") as f_err:
        pop = subprocess.Popen("npm run build-%s --prefix=%s"%(cate, weex_path), shell=True, stdout=f_out, stderr=f_err)
        while pop.poll() != 0:
            end_time = time.time()
            spend_time = int(end_time - start_time)
            print("打包中, 耗时: %ss"% spend_time)
            time.sleep(30)
        end_time = time.time()
        spend_time = int(end_time - start_time)
        print("打包完成! 耗时: %ss"%spend_time)
        # 返回打包文件名称
        if not outputPrefix:
            outputPrefix = "T0x%s" % cate.upper()
        time_str = time.strftime("%Y%m%d%H%M", time.localtime(end_time))
        file_name = "%s_%s.zip" % (outputPrefix, time_str)
        # 判断文件是否存在
        is_file = os.path.isfile(publish_path+file_name)
        if not is_file:
            # 处理有时正好跨1分钟完成的情况
            time_str = str(int(time_str) - 1)
            file_name = "%s_%s.zip" % (outputPrefix, time_str)
            is_file = os.path.isfile(publish_path+file_name)
            if not is_file:
                return "error"
        return DBHandler.saveFileMap(publish_path, file_name)



# 新品配置项处理
def handleSetting(productData={}):
    model = productData.get('model')
    sn8 = productData.get('sN8')
    functionIds = productData.get('functionIds')
    # 查询功能列表和类型列表
    functionList = DBHandler.getFunctionList('electric_heater')
    functionTypeList = DBHandler.getFunctionTypeList('electric_heater')
    # 初始化参数
    func_list_key = []
    func_list_name = []
    ctrl_list = []
    setting = []
    typeKeyDict = { item['typeKey']: item for item in functionTypeList }
    # # todo: 先从functionList将所有对应类型的功能值归类
    # selected_dict = {}
    # for func in functionList:
    #     functionKey = func['functionKey']
    #     functionValue = func['functionValue']
    #     if functionValue and func.get('id') in functionIds and functionKey == functionTypeItem['typeKey']:
    #         value_list.append(functionValue)
    #         selected_dict
    # 遍历功能类型
    for functionTypeItem in functionTypeList:
        value_list = []
        # 从functionList中查找所有对应类型的功能值
        for func in functionList:
            functionKey = func['functionKey']
            functionValue = func['functionValue']
            if functionValue and func.get('id') in functionIds and functionKey == functionTypeItem['typeKey']:
                value_list.append(functionValue)
        # 组装插入字符串
        insertTemplate = functionTypeItem['insertTemplate'] or "%s"
        if functionTypeItem['dataType'] == 'Array':
            # 数组类型
            if len(value_list) == 0 and functionTypeItem['typeKey'] not in ['funcList']: continue # funcList为空也要写，不然会报错
            functionTypeItem['value'] = insertTemplate % "','".join(value_list)
        elif functionTypeItem['typeKey'] == 'config':
            pass
        elif len(value_list) == 1:
            if functionTypeItem['typeKey'] == 'ndReport': # 特殊处理，内胆鲜活度
                if value_list[0] == "tankFresh":
                    functionTypeItem['value'] = 1
                    setting.append({ "value": 1, **typeKeyDict['xhdReport'] })
                elif value_list[0] == "tankFreshTds":
                    functionTypeItem['value'] = 1
                    setting.append({ "value": 2, **typeKeyDict['xhdReport'] })
                else:
                    functionTypeItem['value'] = value_list[0]
            elif functionTypeItem['dataType'] == 'String':
                functionTypeItem['value'] = '"%s"' % value_list[0]
            else:
                functionTypeItem['value'] = value_list[0]
        # 如果非空就加入setting
        if functionTypeItem.get('value'):
            setting.append(functionTypeItem)

    new_line_list = []
    # 型号注释
    new_line_list.append("  // %s \n" % model)
    # SN8配置（配置头）
    new_line_list.append("  '%s'(){return{\n" % sn8)
    # 协议配置
    new_line_list.append('    isNew: true, // 是否采用0214新分段协议\n')
    # 
    setting = sorted(setting, key = lambda i: i['insertPriority'])
    # print(setting)
    for settingItem in setting:
        new_line_list.append('    %s: %s,\n' % (settingItem['typeKey'], settingItem['value']))
    # # 耗材配置
    # new_line_list.append('    // ===耗材配置=== \n')
    # # 功能配置
    # new_line_list.append('    // ===功能配置=== >> %s\n' % '、'.join(func_list_name))
    # （配置尾）
    new_line_list.append("  }},\n")
    return new_line_list
