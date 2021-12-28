<template>
  <div>
    <Button v-if="accessAdd" @click="showAddDrawer" type="primary">添加</Button>
    <Dropdown v-if="accessImport">
      <Button style="width:140px">
        批量导入
        <Icon type="ios-arrow-down"></Icon>
      </Button>
      <DropdownMenu slot="list">
        <DropdownItem>
          <Upload action="" :before-upload="handleBeforeUpload" accept=".xls, .xlsx">
            <Button icon="ios-cloud-upload-outline" :loading="uploadLoading" @click="handleUploadFile">批量导入</Button>
          </Upload>
        </DropdownItem>
        <DropdownItem>
          <Button style="alignment: right" @click="downloadImportTemplate" type="primary">下载导入模板</Button>
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
    <Drawer
      :title="drawerTitle"
      v-model="drawer"
      width="720"
      :mask-closable="false"
      :styles="styles"
      @on-close="closeDrawer">
      <Form :model="productData">
        <Row :gutter="32">
          <Col span="12">
            <FormItem label="产品编码" label-position="top">
              <div v-if="isUpdate">
                <Input disabled v-model="productData.code" :maxlength="50" placeholder="请输入产品编号，50个字符以内"
                       clearable></Input>
              </div>
              <div v-else>
                <Input v-model="productData.code" :maxlength="50" placeholder="请输入产品编号，50个字符以内" clearable></Input>
              </div>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="产品型号" label-position="top">
              <div v-if="isUpdate">
                <Input disabled v-model="productData.model" :maxlength="50" placeholder="请输入产品型号，50个字符以内"
                       clearable></Input>
              </div>
              <div v-else>
                <Input v-model="productData.model" :maxlength="50" placeholder="请输入产品型号，50个字符以内" clearable></Input>
              </div>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="12">
            <FormItem label="SN8" label-position="top">
              <div v-if="isUpdate">
                <Input disabled v-model="productData.sN8" :maxlength="50" placeholder="请输入产品SN8，50个字符以内"
                       clearable></Input>
              </div>
              <div v-else>
                <Input v-model="productData.sN8" :maxlength="50" placeholder="请输入产品SN8，50个字符以内" clearable></Input>
              </div>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="版本" label-position="top">
              <div v-if="isUpdate">
                <Input disabled v-model="productData.productVersion" :maxlength="50" placeholder="" clearable/>
              </div>
              <div v-else>
                <Input v-model="productData.productVersion" :maxlength="50" placeholder="请输入产品版本，50个字符以内" clearable/>
              </div>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="12">
            <FormItem label="品牌" label-position="top">
              <Select v-model="productData.branch" placeholder="请选择品牌">
                <Option v-for="item in branchList" :value="item.code" :key="item.code">{{ item.value }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="产品功能" label-position="top">
              <Select v-model="productData.functionIds" placeholder="请选择产品功能" multiple>
                <Option v-for="item in functionList" :value="item.id" :key="item.id">{{ item.functionName }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="12">
            <FormItem label="产品场景" label-position="top">
              <Select v-model="productData.scenarioIds" placeholder="请选择产品场景" multiple>
                <Option v-for="item in scenarioList" :value="item.id" :key="item.id">{{ item.scenarioName }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="语音功能" label-position="top">
              <Select v-model="productData.voiceFunctionIds" placeholder="请选择产品语音功能" multiple>
                <Option v-for="item in allVoiceFunctionList" :value="item.id" :key="item.id">{{ item.name }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="12">
            <FormItem label="生态入口" label-position="top">
              <Select v-model="productData.ecologyEntranceIds" placeholder="请选择产品生态入口" multiple>
                <Option v-for="item in allEcologyEntranceList" :value="item.id" :key="item.id">{{ item.name }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="传感器" label-position="top">
              <Select v-model="productData.sensorIds" placeholder="请选择产品传感器" multiple>
                <Option v-for="item in allSensorList" :value="item.id" :key="item.id">{{ item.sensorName }}</Option>
              </Select>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="12">
            <FormItem label="插件UI" label-position="top">
              <!-- eslint-disable-next-line-->
              <div class="demo-upload-list" v-for="item in uploadList">
                <template v-if="item.status === 'finished'">
                  <img :src="item.url">
                  <div class="demo-upload-list-cover">
                    <Icon type="ios-eye-outline" @click.native="handleView(item.name)"></Icon>
                    <Icon type="ios-trash-outline" @click.native="handleRemove(item)"></Icon>
                  </div>
                </template>
                <template v-else>
                  <Progress v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>
                </template>
              </div>
              <Upload
                ref="upload"
                :show-upload-list="false"
                :default-file-list="uploadList"
                :on-success="handleSuccess"
                :format="['jpg','jpeg','png']"
                accept=".jpg, .jpeg, .png"
                :max-size="10240"
                :on-format-error="handleFormatError"
                :on-exceeded-size="handleMaxSize"
                :before-upload="handleBeforeUploadPic"
                type="drag"
                :action="uploadMethod"
                style="display: inline-block;width:58px;">
                <div style="width: 58px;height:58px;line-height: 58px;">
                  <Icon type="ios-camera" size="20"></Icon>
                </div>
              </Upload>
              <Modal :styles="viewPicStyles" title="查看大图" v-model="visible">
                <img :src=" viewPicContext + imgName " v-if="visible" style="width: 100%;">
              </Modal>
            </FormItem>
          </Col>
        </Row>
      </Form>
      <div class="demo-drawer-footer">
        <Button style="margin-right: 8px" @click="cancelSaveProduct">取消</Button>
        <Button type="primary" @click="saveProduct">保存</Button>
      </div>
    </Drawer>
    <span>
      <Card>
        <Form :model="productDataForSearch" label-position="right" :label-width="65">
        <Row :gutter="0">
          <Col span="5">
            <FormItem label="产品编码:" :label-width="80">
              <Input v-model="productDataForSearch.productCode" :maxlength="50" placeholder="请输入产品编号，50个字符以内"
                     clearable></Input>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="产品型号:" :label-width="80">
              <Input v-model="productDataForSearch.productModel" :maxlength="50" placeholder="请输入产品型号，50个字符以内"
                     clearable></Input>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="SN8:" :label-width="80">
              <Input v-model="productDataForSearch.productSN8" :maxlength="50" placeholder="请输入产品SN8，50个字符以内"
                     clearable></Input>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="产品功能:" :label-width="80">
              <Select v-model="productDataForSearch.function" placeholder="请选择产品功能" clearable>
                <Option v-for="item in functionList" :value="item.id"
                        :key="item.id">{{ item.functionName }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="4">
            <FormItem label="产品场景:" :label-width="80">
              <Select v-model="productDataForSearch.scenario" placeholder="请选择产品场景" clearable>
                <Option v-for="item in scenarioList" :value="item.id"
                        :key="item.id">{{ item.scenarioName }}</Option>
              </Select>
            </FormItem>
          </Col>

        </Row>
        <Row :gutter="0">
          <Col span="5">
            <FormItem label="品牌:">
              <Select v-model="productDataForSearch.branch" placeholder="请选择品牌" clearable>
                <Option v-for="item in branchList" :value="item.code" :key="item.code">{{ item.value }}</Option>
              </Select>
            </FormItem>
          </Col>

          <Col span="5">
            <FormItem label="语音功能:" :label-width="80">
              <Select v-model="productDataForSearch.voiceFunction" placeholder="请选择产品语音功能" clearable>
                <Option v-for="item in allVoiceFunctionList" :value="item.id"
                        :key="item.id">{{ item.name }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="生态入口:" :label-width="80">
              <Select v-model="productDataForSearch.ecologyEntrance" placeholder="请选择产品生态入口" clearable>
                <Option v-for="item in allEcologyEntranceList" :value="item.id"
                        :key="item.id">{{ item.name }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="传感器:" :label-width="80">
              <Select v-model="productDataForSearch.sensor" placeholder="请选择产品传感器" clearable>
                <Option v-for="item in allSensorList" :value="item.id"
                        :key="item.id">{{ item.sensorName }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="4" style="text-align: right">
             <Button icon="ios-search" style="margin: 10px 0;" :loading="searchLoading" type="primary"
                     @click="searchData">搜索</Button>
          </Col>
        </Row>
       </Form>
      </Card>
    </span>
    <Card>
      <Spin size="large" fix v-if="loadingProduct"/>
      <div>
        <span>共查询到 {{ tableDataCount }} 条数据</span>
        <tables ref="product_tables" editable border stripe v-model="tableData" :columns="columns"
                @on-select="selectProduct"
                @on-select-cancel="selectProductCancel"
                @on-select-all="selectAllProduct"
                @on-select-all-cancel="selectAllProductCancel"
                @on-selection-change="selectChange"
        />
        <div style="float: right ;margin-top:15px">
          <Page :total="tableDataCount" show-sizer transfer :page-size="pageSize"
                :current="pageNumber" show-total :page-size-opts="[10, 20, 30, 40,60,70,80,90,100]"
                @on-change="getProductByPageNumberAndPageSize"
                @on-page-size-change="changePageSize"
          />
        </div>
      </div>
      <Button v-if="accessExport" style="margin: 10px 0;" :loading="exportLoading" type="primary" @click="exportExcel">
        导出为Excel文件
      </Button>
    </Card>
  </div>
</template>

<script>
import Tables from '_c/tables'
import {
  deleteProductById,
  queryProduct,
  getScenario,
  getProductCategoryByProductType,
  getProductTypeByTypeCode,
  getBranchList,
  getFunctionByType,
  saveProduct,
  getVoiceFunction,
  getSensorByType,
  getEcologyEntrance
} from '@/api/data'
import { hasOneOf } from '@/libs/tools'
import store from '@/store'
import { getToken, setToken } from '@/libs/util'
import excel from '@/libs/excel'
import config from '@/config'

export default {
  name: 'tables_product',
  components: {
    Tables
  },
  data () {
    return {
      loadingProduct: false,
      pageSize: 10,
      pageNumber: 1,
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
      drawer: false,
      productData: {
        productType: this.productType,
        productTypeName: '',
        id: '',
        categoryType: '',
        branch: '',
        code: '',
        model: '',
        sN8: '',
        productVersion: '',
        lifecycleStage: '',
        saleChannel: '',
        functionIds: [],
        scenarioIds: [],
        voiceFunctionIds: [],
        ecologyEntranceIds: [],
        sensorIds: [],
        pic: ''
      },
      isUpdate: false,
      productDataForSearch: {
        productType: [],
        id: '',
        productCategory: '',
        branch: '',
        productCode: '',
        productModel: '',
        productSN8: '',
        lifecycleStage: '',
        saleChannel: '',
        function: '',
        scenario: '',
        voiceFunction: '',
        ecologyEntrance: '',
        sensor: '',
        pageSize: 10,
        pageNumber: 1
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
      visible: false,
      columns: [],
      tableData: []
    }
  },
  methods: {
    handleView (name) {
      this.imgName = name
      this.visible = true
    },
    handleRemove (file) {
      // this.uploadOrNot = true
      const fileList = this.$refs.upload.fileList
      this.$refs.upload.fileList.splice(fileList.indexOf(file), 1)
      this.uploadList = []
      this.productData.pic = ''
    },
    handleSuccess (res, file) {
      file.url = config.baseUrl.pro + 'upload/' + res.result
      file.name = res.result
      this.productData.pic = file.name
      this.uploadList = [{
        name: file.name,
        url: this.viewPicContext + file.name,
        status: 'finished'
      }]
    },
    handleFormatError (file) {
      this.$Notice.warning({
        title: '文件格式不对',
        desc: file.name + '文件格式不对，请选择 jpg jpeg png 格式的文件。'
      })
    },
    handleMaxSize (file) {
      this.$Notice.warning({
        title: '超过最大限制',
        desc: '文件  ' + file.name + ' 最大不可超过 10M.'
      })
    },
    handleBeforeUploadPic () {
      const check = this.uploadList.length < 1
      if (!check) {
        this.$Notice.warning({
          title: '最多只能上传一个图片.'
        })
      }
      return check
    },
    getProductByPageNumberAndPageSize (current) {
      this.pageNumber = current
      this.searchData()
    },
    changePageSize (pageSize) {
      this.pageSize = pageSize
      if (this.pageNumber === 1) {
        this.searchData()
      }
    },
    selectProduct () {

    },
    selectProductCancel () {

    },
    selectAllProduct () {

    },
    selectAllProductCancel () {

    },
    selectChange (selection) {
      this.selectDatas = selection
    },
    // 导出Excel
    exportExcel () {
      // 导出产品时，确认当前登录用户时候有权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      // 根据token获取当前登录用户
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，通过用户权限和跳转的页面的name来判断是否有权限访问;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 判断是否有该类型产品的权限
        if (this.accessProductType) {
          if (this.accessExport) {
            if (this.selectDatas.length > 0) {
              this.exportLoading = true
              const params = {
                title: ['品类', '品牌', '产品编号', '产品型号', 'SN8', '版本', '功能', '场景', '语音功能', '生态入口', '传感器'],
                key: ['productTypeName', 'branchName', 'code', 'model', 'sN8', 'productVersion', 'functionsName', 'scenariosNameSupported', 'voiceFunctionName', 'ecologyEntranceName', 'sensorName'],
                comments: this.selectDatas,
                data: this.selectDatas,
                autoWidth: true,
                filename: `产品信息-${this.formatDate(new Date())}`
              }
              excel.export_array_to_excel(params)
              this.exportLoading = false
            } else {
              this.$Message.info('请选择要导出的数据！')
            }
          } else {
            this.$Message.error('当前用户没有导出产品信息的权限！')
          }
        } else {
          this.$Message.error('当前用户没有此类产品的权限！')
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('导出失败！')
      })
    },
    // 上传文件预处理，读取文件内容，只接受 xlsx 和 xls 格式文件
    handleBeforeUpload (file) {
      // 导入产品时，确认当前登录用户时候有权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      // 根据token获取当前登录用户
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，通过用户权限和跳转的页面的name来判断是否有权限访问;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 判断是否有该类型产品的权限
        if (this.accessProductType) {
          if (this.accessImport) {
            const fileExt = file.name.split('.').pop().toLocaleLowerCase()
            if (fileExt === 'xlsx' || fileExt === 'xls') {
              this.readFile(file)
              this.file = file
            } else {
              this.$Notice.warning({
                title: '文件类型错误',
                desc: '文件：' + file.name + '不是EXCEL文件，请选择后缀为.xlsx或者.xls的EXCEL文件。'
              })
            }
          } else {
            this.$Message.error('当前用户没有导入产品的权限！')
          }
        } else {
          this.$Message.error('当前用户没有此类产品的权限！')
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('导入失败！')
      })
      return false
    },
    //  初始化上传参数
    initUpload () {
      this.file = null
      this.showProgress = false
    },
    handleUploadFile () {
      this.initUpload()
    },
    // 读取文件
    readFile (file) {
      const reader = new FileReader()
      reader.readAsArrayBuffer(file)
      reader.onloadstart = e => {
        this.uploadLoading = true
        this.tableLoading = true
        this.showProgress = true
      }
      reader.onprogress = e => {
        this.progressPercent = Math.round(e.loaded / e.total * 100)
      }
      reader.onerror = e => {
        this.$Message.error('文件读取出错')
      }
      reader.onload = e => {
        this.$Message.success('文件读取成功')
        const data = e.target.result
        // 解析上传excel文件，header是字段，result是数据
        const { header, results } = excel.read(data, 'array')
        if (!this.titleIsRight(header)) {
          this.$Message.error('批量导入文件内容不对，请按模板填写！')
          return
        }
        // 将上次上传数据清空
        this.importTotal = 0
        this.invalidData = []
        this.uploadDataCount = results.length
        // 数据是空的情况
        if (results.length === 0) {
          this.uploadLoading = false
          this.tableLoading = false
          this.$Message.info('导入数据为空')
        } else {
          results.forEach((data, index, array) => {
            // 将每一行数据转化为产品信息
            const transFileToData = this.transFileDataToProduct(data)
            // 验证没有通过
            if (!transFileToData || !transFileToData.validate) {
              data['错误信息'] = transFileToData.errorMsg
              this.invalidData.push(data)
              this.uploadDataCount = this.uploadDataCount - 1
              // 所有解析完毕，下载错误数据和展示导入结果
              if (this.uploadDataCount <= 0) {
                this.$Message.info('导入成功 ' + this.importTotal + ' 条数据，导入失败 ' + this.invalidData.length + ' 条数据！')

                // 导出错误的数据
                if (this.invalidData.length > 0) {
                  header.push('错误信息')
                  this.exportLoading = true
                  const params = {
                    title: header,
                    key: header,
                    data: this.invalidData,
                    autoWidth: true,
                    filename: `导入错误信息-${this.formatDate(new Date())}`
                  }
                  excel.export_array_to_excel(params)
                  this.exportLoading = false
                } else {

                }
                this.uploadLoading = false
                this.tableLoading = false
                // 重新加载数据
                this.searchData()
              }
            } else {
              // 导入成功保存数据
              saveProduct(transFileToData.result).then(res => {
                if (res.data.errorCode && res.data.errorCode === '0') {
                  this.importTotal = this.importTotal + 1
                } else {
                  data['错误信息'] = res.data.msg
                  this.invalidData.push(data)
                }
                this.uploadDataCount = this.uploadDataCount - 1
                // 所有数据处理完毕，展示导入结果和导出错误数据
                if (this.uploadDataCount <= 0) {
                  this.$Message.info('导入成功 ' + this.importTotal + ' 条数据，导入失败 ' + this.invalidData.length + ' 条数据！')

                  // 导出错误的数据
                  if (this.invalidData.length > 0) {
                    header.push('错误信息')
                    this.exportLoading = true
                    const params = {
                      title: header,
                      key: header,
                      data: this.invalidData,
                      autoWidth: true,
                      filename: `导入错误信息-${this.formatDate(new Date())}`
                    }
                    excel.export_array_to_excel(params)
                    this.exportLoading = false
                  } else {

                  }
                  this.uploadLoading = false
                  this.tableLoading = false
                  // 重新加载数据
                  this.searchData()
                }
              })
            }
          })
        }
      }
    },
    // 验证上传的excel文件第一行的字段是不是包含需要的字段
    titleIsRight (header) {
      return (header.indexOf('品类') > -1) &&
        (header.indexOf('品牌') > -1) &&
        (header.indexOf('产品编号') > -1) &&
        (header.indexOf('产品型号') > -1) &&
        (header.indexOf('SN8') > -1) &&
        (header.indexOf('版本') > -1) &&
        (header.indexOf('功能') > -1) &&
        (header.indexOf('场景') > -1) &&
        (header.indexOf('语音功能') > -1) &&
        (header.indexOf('生态入口') > -1) &&
        (header.indexOf('传感器') > -1)
    },
    // 将一行的数据转化为一个产品
    transFileDataToProduct (data) {
      // 验证数据是不是正确
      let validate = true
      // 如果数据不正确，错误消息
      let errorMsg = ''
      // 数据转换成产品信息
      const result = null

      const categoryTypeName = data['品类']
      const branchName = data['品牌']
      const code = data['产品编号']
      const model = data['产品型号']
      const SN8 = data['SN8']
      const productVersion = data['版本']
      const functionString = data['功能']
      const scenarioString = data['场景']
      const voiceFunctionString = data['语音功能']
      const ecologyEntranceString = data['生态入口']
      const sensorString = data['传感器']

      if (!categoryTypeName || categoryTypeName.replace(' ', '').length === 0) {
        validate = false
        errorMsg = '品类不可以为空！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }
      if (!branchName || branchName.replace(' ', '').length === 0) {
        validate = false
        errorMsg = '品牌不可以为空！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }
      if (!code || code.replace(' ', '').length === 0) {
        validate = false
        errorMsg = '产品编号不可以为空！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }
      if (code.length > 50) {
        validate = false
        errorMsg = '产品编号不可以多于50个字符！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }
      if (!model || model.replace(' ', '').length === 0) {
        validate = false
        errorMsg = '产品型号不可以为空！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }
      if (model.length > 50) {
        validate = false
        errorMsg = '产品型号不可以多于50个字符！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }
      if (!SN8 || SN8.replace(' ', '').length === 0) {
        validate = false
        errorMsg = '产品SN8不可以为空！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }
      if (SN8.length > 50) {
        validate = false
        errorMsg = '产品SN8不可以多于50个字符！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }
      if (productVersion) {
        if (productVersion.length > 50) {
          validate = false
          errorMsg = '产品版本不可以多于50个字符！'
          return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
        }
      }

      const productTypeToImport = this.productType
      if (categoryTypeName !== this.productTypeName) {
        validate = false
        errorMsg = '请检查品类是否正确！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }

      /* const categoryType = this.categoryNameToCategoryType[categoryTypeName]
      if (!categoryType) {
        validate = false
        errorMsg = '请检查品类是否正确！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      } */
      const branch = this.branchNameToBranchCode[branchName]
      if (!branch) {
        validate = false
        errorMsg = '请检查品牌是否正确！'
        return { 'validate': validate, 'errorMsg': errorMsg, 'result': result }
      }

      const funcIdsResult = this.getFunctionIdsByFunctionString(productTypeToImport, functionString)
      if (!funcIdsResult || !funcIdsResult.isRight) {
        validate = false
        let FuncIdsErrorMsg = funcIdsResult.errorMsg
        return { 'validate': validate, 'errorMsg': FuncIdsErrorMsg, 'result': null }
      }

      const scenIdsResult = this.getScenarioIdsByScenarioString(productTypeToImport, scenarioString)
      if (!scenIdsResult || !scenIdsResult.isRight) {
        validate = false
        let scenIdsErrorMsg = scenIdsResult.errorMsg
        return { 'validate': validate, 'errorMsg': scenIdsErrorMsg, 'result': null }
      }
      const voiceFunctionIdsResult = this.getVoiceFunctionIdsByFunctionString(productTypeToImport, voiceFunctionString)
      if (!voiceFunctionIdsResult || !voiceFunctionIdsResult.isRight) {
        validate = false
        let voiceFunctionIdsErrorMsg = voiceFunctionIdsResult.errorMsg
        return { 'validate': validate, 'errorMsg': voiceFunctionIdsErrorMsg, 'result': null }
      }

      const ecologyEntranceIdsResult = this.getEcologyEntranceIdsByEcologyEntranceString(productTypeToImport, ecologyEntranceString)
      if (!ecologyEntranceIdsResult || !ecologyEntranceIdsResult.isRight) {
        validate = false
        let ecologyEntranceIdsErrorMsg = ecologyEntranceIdsResult.errorMsg
        return { 'validate': validate, 'errorMsg': ecologyEntranceIdsErrorMsg, 'result': null }
      }
      const sensorIdsResult = this.getSensorIdsBySensorString(productTypeToImport, sensorString)
      if (!sensorIdsResult || !sensorIdsResult.isRight) {
        validate = false
        let sensorIdsErrorMsg = sensorIdsResult.errorMsg
        return { 'validate': validate, 'errorMsg': sensorIdsErrorMsg, 'result': null }
      }

      const dataToImport = {
        productType: this.productType,
        id: '',
        productCategory: '',
        branch: branch,
        code: code,
        model: model,
        sN8: SN8,
        productVersion: productVersion,
        lifecycleStage: '',
        saleChannel: '',
        functionIds: funcIdsResult.result,
        scenarioIds: scenIdsResult.result,
        voiceFunctionIds: voiceFunctionIdsResult.result,
        ecologyEntranceIds: ecologyEntranceIdsResult.result,
        sensorIds: sensorIdsResult.result
      }
      return { 'validate': validate, 'errorMsg': errorMsg, 'result': dataToImport }
    },
    // 根据产品类型和功能名称，返回产品对应的功能id
    getFunctionIdsByFunctionString (productType, functionString) {
      let isRight = true
      let errorMsg = ''
      const result = null
      const functionIds = []
      if (functionString) {
        const functionNamesArray = functionString.split('、')
        functionNamesArray.forEach((functionName, index, array) => {
          const functionId = this.productTypeToFuncNameAndId[productType][functionName]
          if (functionId) {
            functionIds.push(functionId)
          } else {
            isRight = false
            errorMsg = '不存在 ' + functionName + ' 的功能，请检查后重新导入！'
            return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': result }
          }
        })
      }
      return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': functionIds }
    },
    // 根据产品类型和产品场景名称，获取产品场景id
    getScenarioIdsByScenarioString (productType, scenarioString) {
      let isRight = true
      let errorMsg = ''
      let result = null
      const scenarioIds = []
      if (scenarioString) {
        let scenarioNamesArray = scenarioString.split('、')
        scenarioNamesArray.forEach((scenarioName) => {
          let scenarioId = this.productTypeToScenNameAndId[productType][scenarioName]
          if (scenarioId) {
            scenarioIds.push(scenarioId)
          } else {
            isRight = false
            errorMsg = '不存在 ' + scenarioName + ' 的场景，请检查后重新导入！'
            return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': result }
          }
        })
      }
      return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': scenarioIds }
    },
    // 根据产品语音功能内容，获取产品语音功能id
    getVoiceFunctionIdsByFunctionString (productType, voiceFunctionString) {
      let isRight = true
      let errorMsg = ''
      let result = null
      const voiceFunctionIds = []
      if (voiceFunctionString) {
        let voiceFunctionNamesArray = voiceFunctionString.split('、')
        voiceFunctionNamesArray.forEach((voiceFunctionName) => {
          let voiceFunctionId = this.voiceFunctionNameToId[voiceFunctionName]
          if (voiceFunctionId) {
            voiceFunctionIds.push(voiceFunctionId)
          } else {
            isRight = false
            errorMsg = '不存在 ' + voiceFunctionName + ' 的语音功能，请检查后重新导入！'
            return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': result }
          }
        })
      }
      return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': voiceFunctionIds }
    },
    // 根据产品生态入口内容，获取产品生态id
    getEcologyEntranceIdsByEcologyEntranceString (productType, ecologyEntranceString) {
      let isRight = true
      let errorMsg = ''
      let result = null
      const ecologyEntranceIds = []
      if (ecologyEntranceString) {
        let ecologyEntranceNamesArray = ecologyEntranceString.split('、')
        ecologyEntranceNamesArray.forEach((ecologyEntranceName) => {
          let ecologyEntranceId = this.ecologyEntranceNameToId[ecologyEntranceName]
          if (ecologyEntranceId) {
            ecologyEntranceIds.push(ecologyEntranceId)
          } else {
            isRight = false
            errorMsg = '不存在 ' + ecologyEntranceName + ' 的生态入口，请检查后重新导入！'
            return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': result }
          }
        })
      }
      return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': ecologyEntranceIds }
    },
    // 根据产品传感器内容，获取产品传感器id
    getSensorIdsBySensorString (productType, sensorString) {
      let isRight = true
      let errorMsg = ''
      let result = null
      const sensorIds = []
      if (sensorString) {
        let snesorNamesArray = sensorString.split('、')
        snesorNamesArray.forEach((sensorName) => {
          let sensorId = this.sensorNameToId[sensorName]
          if (sensorId) {
            sensorIds.push(sensorId)
          } else {
            isRight = false
            errorMsg = '不存在 ' + sensorName + ' 的传感器，请检查后重新导入！'
            return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': result }
          }
        })
      }
      return { 'isRight': isRight, 'errorMsg': errorMsg, 'result': sensorIds }
    },

    // 下载批量导入模板
    downloadImportTemplate () {
      let categoryDescription = ''
      let branchDescription = ''
      let codeDescription = ''
      let modelDescription = ''
      let SN8Description = ''
      let productVersionDescription = ''
      let functionDescription = ''
      let scenarioDescription = ''
      let voiceFunctionDescription = ''
      let ecologyEntranceDescription = ''
      let sensorDescription = ''
      let productTypeName = this.productTypeName
      categoryDescription = this.productTypeName
      /*      let allCategoryByTypeString = productTypeName
      categoryDescription = categoryDescription + productTypeName + '产品的可选项为：'
      // let cateList = this.productTypeToCategory[this.productType];
      let cateList = this.categoryList
      cateList.forEach((cateItem) => {
        allCategoryByTypeString = allCategoryByTypeString + cateItem.value + '、'
      })
      if (allCategoryByTypeString.length > 0) {
        allCategoryByTypeString = allCategoryByTypeString.substring(0, allCategoryByTypeString.length - 1)
      }
      categoryDescription = categoryDescription + allCategoryByTypeString + ';' + '\r\n'
      */

      functionDescription = functionDescription + productTypeName + '产品的可选项为：'
      let funcListByType = this.functionList
      let allFuncStringByType = ''
      funcListByType.forEach((funcItem) => {
        allFuncStringByType = allFuncStringByType + funcItem.functionName + '、'
      })
      if (allFuncStringByType.length > 0) {
        allFuncStringByType = allFuncStringByType.substring(0, allFuncStringByType.length - 1)
      }
      functionDescription = functionDescription + allFuncStringByType + ';' + '\r\n'

      scenarioDescription = scenarioDescription + productTypeName + '产品的可选项为：'
      let scenarioListByType = this.scenarioList
      let allScenarioListByTypeString = ''
      scenarioListByType.forEach((scenItem) => {
        allScenarioListByTypeString = allScenarioListByTypeString + scenItem.scenarioName + '、'
      })
      if (allScenarioListByTypeString.length > 0) {
        allScenarioListByTypeString = allScenarioListByTypeString.substring(0, allScenarioListByTypeString.length - 1)
      }
      scenarioDescription = scenarioDescription + allScenarioListByTypeString + ';' + '\r\n'

      voiceFunctionDescription = '可选项为：'
      let voiceFunctionListByType = this.allVoiceFunctionList
      let allVoiceFunctionListByTypeString = ''
      voiceFunctionListByType.forEach((item) => {
        allVoiceFunctionListByTypeString = allVoiceFunctionListByTypeString + item.name + '、'
      })
      if (allVoiceFunctionListByTypeString.length > 0) {
        allVoiceFunctionListByTypeString = allVoiceFunctionListByTypeString.substring(0, allVoiceFunctionListByTypeString.length - 1)
      }
      voiceFunctionDescription = voiceFunctionDescription + allVoiceFunctionListByTypeString + ';' + '\r\n'

      ecologyEntranceDescription = '可选项为：'
      let ecologyEntranceList = this.allEcologyEntranceList
      let allEcologyEntranceString = ''
      ecologyEntranceList.forEach((item) => {
        allEcologyEntranceString = allEcologyEntranceString + item.name + '、'
      })
      if (allEcologyEntranceString.length > 0) {
        allEcologyEntranceString = allEcologyEntranceString.substring(0, allEcologyEntranceString.length - 1)
      }
      ecologyEntranceDescription = ecologyEntranceDescription + allEcologyEntranceString + ';' + '\r\n'

      sensorDescription = sensorDescription + productTypeName + '产品的可选项为：'
      let sensorListByType = this.allSensorList
      let allSensorListByTypeString = ''
      sensorListByType.forEach((sensorItem) => {
        allSensorListByTypeString = allSensorListByTypeString + sensorItem.sensorName + '、'
      })
      if (allSensorListByTypeString.length > 0) {
        allSensorListByTypeString = allSensorListByTypeString.substring(0, allSensorListByTypeString.length - 1)
      }
      sensorDescription = sensorDescription + allSensorListByTypeString + ';' + '\r\n'

      //  });
      scenarioDescription = scenarioDescription + '可以为多个选项，多个选项以 、 隔开，如 NFC、远程控制。'
      functionDescription = functionDescription + '可以为多个选项，多个选项以 、 隔开，如 NFC、远程控制。'
      voiceFunctionDescription = voiceFunctionDescription + '可以为多个选项，多个选项以 、 隔开，如 NFC、远程控制。'
      ecologyEntranceDescription = ecologyEntranceDescription + '可以为多个选项，多个选项以 、 隔开，如 NFC、远程控制。'
      sensorDescription = sensorDescription + '可以为多个选项，多个选项以 、 隔开，如 NFC、远程控制。'
      branchDescription = '不能为空，品牌可选项为：'
      let allBranchString = ''
      this.branchList.forEach((branchItem) => {
        allBranchString = allBranchString + branchItem.value + '、'
      })
      if (allBranchString.length > 0) {
        allBranchString = allBranchString.substring(0, allBranchString.length - 1)
      }
      branchDescription = branchDescription + allBranchString + '。'
      codeDescription = '不能为空，且长度在50以内。'
      modelDescription = '不能为空，且长度在50以内。'
      SN8Description = '不能为空，且长度在50以内。'
      productVersionDescription = '长度在50以内'
      const params = {
        title: ['品类', '品牌', '产品编号', '产品型号', 'SN8', '版本', '功能', '场景', '语音功能', '生态入口', '传感器'],
        key: ['categoryName', 'branchName', 'code', 'model', 'SN8', 'productVersion', 'functionsName', 'scenariosNameSupported', 'voiceFunctionName', 'ecologyEntranceName', 'sensorName'],
        data: [{
          'categoryName': categoryDescription,
          'branchName': branchDescription,
          'code': codeDescription,
          'model': modelDescription,
          'SN8': SN8Description,
          'productVersion': productVersionDescription,
          'functionsName': functionDescription,
          'scenariosNameSupported': scenarioDescription,
          'voiceFunctionName': voiceFunctionDescription,
          'ecologyEntranceName': ecologyEntranceDescription,
          'sensorName': sensorDescription
        }],
        autoWidth: true,
        filename: '导入模板'
      }
      excel.export_array_to_excel(params)
    },
    // 时间格式化为 yyyyMMddHHmmss
    formatDate (time) {
      if (time != null) {
        let datetime = new Date()
        datetime.setTime(time)
        let year = datetime.getFullYear()
        let month = (datetime.getMonth() + 1) < 10 ? '0' + (datetime.getMonth() + 1) : (datetime.getMonth() + 1)
        let date = datetime.getDate() < 10 ? '0' + datetime.getDate() : datetime.getDate()
        let hour = datetime.getHours() < 10 ? '0' + datetime.getHours() : datetime.getHours()
        let minute = datetime.getMinutes() < 10 ? '0' + datetime.getMinutes() : datetime.getMinutes()
        let second = datetime.getSeconds() < 10 ? '0' + datetime.getSeconds() : datetime.getSeconds()
        return year + '' + month + '' + date + '' + hour + '' + minute + '' + second
      } else {
        return '---'
      }
    },
    setColumns () {
      this.columns = []
      // 如果有导出权限，显示选择框；没有导出权限，就不显示选择框了
      if (this.accessExport) {
        this.columns.push({
          type: 'selection',
          maxWidth: 45,
          align: 'center'
        })
      }
      this.columns.push(
        {
          title: '品类',
          maxWidth: 129,
          key: 'productTypeName'
        }, {
          title: '品牌',
          maxWidth: 96,
          key: 'branchName'
        }, {
          title: '产品编号',
          maxWidth: 130,
          key: 'code'
        }, {
          title: '产品型号',
          maxWidth: 130,
          key: 'model'
        },
        {
          title: 'SN8',
          maxWidth: 130,
          key: 'sN8'
        },
        {
          title: '版本',
          key: 'productVersion'
        },
        {
          title: '功能',
          key: 'functionsName',
          render: (h, params) => {
            let f = params.row.functionsName
            return h('div', { style: { whiteSpace: 'pre-line' } }, f.replace(/、/g, '\n\r'))
          }
        },
        {
          title: '场景',
          key: 'scenariosNameSupported',
          render: (h, params) => {
            let f = params.row.scenariosNameSupported
            return h('div', { style: { whiteSpace: 'pre-line' } }, f.replace(/、/g, '\n\r'))
          }
        },
        {
          title: '语音功能',
          key: 'voiceFunctionName'
        },
        {
          title: '生态入口',
          key: 'ecologyEntranceName'
        },
        {
          title: '传感器',
          key: 'sensorName'
        })
      /*      this.columns.push({
              title: '插件UI',
              maxWidth: 90,
              render: (h, params) => {
                let updateButton = h('Button', {
                  props: {
                    type: 'text',
                    size: 'small'
                  },
                  on: {
                    // 编辑按钮点击事件
                    click: () => {
                      let alink = document.createElement('a')
                      alink.href = this.viewPicContext + params.row.pic
                      alink.download = params.row.productTypeName + params.row.code + '-' + params.row.model + '插件UI'// 图片名
                      alink.click()
                    }
                  }
                }, '插件UI')
                let a = []
                if (params.row.pic) {
                  a.push(updateButton)
                }
                return h('div', a)
              }
            })*/
      // 有产品更新权限和产品删除权限的用户才能看到 编辑 和 删除 两个按钮
      if (this.accessUpdate || this.accessDelete) {
        this.columns.push({
          title: '操作',
          key: 'action',
          maxWidth: 120,
          align: 'center',
          render: (h, params) => {
            let updateButton = h('Button', {
              props: {
                type: 'primary',
                size: 'small'
              },
              on: {
                // 编辑按钮点击事件
                click: () => {
                  // this.productData = params.row
                  this.productData = {
                    productType: params.row.productType,
                    productTypeName: params.row.productTypeName,
                    id: params.row.id,
                    productCategory: params.row.productCategory,
                    branch: params.row.branch,
                    code: params.row.code,
                    model: params.row.model,
                    lifecycleStage: params.row.lifecycleStage,
                    saleChannel: params.row.saleChannel,
                    functionIds: params.row.functionIds,
                    scenarioIds: params.row.scenarioIds,
                    sN8: params.row.sN8,
                    productVersion: params.row.productVersion,
                    voiceFunctionIds: params.row.voiceFunctionIds,
                    ecologyEntranceIds: params.row.ecologyEntranceIds,
                    sensorIds: params.row.sensorIds,
                    pic: params.row.pic
                  }
                  if (params.row.pic) {
                    this.uploadList = [{
                      name: params.row.pic,
                      url: this.viewPicContext + params.row.pic,
                      status: 'finished'
                    }]
                  } else {
                    this.uploadList = []
                  }
                  this.drawerTitle = '编辑产品'
                  this.showAddDrawer()
                }
              }
            }, '编辑')
            let deleteButton = h('Button', {
              props: {
                type: 'error',
                size: 'small'
              },
              style: {
                marginLeft: '3px'
              },
              on: {
                // 删除按钮点击事件
                click: () => {
                  this.$Modal.confirm({
                    title: '确定要删除该产品吗？',
                    onOk: () => {
                      this.remove(params.index, params.row.id)
                    },
                    onCancel: () => {
                    }
                  })
                }
              }
            }, '删除')

            let buttons = []
            if (this.accessUpdate) {
              buttons.push(updateButton)
            }
            if (this.accessDelete) {
              buttons.push(deleteButton)
            }
            return h('div', buttons)
          }
        })
      }
    },
    // 删除产品
    remove (index, id) {
      // 删除产品时，确认当前登录用户时候有权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
        this.$Message.error('当前用户没有删除权限！')
      }
      // 根据token获取当前登录用户
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，通过用户权限和跳转的页面的name来判断是否有权限访问;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        if (this.accessProductType) {
          if (this.accessDelete) {
            deleteProductById(id).then(res => {
              if (res.data.errorCode && res.data.errorCode === '0') {
                this.tableData.splice(index, 1)
                this.$Message.success('删除产品成功！')
                this.tableDataCount = this.tableData.length
              } else {
                this.$Message.error('删除产品失败！')
              }
            })
          } else {
            this.$Message.error('当前用户没有删除产品权限！')
          }
        } else {
          this.$Message.error('当前用户此类产品的权限！')
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('删除失败！')
      })
    },
    // 展示 添加 更新 产品的弹窗
    showAddDrawer () {
      this.productData.productType = this.productType
      this.productData.productTypeName = this.productTypeToTypeName[this.productType]
      if (!this.productData.id || this.productData.id === '') {
        this.isUpdate = false
        this.uploadList = []
      } else {
        this.isUpdate = true
      }
      this.drawer = true
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
                  productVersion: '',
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
                this.drawer = false
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
        productVersion: '',
        lifecycleStage: '',
        saleChannel: '',
        functionIds: [],
        scenarioIds: [],
        voiceFunctionIds: [],
        ecologyEntranceIds: [],
        sensorIds: [],
        pic: ''
      }
      this.drawer = false
    },
    // 关闭产品编辑页面弹窗时，将该弹窗的数据清除
    closeDrawer () {
      this.productData = {
        productType: this.productType,
        id: '',
        categoryType: '',
        branch: '',
        code: '',
        model: '',
        sN8: '',
        productVersion: '',
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
    // 条件查询产品
    searchData () {

      this.loadingProduct = true
      // 搜索产品时，确认当前登录用户时候有权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      // 根据token获取当前登录用户
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，获取用户权限存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 判断是否有该类型产品的权限
        if (this.accessProductType) {
          this.productDataForSearch.productType = []
          this.productDataForSearch.productType.push(this.productType)
          this.productDataForSearch.pageSize=this.pageSize
          this.productDataForSearch.pageNumber = this.pageNumber
          queryProduct(this.productDataForSearch).then(res => {
            if (res.data.result) {
              this.tableData = res.data.result
            } else {
              this.tableData = []
            }
            if (this.tableData && this.tableData.length > 0) {
              this.tableDataCount = this.tableData[0].totalCount
            } else {
              this.tableDataCount = 0
            }
          }).catch(reason => {
            this.loadingProduct = false
          }).finally(() => {
            this.loadingProduct = false
          })
        } else {
          this.$Message.error('当前用户没有此类产品的权限！')
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('搜索失败！')
        this.loadingProduct = false
      })
    },
    initData () {
      this.loadingProduct = true
      this.setColumns()
      queryProduct({ 'productType': [this.productType] }).then(res => {
        if (res.data.result) {
          this.tableData = res.data.result
        } else {
          this.tableData = []
        }
        if (this.tableData && this.tableData.length > 0) {
          this.tableDataCount = this.tableData[0].totalCount
        } else {
          this.tableDataCount = 0
        }
        //this.tableDataCount = this.tableData.length
      }).catch(reason => {
        this.$Message.error('获取产品失败:' + reason)
        this.loadingProduct = false
      }).finally(() => {
        this.loadingProduct = false
      })
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
      // 获取品牌
      getBranchList().then(result => {
        if (result.data.result) {
          this.branchList = result.data.result
          this.branchList.forEach((item) => {
            this.branchNameToBranchCode[item.value] = item.code
          })
        }
      })
      // 获取功能
      getFunctionByType(this.productType).then(res => {
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
  mounted () {
    this.productType = this.$route.meta.productType
    this.initData()
    /*queryProduct({ 'productType': [this.productType] }).then(res => {
      if (res.data.result) {
        this.tableData = res.data.result
      } else {
        this.tableData = []
      }
      this.tableDataCount = this.tableData.length
    })*/

  },
  beforeMount () {
    /*  // 类型根据传过来的数据赋值
      this.productType = this.$route.meta.productType
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
      // 获取品牌
      getBranchList().then(result => {
        if (result.data.result) {
          this.branchList = result.data.result
          this.branchList.forEach((item) => {
            this.branchNameToBranchCode[item.value] = item.code
          })
        }
      })
      // 获取功能
      getFunctionByType(this.productType).then(res => {
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
      */
  },
  computed: {
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
    // 判断是否有导入产品的权限，
    accessImport () {
      return hasOneOf(['super_admin', 'admin', 'product_import'], this.access)
    },
    // 判断是否有导出产品的权限，
    accessExport () {
      return hasOneOf(['super_admin', 'admin', 'product_export'], this.access)
    },
    // 判断是否有更新产品的权限，
    accessUpdate () {
      return hasOneOf(['super_admin', 'admin', 'product_update'], this.access)
    },
    // 判断是否有删除产品的权限，
    accessDelete () {
      return hasOneOf(['super_admin', 'admin', 'product_delete'], this.access)
    }
  },
  watch: {
    '$route' () {

      // 类型根据传过来的数据赋值
      this.productType = this.$route.meta.productType
      //this.$Message.success(this.productType)
      this.initData()
      /*
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
            // 获取品牌
            getBranchList().then(result => {
              if (result.data.result) {
                this.branchList = result.data.result
                this.branchList.forEach((item) => {
                  this.branchNameToBranchCode[item.value] = item.code
                })
              }
            })
            // 获取功能
            getFunctionByType(this.productType).then(res => {
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
            queryProduct({ 'productType': [this.productType] }).then(res => {
              if (res.data.result) {
                this.tableData = res.data.result
              } else {
                this.tableData = []
              }
              this.tableDataCount = this.tableData.length
            })
      */

    }
  }
}
</script>

<style>
.demo-upload-list {
  display: inline-block;
  width: 60px;
  height: 60px;
  text-align: center;
  line-height: 60px;
  border: 1px solid transparent;
  border-radius: 4px;
  overflow: hidden;
  background: #fff;
  position: relative;
  box-shadow: 0 1px 1px rgba(0, 0, 0, .2);
  margin-right: 4px;
}

.demo-upload-list img {
  width: 100%;
  height: 100%;
}

.demo-upload-list-cover {
  display: none;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, .6);
}

.demo-upload-list:hover .demo-upload-list-cover {
  display: block;
}

.demo-upload-list-cover i {
  color: #fff;
  font-size: 20px;
  cursor: pointer;
  margin: 0 2px;
}
</style>
