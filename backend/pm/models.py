from django.db import models

# Create your models here.

# 功能
class FunctionData(models.Model):
    # id = models.CharField(max_length=8, unique=True, primary_key=True)  # 功能id
    functionName = models.CharField(max_length=32)    # 功能名称
    functionDesc = models.CharField(max_length=32, null=True)    # 功能描述
    functionKey = models.CharField(max_length=32)  # 功能键名
    typeKey = models.CharField(max_length=32)    # 功能类型（键名）
    productType = models.CharField(max_length=32)    # 产品类型
    isDefault = models.IntegerField(default=0)  # 是否默认功能
    isDisable = models.IntegerField(default=0)  # 是否禁用
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)

# 功能类型
class FunctionTypeData(models.Model):
    typeName = models.CharField(max_length=32)    # 功能类型名称
    typeKey = models.CharField(max_length=32)    # 功能类型键名
    desc = models.CharField(max_length=32)    # 功能类型描述
    priority = models.IntegerField()   # 功能显示优先级
    isRequired = models.IntegerField()  # 是否必选
    isMultiple = models.IntegerField()  # 是否多选
    productType = models.CharField(max_length=32)    # 产品类型
    dataType = models.CharField(max_length=16, default="String")  #    功能类型，Object，Boolean, Array, Number, Srting
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)

# 电控板功能
class ElectricBoardFunctionData(models.Model):
    functionName = models.CharField(max_length=32)    # 电控功能名称
    functionKey = models.CharField(max_length=16)  # 电控功能键名
    typeKey = models.CharField(max_length=16)    # 电控功能类型（键名）
    productType = models.CharField(max_length=32)    # 产品类型
    isDefault = models.IntegerField()  # 是否默认电控功能
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)

# 电控板功能类型
class ElectricBoardFunctionTypeData(models.Model):
    typeName = models.CharField(max_length=32)    # 电控类型名称
    typeKey = models.CharField(max_length=16)    # 电控类型键名
    desc = models.CharField(max_length=32)    # 电控类型描述
    priority = models.IntegerField()   # 显示优先级
    isRequired = models.IntegerField()  # 是否必选
    isMultiple = models.IntegerField()  # 是否多选
    productType = models.CharField(max_length=32)    # 产品类型
    create_time = models.DateTimeField(auto_now_add=True,null=True)
    update_time = models.DateTimeField(auto_now=True,null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)

# 产品数据
class ProductData(models.Model):
    # 产品基本信息
    productType = models.CharField(max_length=32)    # 产品类型
    productTypeName = models.CharField(max_length=32)  # 品类名称
    categoryType = models.CharField(max_length=32)
    branch = models.CharField(max_length=32)
    code = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    sN8 = models.CharField(max_length=32)
    lifecycleStage = models.CharField(max_length=32) # 产品生命周期
    saleChannel = models.CharField(max_length=128, null=True)
    functionIds = models.CharField(max_length=128, null=True)
    scenarioIds = models.CharField(max_length=128, null=True)
    voiceFunctionIds = models.CharField(max_length=128, null=True)
    ecologyEntranceIds = models.CharField(max_length=128, null=True)
    sensorIds = models.CharField(max_length=128, null=True)
    # 电控功能
    electricBoardFunctionIds = models.CharField(max_length=128, null=True)
    pic = models.CharField(max_length=32, null=True)
    powerBoardCode = models.CharField(max_length=32, null=True)
    displayBoardCode = models.CharField(max_length=32, null=True)
    wifiModuleCode = models.CharField(max_length=32, null=True)
    networkingMode = models.CharField(max_length=32, null=True)
    hasBuzzer = models.IntegerField(default=0, verbose_name='是否有蜂鸣器')  # 是否有蜂鸣器
    hasFlowSensor = models.IntegerField(default=0)  # 是否有流量传感器
    hasElectricLeakageProtect = models.IntegerField(default=0)  # 是否有漏电断电保护
    heatingTubeType = models.IntegerField(null=True)  # 加热管配置
    # 额外数据
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)

# 任务数据
class TaskData(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    actorUserId = models.CharField(max_length=128)
    auditGroupId = models.CharField(max_length=128)
    auditGroupUserIds = models.CharField(max_length=128)
    productType = models.CharField(max_length=32)
    productModel = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    createUserId = models.CharField(max_length=16, null=True)
    updateUserId = models.CharField(max_length=16, null=True)

# 加热管类型
class HeatingTubeTypeData(models.Model):
    productType = models.CharField(max_length=32)    # 产品类型
    name = models.CharField(max_length=32)    # 类型名称
    tubeCount = models.IntegerField()  # 加热管数量
    topTubePower = models.IntegerField()  # 顶部加热管功率
    middleTubePower = models.IntegerField()  # 中部加热管功率
    bottomTubePower = models.IntegerField()  # 底部加热管功率
    onlyTubePower = models.IntegerField()  # 唯一加热管功率
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)

# WIFI模块类型
class WifiModuleTypeData(models.Model):
    code = models.CharField(max_length=32, unique=True)      # 编码
    networkingMode = models.CharField(max_length=32)    # 配网方式
    mcuType = models.CharField(max_length=16)    # MCU型号
    desc = models.CharField(max_length=32, null=True)    # 备注
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)