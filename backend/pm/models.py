from django.db import models

# Create your models here.

# 功能
class FunctionData(models.Model):
    # id = models.CharField(max_length=8, unique=True, primary_key=True)  # 功能id
    functionName = models.CharField(max_length=32)    # 功能名称
    functionKey = models.CharField(max_length=16)  # 功能键名
    typeKey = models.CharField(max_length=16)    # 功能类型（键名）
    productType = models.CharField(max_length=16)    # 产品类型
    isDefault = models.IntegerField()  # 是否默认功能
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)

# 功能类型
class FunctionTypeData(models.Model):
    typeName = models.CharField(max_length=32)    # 功能类型名称
    typeKey = models.CharField(max_length=16)    # 功能类型键名
    desc = models.CharField(max_length=32)    # 功能类型描述
    priority = models.IntegerField()   # 功能显示优先级
    isRequired = models.IntegerField()  # 是否必选
    isMultiple = models.IntegerField()  # 是否多选
    productType = models.CharField(max_length=16)    # 产品类型
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)

# 电控板功能
class ElectricBoardFunctionData(models.Model):
    functionName = models.CharField(max_length=32)    # 电控功能名称
    functionKey = models.CharField(max_length=16)  # 电控功能键名
    typeKey = models.CharField(max_length=16)    # 电控功能类型（键名）
    productType = models.CharField(max_length=16)    # 产品类型
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
    productType = models.CharField(max_length=16)    # 产品类型
    create_time = models.DateTimeField(auto_now_add=True,null=True)
    update_time = models.DateTimeField(auto_now=True,null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)

# 产品数据
class ProductData(models.Model):
    productType = models.CharField(max_length=32)    # 产品类型
    productTypeName = models.CharField(max_length=32)  # 品类名称
    categoryType = models.CharField(max_length=32)
    branch = models.CharField(max_length=32)
    code = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    sN8 = models.CharField(max_length=32)
    lifecycleStage = models.CharField(max_length=32)
    saleChannel = models.CharField(max_length=128, null=True)
    functionIds = models.CharField(max_length=128, null=True)
    scenarioIds = models.CharField(max_length=128, null=True)
    voiceFunctionIds = models.CharField(max_length=128, null=True)
    ecologyEntranceIds = models.CharField(max_length=128, null=True)
    sensorIds = models.CharField(max_length=128, null=True)
    electricBoardFunctionIds = models.CharField(max_length=128, null=True)
    pic = models.CharField(max_length=32, null=True)
    powerBoardCode = models.CharField(max_length=32, null=True)
    displayBoardCode = models.CharField(max_length=32, null=True)
    wifiModuleCode = models.CharField(max_length=32, null=True)
    networkingMode = models.CharField(max_length=32, null=True)
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
    productType = models.CharField(max_length=16)
    productModel = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    createUserId = models.CharField(max_length=16, null=True)
    updateUserId = models.CharField(max_length=16, null=True)