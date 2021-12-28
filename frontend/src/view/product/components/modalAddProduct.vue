<template>
  <Modal
    :styles="{width: '820px'}"
    v-model="visible"
    title="添加任务"
    @on-cancel="closeModal"
    mask
    :mask-closable=false
    :loading="loading">
    <!-- <Steps :current="currentStep">
        <Step title="项目信息"></Step>
        <Step title="产品基本信息"></Step>
        <Step title="电控信息"></Step>
        <Step title="APP功能"></Step>
        <Step title="其他功能"></Step>
    </Steps> -->
    <Form :model="productData" label-position="left" :label-width="88">
      <Tabs v-model="currentStep">
          <Tab-pane label="项目信息" v-if="false">
            <Form ref="taskManage" :model="taskData" label-position="left" :rules="taskRuleValidate" :label-width="75">
              <Row :gutter="8">
                <Col span="24">
                  <FormItem label="标题:" prop="title">
                    <Input v-model="taskData.title" :maxlength="50" placeholder="请输入50个字符以内的任务标题" autosize></Input>
                  </FormItem>
                </Col>
              </Row>
              <Row :gutter="8">
                <Col span="24">
                  <FormItem label="内容:" prop="content">
                    <Input v-model="taskData.content" type="textarea" :maxlength="500" placeholder="请输入500个字符以内的任务内容"
                            autosize></Input>
                  </FormItem>
                </Col>
              </Row>
              <Row :gutter="8">
                <Col span="12">
                  <FormItem label="产品类型:" prop="productType">
                    <Select v-model="taskData.productType" placeholder="请选择产品类型" clearable not-found-text="暂无产品类型" @on-change="changeProductType">
                      <Option v-for="item in allProductType" :value="item.code" :key="item.code">{{ item.value }}</Option>
                    </Select>
                  </FormItem>
                </Col>
                <Col span="10">
                  <FormItem label="产品型号:" prop="productModel">
                    <Select v-model="taskData.productModel" placeholder="请选择产品型号" clearable not-found-text="请先选择产品类型，并确认已选类型有产品" @on-change="changeProductModel">
                      <Option v-for="item in allProductModel[taskData.productType]" :value="item.model" :label="item.model" :key="item.model" >
                        <span>{{ item.model }}</span>
                        <span style="float:right;color:#ccc">{{ item.sN8 }}</span>
                      </Option>
                    </Select>
                  </FormItem>
                </Col>
                <Col span="2" :gutter="0" style="margin-top:4px">
                  <Button shape="circle" size="small">添加产品</Button>
                </Col>
              </Row>
              <Row :gutter="8">
                <Col span="6">
                  <FormItem label="项目经理:">
                    <Input v-model="taskData.pm" :maxlength="50" placeholder="填写项目经理姓名" clearable></Input>
                  </FormItem>
                </Col>
                <Col span="6">
                  <FormItem label="产品企划:">
                    <Input v-model="taskData.planner" :maxlength="50" placeholder="填写产品企划姓名" clearable></Input>
                  </FormItem>
                </Col>
                <Col span="6">
                  <FormItem label="电控硬件:">
                    <Input v-model="taskData.hardwareEngineer" :maxlength="50" placeholder="填写电控硬件工程师姓名" clearable></Input>
                  </FormItem>
                </Col>
                <Col span="6">
                  <FormItem label="电控软件:">
                    <Input v-model="taskData.softwareEngineer" :maxlength="50" placeholder="填写电控软件工程师姓名" clearable></Input>
                  </FormItem>
                </Col>
              </Row>
              <Row :gutter="8">
                <Col span="12">
                  <FormItem label="审核组:" prop="auditGroupId">
                    <span style="max-width: 100%; display: inline-block; overflow-wrap: break-word;text-align: left;">
                      {{ groupIdToUserName[taskData.auditGroupId] }}
                    </span>
                    <Select clearable v-model="taskData.auditGroupId" placeholder="请选择审核组">
                      <Option v-for="item in auditGroupList" :value="item.id" :key="item.id">{{ item.groupName }}</Option>
                    </Select>
                  </FormItem>
                </Col>
                <Col span="12">
                  <FormItem label="执行人:" prop="actorUserId">
                    <Select clearable v-model="taskData.actorUserId" placeholder="请选择执行人">
                      <Option v-for="item in allUser" :value="item.id" :key="item.id">{{ item.userName }}</Option>
                    </Select>
                  </FormItem>
                </Col>
              </Row>
            </Form>
          </Tab-pane>
          <Tab-pane label="产品基本信息">
            <Row :gutter="16">
              <Col span="12">
                <FormItem label="产品编码">
                  <Input :disabled="isUpdate" v-model="productData.code" :maxlength="50" placeholder="请输入产品编号，50个字符以内" clearable></Input>
                </FormItem>
              </Col>
              <Col span="12">
                <FormItem label="产品型号">
                  <Input :disabled="isUpdate" v-model="productData.model" :maxlength="50" placeholder="请输入产品型号，50个字符以内" clearable></Input>
                </FormItem>
              </Col>
            </Row>
            <Row :gutter="16">
              <Col span="12">
                <FormItem label="SN8">
                  <Input :disabled="isUpdate" v-model="productData.sN8" :maxlength="50" placeholder="请输入产品SN8，8个字符" clearable></Input>
                </FormItem>
              </Col>
              <Col span="12">
                <FormItem label="品牌">
                  <Select v-model="productData.branch" placeholder="请选择品牌" filterable transfer>
                    <Option v-for="item in branchList" :value="item.code" :key="item.code">{{ item.value }}</Option>
                  </Select>
                </FormItem>
              </Col>
            </Row>
            <Row :gutter="16">
              <Col span="12">
                <FormItem label="生态入口">
                  <Select v-model="productData.ecologyEntranceIds" placeholder="请选择产品生态入口" multiple filterable transfer>
                    <Option v-for="item in allEcologyEntranceList" :value="item.id" :key="item.id">{{ item.name }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <!-- todo: 扩展，可复制功能 -->
              <!-- <Col span="12">
                <FormItem label="APP借用SN8">
                  <Select v-model="productData.appCopySn8" placeholder="APP完全借用可选择借用机型的SN8，可选" filterable transfer>
                    <Option v-for="item in allSn8List" :value="item.id" :key="item.id">{{ item.sn8 }}</Option>
                  </Select>
                </FormItem>
              </Col> -->
            </Row>
          </Tab-pane>
          <Tab-pane label="电控信息">
            <Row :gutter="16">
              <Col span="12">
                <FormItem label="电源板编码">
                  <Input :disabled="isUpdate" v-model="productData.powerBoardCode" :maxlength="50" placeholder="请输入电源板编码，50个字符以内" clearable></Input>
                </FormItem>
              </Col>
              <Col span="12">
                <FormItem label="显示板编码">
                  <Input :disabled="isUpdate" v-model="productData.displayBoardCode" :maxlength="50" placeholder="请输入显示板编码，50个字符以内" clearable></Input>
                </FormItem>
              </Col>
            </Row>
            <Row :gutter="16">
              <Col span="12">
                <FormItem label="WiFi模块编码">
                  <Input :disabled="isUpdate" v-model="productData.wifiModuleCode" :maxlength="50" placeholder="请输入WiFi模块编码，50个字符以内" clearable></Input>
                </FormItem>
              </Col>
              <Col span="12">
              <!-- 待处理，WiFi模块单独维护 -->
                <FormItem label="配网方式">
                  <Input :disabled="true" v-model="productData.networkingMode" :maxlength="50" placeholder="输入WiFi模块编码后将自动匹配配网方式" clearable></Input>
                </FormItem>
              </Col>
            </Row>
            <Row :gutter="16">
              <Col span="12">
                <FormItem label="蜂鸣器">
                  <Input v-model="productData.hasBuzzer" :maxlength="50" placeholder="请选择是否有蜂鸣器" clearable></Input>
                </FormItem>
              </Col>
              <Col span="12">
                <FormItem label="流量传感器">
                  <Input v-model="productData.hasFlowSensor" :maxlength="50" placeholder="请选择流量传感器配置" clearable></Input>
                </FormItem>
              </Col>
            </Row>
            <Row :gutter="16">
              <Col span="12">
                <FormItem label="漏电断电">
                  <Input v-model="productData.hasElectricLeakageProtect" :maxlength="50" placeholder="请选择是否有流量传感器" clearable></Input>
                </FormItem>
              </Col>
              <Col span="12">
                <FormItem label="加热管">
                  <Input v-model="productData.hasBuzzer" :maxlength="50" placeholder="请选择加热管配置" clearable></Input>
                </FormItem>
              </Col>
            </Row>
          </Tab-pane>
          <Tab-pane label="APP功能">
            <Row :gutter="16" v-for="(colList,index) in functionTypeListRow" :key="index">
              <Col span="12">
                <FormItem :label="colList[0].title">
                  <Select v-model="functionIdList[index*2]" :placeholder="`请选择${colList[0].typeName}`" :multiple="!!colList[0].isMultiple" filterable clearable transfer>
                    <Option v-for="item in getFunctionListByType(colList[0].typeKey)" :value="item.id" :key="item.id">
                      {{ item.functionName }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <Col span="12" v-if="colList.length >1">
                <FormItem :label="colList[1].title">
                  <Select v-model="functionIdList[index*2+1]" :placeholder="`请选择${colList[1].typeName}`" :multiple="!!colList[1].isMultiple" filterable clearable transfer>
                    <Option v-for="item in getFunctionListByType(colList[1].typeKey)" :value="item.id" :key="item.id">{{ item.functionName }}</Option>
                  </Select>
                </FormItem>
              </Col>
            </Row>
          </Tab-pane>
          <Tab-pane label="时间节点">
          </Tab-pane>
      </Tabs>
    </Form>
    <div slot="footer">
      <Button style="margin-right: 8px" @click="cancelSaveProduct">取消</Button>
      <Button v-if="currentStep != 0" style="margin-right: 8px" @click="currentStep-=1">上一步</Button>
      <Button v-if="currentStep == 3" type="primary" @click="saveProduct">保存</Button>
      <Button v-else type="primary" @click="currentStep+=1">下一步</Button>
    </div>
  </Modal>
</template>

<script>
import {
  deleteProductById,
  queryProduct,
  getScenario,
  getProductCategoryByProductType,
  getProductTypeByTypeCode,
  getBranchList,
  getFunctionByType,
  getFunctionType,
  saveProduct,
  getVoiceFunction,
  getSensorByType,
  getEcologyEntrance,
  getProductType,
  getProductModel,
  getAllUserIdAndName,
  queryAuditGroupByUserId
} from '@/api/data'
import { hasOneOf } from '@/libs/tools'
import store from '@/store'
import { getToken, setToken } from '@/libs/util'
import config from '@/config'

export default {
  props: {
    isUpdate: {
      type: Boolean,
      default: false
    },
    value: {
      type: Boolean,
      default: false
    },
    propTaskData: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      uploadMethod: config.baseUrl.pro + 'product/uploadOperationPanelPic',
      viewPicContext: config.baseUrl.pro + 'upload/',
      progressPercent: 0,
      uploadLoading: false,
      file: null,
      showProgress: false,
      uploadDataCount: 0,
      importTotal: 0,
      importErrorTotal: 0,
      invalidData: [],
      tableLoading: false,
      categoryNameToProductType: {},
      categoryNameToCategoryType: {},
      branchNameToBranchCode: {},
      productTypeToScenNameAndId: {},
      productTypeToFunctionList: {},
      productTypeToFuncNameAndId: {},
      productTypeToCategory: {},
      voiceFunctionNameToId: {},
      ecologyEntranceNameToId: {},
      sensorNameToId: {},
      searchLoading: false,
      productType: '',
      productTypeName: '',
      tableDataCount: 0,
      exportLoading: false,
      selectDatas: [],
      styles: {
        height: 'calc(100% - 55px)',
        overflow: 'auto',
        paddingBottom: '53px',
        position: 'static'
      },
      viewPicStyles: {
        maxWidth: '100%',
        width: 'fit-content',
        height: 'auto'
      },
      productData: {
        productType: this.productType,
        productTypeName: '',
        id: '',
        categoryType: '',
        branch: '',
        code: '',
        model: '',
        sN8: '',
        lifecycleStage: '',
        saleChannel: '',
        functionIds: [],
        scenarioIds: [],
        voiceFunctionIds: [],
        ecologyEntranceIds: [],
        sensorIds: [],
        pic: ''
      },
      categoryList: [],
      branchList: [],
      functionList: [],
      scenarioList: [],
      allSensorList: [],
      allVoiceFunctionList: [],
      allEcologyEntranceList: [],
      drawerTitle: '添加产品',
      productTypeToAuth: {
        electric_heater: 'product_electric_heater',
        gas_heater_stove: 'product_gas_heater_stove',
        water_purification: 'product_water_purification',
        water_drink: 'product_water_drink',
        rang_hood_type: 'product_rang_hood_type',
        integrated_gas_combined_kitchen: 'product_integrated_gas_combined_kitchen',
        diswasher_type: 'product_diswasher_type',
        disinfection_cabinet_type: 'product_disinfection_cabinet_type',
        gas_stove: 'product_gas_stove',
        gas_combined_kitchen: 'product_gas_combined_kitchen'
      },
      productTypeToTypeName: {
        electric_heater: '电热水器',
        gas_heater_stove: '燃气热水器',
        water_purification: '净水机',
        water_drink: '饮水机(含净饮机)',
        rang_hood_type: '吸油烟机',
        integrated_gas_combined_kitchen: '集成灶',
        diswasher_type: '洗碗机',
        disinfection_cabinet_type: '消毒柜',
        gas_stove: '燃气炉',
        gas_combined_kitchen: '燃气灶(含组合灶)'
      },
      uploadList: [],
      imgName: '',
      visible: this.value,
      columns: [],
      tableData: [],
      currentStep: 0,
      allSn8List: [],
      functionIds1: [],
      functionIds2: [],
      functionIds3: [],
      functionIds4: [],
      functionIds5: [],
      functionIds6: [],
      functionIds7: [],
      loading: false,
      functionTypeList: [],
      functionIdList: [],
      // 任务管理
      taskData: {},
      taskRuleValidate: {
        title: { required: true, message: '标题不能为空', trigger: 'blur' },
        content: { required: true, message: '内容不能为空', trigger: 'blur' },
        auditGroupId: { required: true, type: 'number', message: '审核组不能为空', trigger: 'change' },
        actorUserId: { required: true, type: 'number', message: '执行人不能为空', trigger: 'change' },
        productType: { required: true, message: '产品类型不能为空', trigger: 'blur' },
        productModel: { required: true, message: '产品型号不能为空', trigger: 'blur' },
        handleDetail: { required: true, message: '处理不能为空', trigger: 'blur' },
        handleOpinion: { required: true, message: '处理意见不能为空', trigger: 'blur' }
      },
      allProductType: [],
      allProductModel: {},
      allUser: [],
      auditGroupList: [],
      groupIdToUserName: {},
      groupIdToUserIds: {}
    }
  },
  watch: {
    value (val) {
      this.visible = val
    }
  },
  computed: {
    modalTitle () {
      return this.isUpdate ? '编辑产品' : '添加产品'
    },
    functionTypeListRow () {
      let rowList = []
      this.functionTypeList.map((item, index) => {
        item.title = item.typeName + (item.desc ? `(${item.desc})` : '')
        if (index % 2 == 0) {
          rowList.push([item])
        } else {
          rowList[rowList.length - 1].push(item)
        }
      })
      return rowList
    },
    access () {
      return this.$store.state.user.access
    },
    // 是否有当前产品类型的权限
    accessProductType () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth[this.$route.meta.productType]], this.access)
    },
    // 判断是否有添加产品的权限，
    accessAdd () {
      return hasOneOf(['super_admin', 'admin', 'product_add'], this.access)
    },
    // 判断是否有更新产品的权限，
    accessUpdate () {
      return hasOneOf(['super_admin', 'admin', 'product_update'], this.access)
    }
  },
  methods: {
    saveTaskData () {
      this.$refs.taskManage.validate((valid) => {
        if (valid) {
          // 获取登录用户的token，根据token获取当前用户是否有权限
          const token = getToken()
          store.commit('setToken', token)
          if (!token) {
            this.$store.state.user.access = []
          }
          store.dispatch('getUserInfo').then(user => {
            // 拉取用户信息，获取用户权限access， 存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
            this.$store.state.user.access = user.access
            if (this.accessAddTask) {
              this.loading = true
              let userId = this.$store.state.user.userId
              this.taskData.createUserId = userId
              this.taskData.auditGroupUserIds = this.groupIdToUserIds[this.taskData.auditGroupId]
              try {
                saveTask(this.taskData).then(res => {
                  this.loading = false
                  if (res.data.errorCode !== '0') {
                    this.$Message.error('保存失败:' + res.data.msg)
                  } else {
                    this.$Message.success('保存成功！')
                    this.getUnhandledTaskList(userId)
                    this.modal1 = false
                    this.clearTaskData()
                  }
                })
              } catch (e) {
                this.loading = false
                this.$Message.error('保存失败:' + e)
              }
            } else {
              this.$Message.warning('当前用户没有发起任务的权限')
            }
          })
        }
      })
    },
    // 保存产品，先判断当前用户是否有该类型的权限
    saveProduct () {
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，通过用户权限和跳转的页面的name来判断是否有权限访问;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 根据是否有id，判断是更新还是新增
        let booleanForAdd = true
        let booleanForUpdate = true
        if (this.productData.id) {
          booleanForAdd = false
          booleanForUpdate = true
        } else {
          booleanForAdd = true
          booleanForUpdate = false
        }
        // 如果有对应产品的权限
        if (this.accessProductType) {
          if ((this.accessUpdate && booleanForUpdate) || (this.accessAdd && booleanForAdd)) {
            // 拼接功能id列表
            this.productData.functionIds = this.functionIdList.reduce((prev, cur) => prev.concat(cur))
            saveProduct(this.productData).then(result => {
              if (result.data.errorCode && result.data.errorCode === '0') {
                this.$Message.success('产品保存成功！')
                this.productData = {
                  productType: this.productType,
                  id: '',
                  productCategory: '',
                  branch: '',
                  code: '',
                  model: '',
                  sN8: '',
                  lifecycleStage: '',
                  saleChannel: '',
                  functionIds: [],
                  scenarioIds: [],
                  voiceFunctionIds: [],
                  ecologyEntranceIds: [],
                  sensorIds: [],
                  pic: ''
                }
                // 重新加载列表
                this.searchData()
                this.visible = false
                this.$emit('input', false)
              } else {
                this.$Message.error('产品保存失败:' + result.data.msg)
              }
            })
          } else {
            if (booleanForAdd) {
              this.$Message.error('当前用户没有添加产品权限！')
            } else {
              this.$Message.error('当前用户没有更新产品权限！')
            }
          }
        } else {
          this.$Message.error('当前用户没有此类产品的权限！')
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('保存失败！')
      })
    },
    // 关闭产品编辑页面弹窗时，将该弹窗的数据清除
    cancelSaveProduct () {
      this.productData = {
        productType: this.productType,
        id: '',
        categoryType: '',
        branch: '',
        code: '',
        model: '',
        sN8: '',
        lifecycleStage: '',
        saleChannel: '',
        functionIds: [],
        scenarioIds: [],
        voiceFunctionIds: [],
        ecologyEntranceIds: [],
        sensorIds: [],
        pic: ''
      }
      this.visible = false
      this.$emit('input', false)
    },
    // 关闭产品编辑页面弹窗时，将该弹窗的数据清除
    closeModal () {
      this.$emit('input', false)
      this.productData = {
        productType: this.productType,
        id: '',
        categoryType: '',
        branch: '',
        code: '',
        model: '',
        sN8: '',
        lifecycleStage: '',
        saleChannel: '',
        functionIds: [],
        scenarioIds: [],
        voiceFunctionIds: [],
        ecologyEntranceIds: [],
        sensorIds: [],
        pic: ''
      }
    },
    getFunctionListByType (typeKey) {
      return this.functionList.filter(item => item.typeKey == typeKey)
    },
    changeProductType () {
      this.taskData.productFunctionType = []
      this.taskData.productScenarioType = []
      this.taskData.productSensorType = []
      this.taskData.productModel = ''
      this.initProductTypeData()
    },
    changeProductModel () {
      queryProduct({ 'model': [this.taskData.productModel] }).then(res => {
        if (res.data.result) {
          this.productData = res.data.result[0]
        } else {
          this.productData = {
            productType: this.productType,
            id: '',
            categoryType: '',
            branch: '',
            code: '',
            model: '',
            sN8: '',
            lifecycleStage: '',
            saleChannel: '',
            functionIds: [],
            scenarioIds: [],
            voiceFunctionIds: [],
            ecologyEntranceIds: [],
            sensorIds: [],
            pic: ''
          }
        }
      })
    },
    initProductTypeData () {
      // 获取当前类型的名称
      getProductTypeByTypeCode(this.productType).then(res => {
        if (res.data.result && res.data.result.value) {
          this.productTypeName = res.data.result.value
        }
      })
      // 获取场景
      getScenario(this.productType).then(res => {
        if (res.data.result) {
          let scenarios = res.data.result
          this.scenarioList = scenarios
          this.setColumns(scenarios)

          let scenarioNameToScenarioId = {}
          scenarios.forEach((scen) => {
            scenarioNameToScenarioId[scen.scenarioName] = scen.id
          })
          this.productTypeToScenNameAndId[this.productType] = scenarioNameToScenarioId
        }
      })
      // 获取品类
      getProductCategoryByProductType(this.productType).then(result => {
        if (result.data.result) {
          this.categoryList = result.data.result
          this.categoryList.forEach((cate) => {
            this.categoryNameToProductType[cate.value] = this.productType
            this.categoryNameToCategoryType[cate.value] = cate.code
          })
        }
      })
      // 获取功能
      getFunctionByType(this.productType).then(res => {
        // console.log(res.data)
        if (res.data.result) {
          this.functionList = res.data.result
          this.productTypeToFunctionList[this.productType] = this.functionList
          let functionNameToFunctionId = {}
          this.functionList.forEach((func) => {
            functionNameToFunctionId[func.functionName] = func.id
          })
          this.productTypeToFuncNameAndId[this.productType] = functionNameToFunctionId
        }
      })
      // 获取功能类型
      getFunctionType(this.productType).then(res => {
        // console.log(res.data)
        if (res.data.result) {
          this.functionTypeList = res.data.result
          this.functionIdList = new Array(this.functionTypeList.length).fill([])
        }
      })
      // 获取传感器
      getSensorByType(this.productType).then(res => {
        if (res.data.errorCode === '0') {
          this.allSensorList = res.data.result
          if (this.allSensorList) {
            this.allSensorList.forEach(value => {
              this.sensorNameToId[value.sensorName] = value.id
            })
          }
        }
      })
    }
  },
  created () {
    this.taskData = this.propTaskData
  },
  mounted () {
    this.productType = this.$route.meta.productType
    let userId = this.$store.state.user.userId
    queryAuditGroupByUserId(userId).then(res => {
      if (res.data.result) {
        this.auditGroupList = res.data.result
        this.auditGroupList.forEach(value => {
          this.groupIdToUserName[value.id] = value.userNames
          this.groupIdToUserIds[value.id] = value.userIds.toString()
        })
      }
    })
    getAllUserIdAndName().then(res => {
      if (res.data.errorCode === '0' && res.data.result) {
        res.data.result.forEach((item) => {
          if (item.userName !== 'admin' && item.userName !== 'super_admin') {
            this.allUser.push(item)
          }
        })
      } else {
        this.allUser = []
      }
    })
  },
  beforeMount () {
    // 获取所有产品类型
    getProductType().then(res => {
      if (res.data.errorCode === '0' && res.data.result) {
        this.allProductType = res.data.result
      }
    })
    // 类型根据传过来的数据赋值
    this.productType = this.$route.meta.productType
    this.initProductTypeData()
    // 获取品牌
    getBranchList().then(result => {
      if (result.data.result) {
        this.branchList = result.data.result
        this.branchList.forEach((item) => {
          this.branchNameToBranchCode[item.value] = item.code
        })
      }
    })
    // 获取语音功能
    getVoiceFunction().then(res => {
      if (res.data.errorCode === '0') {
        this.allVoiceFunctionList = res.data.result
        if (this.allVoiceFunctionList) {
          this.allVoiceFunctionList.forEach(value => {
            this.voiceFunctionNameToId[value.name] = value.id
          })
        }
      }
    })
    // 获取生态入口
    getEcologyEntrance().then(res => {
      if (res.data.errorCode === '0') {
        this.allEcologyEntranceList = res.data.result
        if (this.allEcologyEntranceList) {
          this.allEcologyEntranceList.forEach(value => {
            this.ecologyEntranceNameToId[value.name] = value.id
          })
        }
      }
    })
    // 获取所有的产品型号
    getProductModel().then(res => {
      if (res.data.result) {
        this.allProductModel = {}
        res.data.result.forEach((item) => {
          if (this.allProductModel[item.productType]) {
            this.allProductModel[item.productType].push(item)
          } else {
            this.allProductModel[item.productType] = []
            this.allProductModel[item.productType].push(item)
          }
        })
        console.log(this.allProductModel)
      }
      // getModelFinish = true
      // if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
      //   this.spinShow = false
      // }
    })
  }
}
</script>

<style scoped>

</style>
