from git.repo import Repo
import os, time
import subprocess
from . import DBHandler

weex_path = "/Users/jerome/Git/weex-kh-widgets"

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
def compile():
    log_time = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    stdout_file_name = "pm/log/compile_log_%s_stdout.txt"%log_time
    stderr_file_name = "pm/log/compile_log_%s_stderr.txt"%log_time
    with open(stdout_file_name,"wb") as f_out, open(stderr_file_name,"wb") as f_err:
        pop = subprocess.Popen("npm run build-e2 --prefix=C:\DATA\Code\Git\weex-kh-widgets", shell=True, stdout=f_out, stderr=f_err)
        while pop.poll() != 0:
            print("尚未完成")
            time.sleep(30)

# 新品配置项处理
def handleSetting(productData={}):
    model = productData.get('model')
    sn8 = productData.get('sN8')
    functionIds = productData.get('functionIds')
    functionList = DBHandler.getFunctionList('electric_heater')
    func_list_key = []
    func_list_name = []
    ctrl_list = []
    appointType = ''
    mbReport = ''
    lxReport = ''
    ndReport = ''
    xhdReport = ''
    hotWaterType = ''
    for func in functionList:
        if func.get('id') in functionIds:
            if func.get('typeKey') == 'function':
                func_list_key.append(func['functionKey'])
                func_list_name.append(func['functionName'])
            elif func.get('typeKey') == 'controlFunc':
                ctrl_list.append(func['functionKey'])
            elif func.get('typeKey') == 'appoint':
                appointType = func['functionKey']
            elif func.get('typeKey') == 'consumableMb':
                mb_value_dict = {
                    "mbElectronic": '0',
                    "mbPercent": '1',
                    "mbCloud": '2',
                    "mbAC": '3',
                }
                mbReport = mb_value_dict.get(func['functionKey'])
            elif func.get('typeKey') == 'consumableFilter':
                lx_value_dict = {
                    "filterElec": '1',
                    "filterCloud": '2',
                }
                lxReport = lx_value_dict.get(func['functionKey'])
            elif func.get('typeKey') == 'consumableTank':
                nd_value_dict = {
                    "tankNoClean": '0',
                    "tankElecDay": '1',
                    "tankFresh": '1',
                    "tankFreshTds": '1',
                    "tankCloud": '3',
                }
                ndReport = nd_value_dict.get(func['functionKey'])
                if func['functionKey'] == "tankFresh":
                    xhdReport = '1'
                elif func['functionKey'] == "tankFreshTds":
                    xhdReport = '2'
            elif func.get('typeKey') == 'hotWaterType':
                hotWaterType = func['functionKey']

    new_line_list = []
    # 型号注释
    new_line_list.append("  // %s \n" % model)
    # SN8配置（配置头）
    new_line_list.append("  '%s'(){return{\n" % sn8)
    # 协议配置
    new_line_list.append('    isNew: true, // 是否采用0214新分段协议\n')
    # 耗材配置
    new_line_list.append('    // ===耗材配置=== \n')
    if mbReport:
        new_line_list.append('    mbReport: %s,\n' % mbReport)
    if lxReport:
        new_line_list.append('    lxReport: %s,\n' % lxReport)
    if ndReport:
        new_line_list.append('    ndReport: %s,\n' % ndReport)
    if xhdReport:
        new_line_list.append('    xhdReport: %s,\n' % xhdReport)
    # 功能配置
    new_line_list.append('    // ===功能配置=== >> %s\n' % '、'.join(func_list_name))
    new_line_list.append("    funcList: getFuncList(['%s']),\n" % "','".join(func_list_key))
    # 控制栏配置
    if ctrl_list:
        new_line_list.append('    controlFunc: '+str(ctrl_list)+",\n")
    # 热水量配置
    if hotWaterType:
        new_line_list.append('    hotWaterType: "%s",\n' % hotWaterType)
    # 预约配置
    if appointType:
        new_line_list.append('    appointType: "%s",\n' % appointType)
    # （配置尾）
    new_line_list.append("  }},\n")
    return new_line_list
