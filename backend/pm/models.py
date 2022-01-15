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
    authCode = models.CharField(max_length=255, blank=True, null=True, db_column="auth_code")
    authName = models.CharField(max_length=255, blank=True, null=True, db_column="auth_name")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_authorization'


class FmDevelopTask(models.Model):
    actorUserId = models.IntegerField(blank=True, null=True, db_column="actor_user_id")
    auditUserIds = models.CharField(max_length=255, blank=True, null=True, db_column="audit_user_ids")
    content = models.CharField(max_length=255, blank=True, null=True)
    currentHandleFinishUserId = models.CharField(max_length=255, blank=True, null=True, db_column="current_handle_finish_user_id")
    currentHandleUserId = models.CharField(max_length=255, blank=True, null=True, db_column="current_handle_user_id")
    currentHandlerRole = models.CharField(max_length=255, blank=True, null=True, db_column="current_handler_role")
    productEcologyEntranceIds = models.CharField(max_length=255, blank=True, null=True, db_column="product_ecology_entrance_ids")
    productFunctionIds = models.CharField(max_length=255, blank=True, null=True, db_column="product_function_ids")
    productModel = models.CharField(max_length=255, blank=True, null=True, db_column="product_model")
    productScenarioIds = models.CharField(max_length=255, blank=True, null=True, db_column="product_scenario_ids")
    productSensorIds = models.CharField(max_length=255, blank=True, null=True, db_column="product_sensor_ids")
    productVoiceFunctionIds = models.CharField(max_length=255, blank=True, null=True, db_column="product_voice_function_ids")
    sponsorTime = models.DateTimeField(blank=True, null=True, db_column="sponsor_time")
    sponsorUserId = models.IntegerField(blank=True, null=True, db_column="sponsor_user_id")
    status = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_develop_task'


class FmDevelopTaskPruduct(models.Model):
    developTaskId = models.IntegerField(blank=True, null=True, db_column="develop_task_id")
    productType = models.CharField(max_length=255, null=True, db_column="product_type")
    productCode = models.CharField(max_length=255, blank=True, null=True, db_column="product_code")
    productSn8 = models.CharField(max_length=255, blank=True, null=True, db_column="product_sn8")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_develop_task_product'


class FmDevelopTaskAuditGroup(models.Model):
    createUserId = models.IntegerField(blank=True, null=True, db_column="create_user_id")
    groupName = models.CharField(max_length=255, blank=True, null=True, db_column="group_name")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_develop_task_audit_group'


class FmDevelopTaskAuditGroupUser(models.Model):
    auditGroupId = models.IntegerField(blank=True, null=True, db_column="audit_group_id")
    userId = models.IntegerField(blank=True, null=True, db_column="user_id")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_develop_task_audit_group_user'


class FmDevelopTaskProcessContent(models.Model):
    developTaskId = models.IntegerField(blank=True, null=True, db_column="develop_task_id")
    operation = models.CharField(max_length=255, blank=True, null=True)
    opinion = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    userId = models.IntegerField(blank=True, null=True, db_column="user_id")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_develop_task_process_content'


class FmDictionary(models.Model):
    keyCode = models.CharField(max_length=255, blank=True, null=True, db_column="key_code")
    keyName = models.CharField(max_length=255, blank=True, null=True, db_column="key_name")
    valueCode = models.CharField(max_length=255, blank=True, null=True, db_column="value_code")
    valueName = models.CharField(max_length=255, blank=True, null=True, db_column="value_name")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_dictionary'


class FmEncologyEntrance(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_encology_entrance'


class FmFunction(models.Model):
    functionName = models.CharField(max_length=255, blank=True, null=True, db_column="function_name")
    typeCode = models.CharField(max_length=255, blank=True, null=True, db_column="type_code")
    functionDesc = models.CharField(max_length=255, null=True, db_column="function_desc")    # 功能描述
    functionValue = models.CharField(max_length=255, null=True, db_column="function_value")  # 功能值
    functionKey = models.CharField(max_length=255, null=True, db_column="function_key")    # 功能键名（类型）
    isDefault = models.IntegerField(default=0, db_column="is_default")  # 是否默认功能
    isDisable = models.IntegerField(default=0, db_column="is_disable")  # 是否禁用
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_function'


# 功能类型
class FmFunctionType(models.Model):
    typeName = models.CharField(max_length=255, db_column="type_name")    # 功能类型名称
    typeKey = models.CharField(max_length=255, db_column="type_key")    # 功能类型键名
    desc = models.CharField(max_length=255)    # 功能类型描述
    displayPriority = models.IntegerField(default=0, db_column="display_priority")   # 功能显示优先级
    insertPriority = models.IntegerField(default=0, db_column="insert_priority")   # 功能插入代码的优先级
    isRequired = models.IntegerField(default=0, db_column="is_required")  # 是否必选
    isMultiple = models.IntegerField(default=0, db_column="is_multiple")  # 是否多选
    componentType = models.CharField(max_length=255, null=True, db_column="component_type")    # 组件类型
    productType = models.CharField(max_length=255, db_column="product_type")    # 产品类型
    insertTemplate = models.CharField(max_length=255, null=True, db_column="insert_template")    # 功能插入代码的模板，用于添加前缀后缀
    dataType = models.CharField(max_length=16, default="String", db_column="data_type")  # 数据类型，Object，Boolean, Array, Number, String
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_function_type'


class FmProductEcologyEntrance(models.Model):
    ecologyEntranceId = models.IntegerField(blank=True, null=True, db_column="ecology_entrance_id")
    productCode = models.CharField(max_length=255, blank=True, null=True, db_column="product_code")
    productSn8 = models.CharField(max_length=255, blank=True, null=True, db_column="product_sn8")
    productVersion = models.CharField(max_length=255, blank=True, null=True, db_column="product_version")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_product_ecology_entrance'


class FmProductFunction(models.Model):
    functionId = models.IntegerField(blank=True, null=True, db_column="function_id")
    productCode = models.CharField(max_length=255, blank=True, null=True, db_column="product_code")
    productSn8 = models.CharField(max_length=255, blank=True, null=True, db_column="product_sn8")
    productVersion = models.CharField(max_length=255, blank=True, null=True, db_column="product_version")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_product_function'


class FmProductInfo(models.Model):
    branch = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    lifecycleStage = models.CharField(max_length=255, blank=True, null=True, db_column="lifecycle_stage")
    model = models.CharField(max_length=255, blank=True, null=True)
    productCategory = models.CharField(max_length=255, blank=True, null=True, db_column="product_category")
    productType = models.CharField(max_length=255, blank=True, null=True, db_column="product_type")
    saleChannel = models.CharField(max_length=255, blank=True, null=True, db_column="sale_channel")
    sn8 = models.CharField(max_length=255, blank=True, null=True)
    pic = models.CharField(max_length=255, blank=True, null=True)
    productVersion = models.CharField(max_length=255, blank=True, null=True, db_column="product_version")
    dishwasherProperty = models.CharField(max_length=5000, blank=True, null=True, db_column="dishwasher_property")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_product_info'


class FmProductScenario(models.Model):
    productCode = models.CharField(max_length=255, blank=True, null=True, db_column="product_code")
    scenarioId = models.IntegerField(blank=True, null=True, db_column="scenario_id")
    productSn8 = models.CharField(max_length=255, blank=True, null=True, db_column="product_sn8")
    productVersion = models.CharField(max_length=255, blank=True, null=True, db_column="product_version")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_product_scenario'


class FmProductSensor(models.Model):
    productCode = models.CharField(max_length=255, blank=True, null=True, db_column="product_code")
    sensorId = models.IntegerField(blank=True, null=True, db_column="sensor_id")
    productSn8 = models.CharField(max_length=255, blank=True, null=True, db_column="product_sn8")
    productVersion = models.CharField(max_length=255, blank=True, null=True, db_column="product_version")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_product_sensor'


class FmProductVoiceFunction(models.Model):
    productCode = models.CharField(max_length=255, blank=True, null=True, db_column="product_code")
    voiceFunction_id = models.IntegerField(blank=True, null=True, db_column="voice_function_id")
    productSn8 = models.CharField(max_length=255, blank=True, null=True, db_column="product_sn8")
    productVersion = models.CharField(max_length=255, blank=True, null=True, db_column="product_version")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_product_voice_function'


# 电控板功能
class FmProductElectricBoardInfo(models.Model):
    productCode = models.CharField(max_length=255, blank=True, null=True, db_column="product_code")
    productSn8 = models.CharField(max_length=255, blank=True, null=True, db_column="product_sn8")
    productVersion = models.CharField(max_length=255, blank=True, null=True, db_column="product_version")
    infoName = models.CharField(max_length=255, db_column="info_name")    # 电控信息名称
    infoKey = models.CharField(max_length=255, db_column="info_key")  # 电控信息键名
    infoValue = models.CharField(max_length=255, db_column="info_value") # 电控信息值
    productType = models.CharField(max_length=255, db_column="product_type")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_function_electric_board_info'


class FmScenario(models.Model):
    scenarioName = models.CharField(max_length=255, blank=True, null=True, db_column="scenario_name")
    typeCode = models.CharField(max_length=255, blank=True, null=True, db_column="type_code")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_scenario'


class FmSensor(models.Model):
    sensorName = models.CharField(max_length=255, blank=True, null=True, db_column="sensor_name")
    typeCode = models.CharField(max_length=255, blank=True, null=True, db_column="type_code")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_sensor'


class FmUser(models.Model):
    avator = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=1024, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    userName = models.CharField(max_length=255, blank=True, null=True, db_column="user_name")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_user'


class FmUserAuthorization(models.Model):
    authId = models.IntegerField(blank=True, null=True, db_column="auth_id")
    userId = models.IntegerField(blank=True, null=True, db_column="user_id")
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_user_authorization'


class FmVoiceFunction(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_voice_function'


# 电控信息类型
class FmElectricBoardInfo(models.Model):
    typeName = models.CharField(max_length=255, db_column="type_name")    # 功能类型名称
    typeKey = models.CharField(max_length=255, db_column="type_key")    # 功能类型键名
    desc = models.CharField(max_length=255, null=True)    # 功能类型描述
    displayPriority = models.IntegerField(default=0, db_column="display_priority")   # 功能显示优先级
    isRequired = models.IntegerField(default=0, db_column="is_required")  # 是否必选
    productType = models.CharField(max_length=255, db_column="product_type")    # 产品类型
    dataType = models.CharField(max_length=16, default="String", db_column="data_type")  # 数据类型，Object，Boolean, Array, Number, String
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_column="create_date_time")
    updateDateTime = models.DateTimeField(auto_now=True, blank=True, null=True, db_column="update_date_time")

    class Meta:
        # managed = False
        db_table = 'fm_electric_board_info'


# ========== 自己创建的 ============

# 功能，可废弃
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

# 功能类型, 已迁移，可废弃
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
    dataType = models.CharField(max_length=16, default="String", db_column="data_type")  # 数据类型，Object，Boolean, Array, Number, Srting
    isDefault = models.IntegerField()  # 是否默认电控功能
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    create_user_id = models.CharField(max_length=16, null=True)
    update_user_id = models.CharField(max_length=16, null=True)
    # 电控功能
    # powerBoardCode = models.CharField(max_length=32, null=True)
    # displayBoardCode = models.CharField(max_length=32, null=True)
    # wifiModuleCode = models.CharField(max_length=32, null=True)
    # networkingMode = models.CharField(max_length=32, null=True)

    # hasBuzzer = models.IntegerField(default=0, verbose_name='是否有蜂鸣器')  # 是否有蜂鸣器
    # hasFlowSensor = models.IntegerField(default=0)  # 是否有流量传感器
    # hasElectricLeakageProtect = models.IntegerField(default=0)  # 是否有漏电断电保护
    # heatingTubeType = models.IntegerField(null=True)  # 加热管配置

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

# 任务数据, 已迁移，可废弃
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