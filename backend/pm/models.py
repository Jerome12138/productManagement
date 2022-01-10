from django.db import models

# Create your models here.

# ============ 来自数据库导入 ==============
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class FmAuthorization(models.Model):
    auth_code = models.CharField(max_length=255, blank=True, null=True)
    auth_name = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_authorization'


class FmDevelopTask(models.Model):
    actor_user_id = models.IntegerField(blank=True, null=True)
    audit_user_ids = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    current_handle_finish_user_id = models.CharField(max_length=255, blank=True, null=True)
    current_handle_user_id = models.CharField(max_length=255, blank=True, null=True)
    current_handler_role = models.CharField(max_length=255, blank=True, null=True)
    product_ecology_entrance_ids = models.CharField(max_length=255, blank=True, null=True)
    product_function_ids = models.CharField(max_length=255, blank=True, null=True)
    product_model = models.CharField(max_length=255, blank=True, null=True)
    product_scenario_ids = models.CharField(max_length=255, blank=True, null=True)
    product_sensor_ids = models.CharField(max_length=255, blank=True, null=True)
    product_voice_function_ids = models.CharField(max_length=255, blank=True, null=True)
    sponsor_time = models.DateTimeField(blank=True, null=True)
    sponsor_user_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_develop_task'


class FmDevelopTaskAuditGroup(models.Model):
    create_user_id = models.IntegerField(blank=True, null=True)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_develop_task_audit_group'


class FmDevelopTaskAuditGroupUser(models.Model):
    audit_group_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_develop_task_audit_group_user'


class FmDevelopTaskProcessContent(models.Model):
    develop_task_id = models.IntegerField(blank=True, null=True)
    operation = models.CharField(max_length=255, blank=True, null=True)
    opinion = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_develop_task_process_content'


class FmDictionary(models.Model):
    key_code = models.CharField(max_length=255, blank=True, null=True)
    key_name = models.CharField(max_length=255, blank=True, null=True)
    value_code = models.CharField(max_length=255, blank=True, null=True)
    value_name = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_dictionary'


class FmEncologyEntrance(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_encology_entrance'


class FmFunction(models.Model):
    function_name = models.CharField(max_length=255, blank=True, null=True)
    type_code = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_function'


class FmProductEcologyEntrance(models.Model):
    ecology_entrance_id = models.IntegerField(blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)
    product_sn8 = models.CharField(max_length=255, blank=True, null=True)
    product_version = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_product_ecology_entrance'


class FmProductFunction(models.Model):
    function_id = models.IntegerField(blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)
    product_sn8 = models.CharField(max_length=255, blank=True, null=True)
    product_version = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_product_function'


class FmProductInfo(models.Model):
    branch = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    lifecycle_stage = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    product_category = models.CharField(max_length=255, blank=True, null=True)
    product_type = models.CharField(max_length=255, blank=True, null=True)
    sale_channel = models.CharField(max_length=255, blank=True, null=True)
    sn8 = models.CharField(max_length=255, blank=True, null=True)
    pic = models.CharField(max_length=255, blank=True, null=True)
    product_version = models.CharField(max_length=255, blank=True, null=True)
    dishwasher_property = models.CharField(max_length=5000, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_product_info'


class FmProductScenario(models.Model):
    product_code = models.CharField(max_length=255, blank=True, null=True)
    scenario_id = models.IntegerField(blank=True, null=True)
    product_sn8 = models.CharField(max_length=255, blank=True, null=True)
    product_version = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_product_scenario'


class FmProductSensor(models.Model):
    product_code = models.CharField(max_length=255, blank=True, null=True)
    sensor_id = models.IntegerField(blank=True, null=True)
    product_sn8 = models.CharField(max_length=255, blank=True, null=True)
    product_version = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_product_sensor'


class FmProductVoiceFunction(models.Model):
    product_code = models.CharField(max_length=255, blank=True, null=True)
    voice_function_id = models.IntegerField(blank=True, null=True)
    product_sn8 = models.CharField(max_length=255, blank=True, null=True)
    product_version = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_product_voice_function'


class FmScenario(models.Model):
    scenario_name = models.CharField(max_length=255, blank=True, null=True)
    type_code = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_scenario'


class FmSensor(models.Model):
    sensor_name = models.CharField(max_length=255, blank=True, null=True)
    type_code = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_sensor'


class FmUser(models.Model):
    avator = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=1024, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_user'


class FmUserAuthorization(models.Model):
    auth_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_user_authorization'


class FmVoiceFunction(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    create_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'fm_voice_function'


# ========== 自己创建的 ============

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