<template>
  <Modal
    :styles="{width: '820px'}"
    v-model="visible"
    title="添加产品"
    @on-cancel="closeModal"
    mask
    :mask-closable=false
    :loading="loading">
    <!-- <Steps :current="currentStep">
        <Step title="产品基本信息"></Step>
        <Step title="电控信息"></Step>
        <Step title="APP功能"></Step>
        <Step title="其他功能"></Step>
    </Steps> -->
    <Form :model="productData" label-position="left" :label-width="88">
      <Tabs v-model="currentStep">
          <Tab-pane label="产品基本信息">
            <Row :gutter="16">
              <Col span="12">
                <FormItem label="产品编码">
                  <Input :disabled="isUpdate" v-model="productData.code" :maxlength="50" placeholder="请输入产品编码" clearable></Input>
                </FormItem>
              </Col>
              <Col span="12">
                <FormItem label="产品型号">
                  <Input :disabled="isUpdate" v-model="productData.model" :maxlength="50" placeholder="请输入产品型号" clearable></Input>
                </FormItem>
              </Col>
            </Row>
            <Row :gutter="16">
              <Col span="12">
                <FormItem label="SN8">
                  <Input :disabled="isUpdate" v-model="productData.sn8" :maxlength="50" placeholder="请输入产品SN8，8个字符" clearable></Input>
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
            </Row>
          </Tab-pane>
          <Tab-pane label="电控信息">
            <Row :gutter="16">
              <Col span="12" v-for="(electricBoardInfo,index) in allElectricBoardInfoList" :key="index">
                <FormItem :label="electricBoardInfo.typeName">
                  <!-- 选择 -->
                  <Select
                    v-if="electricBoardInfo.componentType=='Select'"
                    v-model="productData.electricBoardInfo[electricBoardInfo.typeKey]"
                    :placeholder="electricBoardInfo.desc"
                    transfer
                    clearable
                    @on-change="wifiModuleCodeSelected"
                  >
                    <Option
                      v-for="item in allSelectOptionList.filter(op=>op.key == electricBoardInfo.typeKey)"
                      :value="item.value"
                      :key="item.id"
                    >
                      {{ item.label }}
                      <span style="float:right;color:#ccc"> {{item.desc}}</span>
                    </Option>
                  </Select>
                  <!-- 文本输入框 -->
                  <Input v-else v-model="productData.electricBoardInfo[electricBoardInfo.typeKey]" :placeholder="electricBoardInfo.desc"></Input>
                </FormItem>
              </Col>
            </Row>
          </Tab-pane>
          <Tab-pane label="APP功能">
            <Row :gutter="16">
              <!-- todo: 扩展，可复制功能 -->
              <Col span="12">
                <Button type="primary" @click="showCopyModal=true">从现有产品复制功能</Button>
              </Col>
            </Row>
            <Row :gutter="16">
              <Col :span="functionType.componentType=='Select'?12:24" v-for="(functionType,index) in functionTypeList" :key="index">
                <FormItem style="margin-bottom: 12px">
                  <div slot="label">
                    <span>{{functionType.typeName}}</span>
                    <!-- <Poptip placement="right" width="400">
                      <Icon type="ios-help-circle" size="16" color="#888888" @click="showHelp(index)"/>
                        <div slot="content">
                          <img :src="qqFans" alt="" height="400px">
                        </div>
                    </Poptip> -->
                  </div>
                  <!-- 多选 -->
                  <CheckboxGroup v-if="functionType.componentType=='Checkbox'" v-model="functionIdList[index]" clearable>
                    <Checkbox
                      v-for="item in functionList.filter(item => item.functionKey == functionType.typeKey && !item.isDisable)"
                      :key="item.id"
                      :label="item.id"
                    >
                      <span>{{item.functionName}}</span>
                      <span v-if="item.functionDesc" style="color: #999999; font-size: 0.6em;">({{item.functionDesc}})</span>
                    </Checkbox>
                  </CheckboxGroup>
                  <!-- 单选 -->
                  <RadioGroup v-else-if="functionType.componentType=='Radio'" v-model="functionIdList[index]" clearable>
                    <Radio
                      v-for="item in functionList.filter(item => item.functionKey == functionType.typeKey && !item.isDisable)"
                      :key="item.id"
                      :label="item.id"
                    >
                      <!-- 单选的functionName都一样，显示desc就行 -->
                      <span>{{item.functionDesc}}</span>
                    </Radio>
                  </RadioGroup>
                  <!-- 选择器 -->
                  <Select
                    v-else-if="functionType.componentType=='Select'"
                    v-model="functionIdList[index]"
                    :placeholder="functionType.desc"
                    transfer
                    clearable
                  >
                    <Option
                      v-for="item in functionList.filter(item => item.functionKey == functionType.typeKey && !item.isDisable)"
                      :value="item.id"
                      :key="item.id"
                    >
                      {{ item.functionDesc }}
                    </Option>
                  </Select>
                  <!-- 文本输入框 -->
                  <Input v-else v-model="functionIdList[index]" clearable></Input>
                </FormItem>
              </Col>
            </Row>
          </Tab-pane>
          <!-- <Tab-pane label="其他功能">
          </Tab-pane> -->
      </Tabs>
    </Form>
    <div slot="footer">
      <Button style="margin-right: 8px" @click="cancelSaveProduct">取消</Button>
      <Button v-if="currentStep != 0" style="margin-right: 8px" @click="currentStep-=1">上一步</Button>
      <Button v-if="currentStep == 2" type="primary" @click="saveProduct">保存</Button>
      <Button v-else type="primary" @click="currentStep+=1">下一步</Button>
    </div>
    <Modal
      :styles="{width: '320px'}"
      v-model="showCopyModal"
      title="复制产品功能"
      @on-cancel="showCopyModal=false"
      @on-ok="copyFunctionFromProduct"
      mask
      :mask-closable=false>
      <Select v-model="appCopySn8" placeholder="选择产品" filterable transfer>
        <Option v-for="item in allProductModel[productType]" :value="item.sn8" :label="item.model" :key="item.sn8" >
          <span>{{ item.model }} ({{ item.sn8 }})</span>
          <span style="float:right;color:#ccc;margin-right:16px">{{ item.appStatus }}</span>
        </Option>
      </Select>
    </Modal>
  </Modal>
</template>

<script>
import {
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
  queryAuditGroupByUserId,
  getElectricBoardInfo,
  getSelectOption,
} from '@/api/data'
import { hasOneOf } from '@/libs/tools'
import store from '@/store'
import { getToken, setToken } from '@/libs/util'
import config from '@/config'
import qqFans from '@/assets/images/qq-group1.jpg'

const initProductData = {
  productType: '',
  id: '',
  categoryType: '',
  branch: '',
  code: '',
  model: '',
  sn8: '',
  lifecycleStage: '',
  saleChannel: '',
  functionIds: [],
  scenarioIds: [],
  voiceFunctionIds: [],
  ecologyEntranceIds: [],
  sensorIds: [],
  electricBoardInfo: {},
  appStatus: '草稿',
  pic: ''
}
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
    productType: {
      type: String,
      default: ''
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
      productData: JSON.parse(JSON.stringify(initProductData)), // 深拷贝，防止子项引用改到默认数据
      categoryList: [],
      branchList: [],
      functionList: [],
      scenarioList: [],
      allSensorList: [],
      allElectricBoardInfoList: [],
      allSelectOptionList: [],
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
      allProductType: [],
      allProductModel: {},
      qqFans: qqFans,
      showCopyModal: false,
      appCopySn8: '',
    }
  },
  watch: {
    value (nV, oV) {
      this.visible = nV
      if (nV && !oV) {
        // 类型根据传过来的数据赋值
        this.initProductTypeData()
      }
    },
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
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth[this.productType]], this.access)
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
            this.productData.functionIds = this.functionIdList.reduce((prev, cur) => {
              if (typeof cur === 'string') {
                cur = cur ? [cur] : []
              }
              return prev.concat(cur)
            })
            saveProduct(this.productData).then(result => {
              if (result.data.errorCode && result.data.errorCode === '0') {
                this.$Message.success('产品保存成功！')
                this.productData = JSON.parse(JSON.stringify(initProductData))
                this.visible = false
                this.$emit('input', false)
                // 重新加载列表
                this.$emit('saveProductSuccess', false)
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
      this.productData = JSON.parse(JSON.stringify(initProductData))
      this.visible = false
      this.$emit('input', false)
    },
    // 关闭产品编辑页面弹窗时，将该弹窗的数据清除
    closeModal () {
      this.$emit('input', false)
      this.productData = JSON.parse(JSON.stringify(initProductData))
    },
    getFunctionListByType (typeKey) {
      return this.functionList.filter(item => item.functionKey == typeKey && !item.isDisable)
    },
    initProductTypeData () {
      initProductData.productType = this.productType
      this.productData.productType = this.productType
      // 获取场景
      // getScenario(this.productType).then(res => {
      //   if (res.data.result) {
      //     let scenarios = res.data.result
      //     this.scenarioList = scenarios
      //     this.setColumns(scenarios)

      //     let scenarioNameToScenarioId = {}
      //     scenarios.forEach((scen) => {
      //       scenarioNameToScenarioId[scen.scenarioName] = scen.id
      //     })
      //     this.productTypeToScenNameAndId[this.productType] = scenarioNameToScenarioId
      //   }
      // })
      // 获取品类
      // getProductCategoryByProductType(this.productType).then(result => {
      //   if (result.data.result) {
      //     this.categoryList = result.data.result
      //     this.categoryList.forEach((cate) => {
      //       this.categoryNameToProductType[cate.value] = this.productType
      //       this.categoryNameToCategoryType[cate.value] = cate.code
      //     })
      //   }
      // })
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
          this.functionIdList = this.functionTypeList.map(item => {
            return item.isMultiple ? [] : ''
          })
        }
      })
      // 获取传感器
      // getSensorByType(this.productType).then(res => {
      //   if (res.data.errorCode === '0') {
      //     this.allSensorList = res.data.result
      //     if (this.allSensorList) {
      //       this.allSensorList.forEach(value => {
      //         this.sensorNameToId[value.sensorName] = value.id
      //       })
      //     }
      //   }
      // })
      // 获取电控信息
      getElectricBoardInfo(this.productType).then(res => {
        if (res.data.errorCode === '0') {
          this.allElectricBoardInfoList = res.data.result
          if (this.allElectricBoardInfoList) {
            // this.allElectricBoardInfoList.forEach(value => {
            //   this.sensorNameToId[value.sensorName] = value.id
            // })
          }
        }
      })
      // 获取电控信息
      getSelectOption(this.productType).then(res => {
        if (res.data.errorCode === '0') {
          this.allSelectOptionList = res.data.result
          if (this.allSelectOptionList) {
            // this.allSelectOptionList.forEach(value => {
            //   this.sensorNameToId[value.sensorName] = value.id
            // })
          }
        }
      })
    },
    copyFunctionFromProduct () {
      if (!this.appCopySn8) return
      let copyItem = this.allProductModel[this.productType].find(item => item.sn8 === this.appCopySn8)
      console.log(this.appCopySn8)
      this.productData.functionIds = copyItem.functionIds
      console.log(this.productData.functionIds)
    },
    wifiModuleCodeSelected () {
      // let selectedItem = this.allWifiModuleTypeList.find(item => item.code === this.productData.wifiModuleCode)
      // this.productData.networkingMode = selectedItem.networkingMode
    },
  },
  created () {
  },
  mounted () {
  },
  beforeMount () {
    // 获取所有产品类型
    getProductType().then(res => {
      if (res.data.errorCode === '0' && res.data.result) {
        this.allProductType = res.data.result
      }
    })
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
