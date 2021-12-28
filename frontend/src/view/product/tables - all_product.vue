<template>
  <div>
      <span>
        <Dropdown v-if="accessAdd">
        <Button style="width:190px" type="primary">
            添加<Icon type="ios-arrow-down"></Icon>
        </Button>
         <DropdownMenu slot="list">
            <DropdownItem v-if="accessElectricHeater">
              <Button style="width:160px" @click="addProductByType('electric_heater')">电热水器</Button>
            </DropdownItem>
           <DropdownItem v-if="accessGasHeaterStove">
              <Button style="width:160px" @click="addProductByType('gas_heater_stove')">燃气热水器</Button>
            </DropdownItem>
                      <DropdownItem v-if="accessGasStove">
              <Button style="width:160px" @click="addProductByType('gas_stove')">燃气炉</Button>
            </DropdownItem>
           <DropdownItem v-if="accessWaterPurification">
              <Button style="width:160px" @click="addProductByType('water_purification')">净水机</Button>
            </DropdownItem>
           <DropdownItem v-if="accessWaterDrink">
              <Button style="width:160px" @click="addProductByType('water_drink')">饮水机(含净饮机)</Button>
            </DropdownItem>
           <DropdownItem v-if="accessRangHoodType">
              <Button style="width:160px" @click="addProductByType('rang_hood_type')">吸油烟机</Button>
            </DropdownItem>
           <DropdownItem v-if="accessIntegratedGasCombinedKitchen">
              <Button style="width:160px"
                      @click="addProductByType('integrated_gas_combined_kitchen')">集成灶</Button>
           </DropdownItem>
           <DropdownItem v-if="accessGasCombinedKitchen">
              <Button style="width:160px"
                      @click="addProductByType('gas_combined_kitchen')">燃气灶(含组合灶)</Button>
           </DropdownItem>
           <DropdownItem v-if="accessDiswacherType">
              <Button style="width:160px" @click="addProductByType('diswasher_type')">洗碗机</Button>
            </DropdownItem>
           <DropdownItem v-if="accessDisinfectionCabinetType">
              <Button style="width:160px" @click="addProductByType('disinfection_cabinet_type')">消毒柜</Button>
            </DropdownItem>
         </DropdownMenu>
        </Dropdown>
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
      </span>
    <span>
      <Card>
        <Form :model="productDataForSearch" label-position="right" :label-width="65">
        <Row :gutter="0">
          <Col span="5">
            <FormItem label="品类:">
              <Select v-model="productDataForSearch.productTypeSelected" placeholder="请选择产品类型" clearable
                      @on-change="searchProductTypeSelectChange">
                <Option v-for="item in allProductType" :value="item.code" :key="item.code">{{ item.value }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="品牌:">
              <Select v-model="productDataForSearch.branch" placeholder="请选择品牌" clearable>
                <Option v-for="item in branchList" :value="item.code" :key="item.code">{{ item.value }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="产品编码:" :label-width="80">
              <Input v-model="productDataForSearch.productCode" :maxlength="50" placeholder="请输入产品编号，50个字符以内"
                     clearable></Input>
            </FormItem>
          </Col>
          <Col span="4">
            <FormItem label="产品型号:" :label-width="80">
              <Input v-model="productDataForSearch.productModel" :maxlength="50" placeholder="请输入产品型号，50个字符以内"
                     clearable></Input>
            </FormItem>
          </Col>
          <Col span="4">
            <FormItem label="SN8:" :label-width="80">
              <Input v-model="productDataForSearch.productSN8" :maxlength="50" placeholder="请输入产品SN8，50个字符以内"
                     clearable></Input>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="0">
          <Col span="5">
            <FormItem label="产品功能:" :label-width="80">
              <Select v-if="productDataForSearch.productTypeSelected" v-model="productDataForSearch.function"
                      placeholder="请选择产品功能" not-found-text="当前品类没有功能选项" clearable>
                <Option v-for="item in productTypeToFunctionList[productDataForSearch.productTypeSelected]"
                        :value="item.id"
                        :key="item.id">{{ item.functionName }}</Option>
              </Select>
              <Select v-else v-model="productDataForSearch.functionName" placeholder="请选择产品功能" clearable>
                <Option v-for="item in allProductTypeFunctionList" :value="item"
                        :key="item">{{ item }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="5">
            <FormItem label="产品场景:" :label-width="80">
              <Select v-if="productDataForSearch.productTypeSelected" v-model="productDataForSearch.scenario"
                      placeholder="请选择产品场景" not-found-text="请先选择品类" clearable>
                <Option v-for="item in productTypeToScenarioList[productDataForSearch.productTypeSelected]"
                        :value="item.id"
                        :key="item.id">{{ item.scenarioName }}</Option>
              </Select>
              <Select v-else v-model="productDataForSearch.scenarioName" placeholder="请选择产品场景" not-found-text="请先选择类型"
                      clearable>
                <Option v-for="item in allProductTypeScenarioList" :value="item"
                        :key="item">{{ item }}</Option>
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
          <Col span="4">
            <FormItem label="生态入口:" :label-width="80">
              <Select v-model="productDataForSearch.ecologyEntrance" placeholder="请选择产品生态入口" clearable>
                <Option v-for="item in allEcologyEntranceList" :value="item.id"
                        :key="item.id">{{ item.name }}</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="4">
            <FormItem label="传感器:" :label-width="80">
              <Select v-if="productDataForSearch.productTypeSelected" v-model="productDataForSearch.sensor"
                      placeholder="请选择产品传感器" clearable>
                <Option v-for="item in productTypeToSensorList[productDataForSearch.productTypeSelected]"
                        :value="item.id"
                        :key="item.id">{{ item.sensorName }}</Option>
              </Select>
              <Select v-else v-model="productDataForSearch.sensorName" placeholder="请选择产品传感器"
                      clearable>
                <Option v-for="item in allProductTypeSensorList" :value="item"
                        :key="item">{{ item }}</Option>
              </Select>
            </FormItem>
          </Col>
           <Col span="1" style="text-align: right">
             <Button style="margin-left: 10px" :loading="searchLoading" type="primary"
                     @click="searchData">搜索</Button>
          </Col>
        </Row>
       </Form>
      </Card>
    </span>

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
            <FormItem label="品类:" label-position="top">
              <div style="margin-left:10px">{{ productData.productTypeName }}</div>
            </FormItem>
          </Col>
        </Row>

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
                <Input disabled v-model="productData.productVersion" :maxlength="50" placeholder=""
                       clearable></Input>
              </div>
              <div v-else>
                <Input v-model="productData.productVersion" :maxlength="50" placeholder="请输入产品版本号，50个字符以内"
                       clearable></Input>
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
    <Modal v-model="deleteSelectedProductModal" title="确认删除">
      <div style="text-align: center;font-size: 18px">删除后数据无法恢复，确认删除吗</div>
      <div slot="footer">
        <Button @click="cancelDeleteSelectedProduct">取消删除</Button>
        <Button type="primary" @click="confirmDeleteSelectedProduct">确认删除</Button>
      </div>
    </Modal>
    <Card>
      <Spin size="large" fix v-if="loadingProduct"/>
      <Spin size="large" fix v-if="loadingDeleteProduct"/>

      <div>
        <span>共查询到 {{ tableDataCount }} 条数据</span>
        <tables ref="tables" editable border stripe v-model="tableData" :columns="columns"
                @on-select="selectProduct"
                @on-select-cancel="selectProductCancel"
                @on-select-all="selectAllProduct"
                @on-select-all-cancel="selectAllProductCancel"
                @on-selection-change="selectChange"/>
        <div style="float: right ;margin-top:15px">
          <Page :total="tableDataCount" show-sizer transfer :page-size="pageSize"
                :current="pageNumber" show-total :page-size-opts="[10, 20, 30, 40,60,70,80,90,100]"
                @on-change="getProductByPageNumberAndPageSize"
                @on-page-size-change="changePageSize"
          />
        </div>
      </div>

      <Button v-if="accessDelete" style="margin-right: 20px" :loading="deleteSelectedProductLoading" type="default"
              @click="deleteSelectedProduct">
        删除选中产品
      </Button>

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
  getProductType,
  getScenarioByType,
  queryProduct,
  getProductCategoryByProductType,
  getBranchList,
  getFunctionByType,
  saveProduct,
  getVoiceFunction,
  getEcologyEntrance,
  getSensorByType,
  deleteSelectedProductByIds
} from '@/api/data'
import { hasOneOf } from '@/libs/tools'
import store from '@/store'
import { getToken, setToken } from '@/libs/util'
import excel from '@/libs/excel'
import config from '@/config'

export default {
  name: 'all_table',
  components: {
    Tables
  },
  data () {
    return {
      loadingDeleteProduct: false,
      deleteSelectedProductModal: false,
      deleteSelectedProductLoading: false,
      pageSize: 10,
      pageNumber: 1,
      uploadMethod: config.baseUrl.pro + 'product/uploadOperationPanelPic',
      viewPicContext: config.baseUrl.pro + 'upload/',
      loadingProduct: true,
      searchLoading: false,
      tableDataCount: 0,
      exportLoading: false,
      uploadDataCount: 0,
      importTotal: 0,
      importErrorTotal: 0,
      invalidData: [],
      uploadLoading: false,
      progressPercent: 0,
      showProgress: false,
      showRemoveFile: false,
      file: null,
      tableLoading: false,
      selectDatas: [],
      categoryNameToProductType: {},
      categoryNameToCategoryType: {},
      branchNameToBranchCode: {},
      ecologyEntranceNameToEcologyEntranceId: {},
      voiceFunctionNameToVoiceFunctionId: {},
      voiceFunctionNameToId: {},
      ecologyEntranceNameToId: {},
      productTypeToFuncNameAndId: {},
      productTypeToScenNameAndId: {},
      productTypeToFunctionList: {},
      productTypeToScenarioList: {},
      allProductTypeFunctionList: [],
      allProductTypeScenarioList: [],
      allProductTypeSensorList: [],
      productTypeToSensorList: {},
      productTypeToSensorNameAndId: {},
      allProductType: [],
      productTypeToCategory: {},
      productTypeNameToProductType: {},
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
        lifecycleStage: '',
        saleChannel: '',
        functionIds: [],
        scenarioIds: [],
        voiceFunctionIds: [],
        ecologyEntranceIds: [],
        sensorIds: [],
        pic: '',
        productVersion: ''
      },
      isUpdate: false,
      productDataForSearch: {
        productTypeSelected: '',
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
        functionName: '',
        scenario: '',
        scenarioName: '',
        voiceFunction: '',
        ecologyEntrance: '',
        sensor: '',
        sensorName: '',
        pageSize: 10,
        pageNumber: 1
      },
      categoryList: [],
      branchList: [],
      functionList: [],
      scenarioList: [],
      allVoiceFunctionList: [],
      allEcologyEntranceList: [],
      allSensorList: [],
      drawerTitle: '添加产品',
      importProductData: [],
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
        gas_combined_kitchen: 'prodcut_gas_combined_kitchen'
      },
      authToProductType: {
        product_electric_heater: 'electric_heater',
        product_gas_heater_stove: 'gas_heater_stove',
        product_water_purification: 'water_purification',
        product_water_drink: 'water_drink',
        product_rang_hood_type: 'rang_hood_type',
        product_integrated_gas_combined_kitchen: 'integrated_gas_combined_kitchen',
        product_diswasher_type: 'diswasher_type',
        product_disinfection_cabinet_type: 'disinfection_cabinet_type',
        product_gas_stove: 'gas_stove',
        prodcut_gas_combined_kitchen: 'gas_combined_kitchen'
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
      defaultList: [],
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
      this.getProductByCondition()
    },
    changePageSize (pageSize) {
      this.pageSize = pageSize
      if (this.pageNumber === 1) {
        this.getProductByCondition()
      }
      //this.getProductByCondition()
    },
    deleteSelectedProduct () {
      if (!this.selectDatas || this.selectDatas.length === 0) {
        this.$Message.info('请选择要批量删除的产品。')
        return
      }
      this.deleteSelectedProductModal = true
    },
    cancelDeleteSelectedProduct () {
      this.deleteSelectedProductModal = false
    },
    confirmDeleteSelectedProduct () {
      this.deleteSelectedProductModal = false
      this.loadingDeleteProduct = true
      let selectedProductIds = []
      this.selectDatas.forEach(value => {
        selectedProductIds.push(value.id)
      })
      let params = {
        productIds: selectedProductIds
      }
      deleteSelectedProductByIds(params).then(res => {
        if (res.data.errorCode === '0') {
          let newCount = this.tableDataCount - selectedProductIds.length
          if (newCount < 0) {
            this.pageNumber = 1
          } else if (this.pageNumber > 1) {

            if (newCount % this.pageSize === 0) {
              this.pageNumber = newCount / this.pageSize
            } else {
              this.pageNumber = (newCount / this.pageSize) + 1
            }
          }
          this.selectDatas = []
          this.getProductByCondition()
        } else {
          this.$Message.error('批量删除失败：' + res.data.msg)
        }
      }).catch(reason => {
        this.$Message.error('批量删除失败：' + reason)
        this.loadingDeleteProduct = false
      }).finally(() => {
        this.loadingDeleteProduct = false
      })
    },
    // 选中一个
    selectProduct () {

    },
    // 取消选中一个
    selectProductCancel () {

    },
    // 全选
    selectAllProduct () {

    },
    // 取消全选
    selectAllProductCancel () {

    },
    // 选中项发生改变，将选中的项赋值给this.selectDatas
    selectChange (selection) {
      this.selectDatas = selection
    },
    // 导出Excel
    exportExcel () {
      // 重新获取token，更新当前页面的token
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      // 根据token，查找用户权限
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，获取用户权限存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 判断是否有导出权限
        if (this.accessExport) {
          // 判断是否有选中项
          if (this.selectDatas.length > 0) {
            // 正在导出加载中
            this.exportLoading = true
            const params = {
              title: ['品类', '品牌', '产品编号', '产品型号', 'SN8', '版本', '功能', '场景', '语音功能', '生态入口', '传感器'],
              key: ['productTypeName', 'branchName', 'code', 'model', 'sN8', 'productVersion', 'functionsName', 'scenariosNameSupported', 'voiceFunctionName', 'ecologyEntranceName', 'sensorName'],
              comments: this.selectDatas,
              data: this.selectDatas,
              autoWidth: true,
              filename: `产品信息-${this.formatDate(new Date())}`
            }
            // 导出excel文件
            excel.export_array_to_excel(params)
            this.exportLoading = false
          } else {
            this.$Message.info('请选择要导出的数据！')
          }
        } else {
          this.$Message.info('当前用户没有导出权限！')
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('导出失败！')
      })
    },
    setColumns () {
      // 如果有导出权限，数据前面加选中框
      if (this.accessExport) {
        this.columns.push({
          type: 'selection',
          maxWidth: 45,
          align: 'center'
        })
      }
      this.columns.push({
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
        }, {
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
        }, {
          title: '场景',
          key: 'scenariosNameSupported',
          render: (h, params) => {
            let s = params.row.scenariosNameSupported
            return h('div', { style: { whiteSpace: 'pre-line' } }, s.replace(/、/g, '\n\r'))
          }
        }, {
          title: '语音功能',
          key: 'voiceFunctionName'
        }, {
          title: '生态入口',
          key: 'ecologyEntranceName'
        }, {
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
      // 如果有删除或者更新权限，显示 操作 一列
      if (this.accessUpdate || this.accessDelete) {
        this.columns.push({
          title: '操作',
          key: 'action',
          maxWidth: 120,
          align: 'center',
          render: (h, params) => {
            // 根据权限显示 修改按钮 和 删除按钮
            let updateButton = h('Button', {
              props: {
                type: 'primary',
                size: 'small'
              },
              on: {
                // 编辑按钮点击事件
                click: () => {
                  // 产品类型根据当前数据的产品类型
                  this.productType = params.row.productType
                  // 弹窗展示的数据赋值
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
                  // 弹窗确认框，确认是否删除该数据
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
            let operationButton = []
            if (this.accessUpdate) {
              operationButton.push(updateButton)
            }
            if (this.accessDelete) {
              operationButton.push(deleteButton)
            }
            return h('div', operationButton)
          }
        })
      }
    },
    // 删除产品
    remove (index, id) {
      // 根据token，判断当前用户是否有权限删除该数据
      // 重新获取token，更新当前页面的token
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      // 根据token，查找用户权限
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，获取用户权限存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 判断删除产品的权限
        if (this.accessDelete) {
          deleteProductById(id).then(res => {
            if (res.data.errorCode && res.data.errorCode === '0') {
              this.tableData.splice(index, 1)
              this.tableDataCount = this.tableData.length
              this.$Message.success('删除产品成功！')
            } else {
              this.$Message.error('删除产品失败:' + res.data.msg)
            }
          })
        } else {
          this.$Message.error('当前用户没有删除权限！')
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('删除失败！')
      })
    },
    // 展示添加 编辑产品的弹窗
    showAddDrawer () {
      this.productData.productType = this.productType
      this.categoryList = this.productTypeToCategory[this.productType]
      this.functionList = this.productTypeToFunctionList[this.productType]
      this.scenarioList = this.productTypeToScenarioList[this.productType]
      this.allSensorList = this.productTypeToSensorList[this.productType]

      if (!this.productData.id || this.productData.id === '') {
        this.isUpdate = false
      } else {
        this.isUpdate = true
      }
      this.drawer = true
    },
    // 保存、更新产品信息
    saveProduct () {
      // 获取登录用户的token，根据token获取当前用户是否有权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，获取用户权限存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 根据 this.productData 是否有id判断是更新还是添加
        let addProductBoolean = false
        let updateProductBoolean = false

        if (this.productData.id && this.productData.id !== '') {
          addProductBoolean = false
          updateProductBoolean = true
        } else {
          addProductBoolean = true
          updateProductBoolean = false
        }
        // 如果是更新且有更权限 或者， 添加且有添加权限
        if ((addProductBoolean && this.accessAdd) || (updateProductBoolean && this.accessUpdate)) {
          saveProduct(this.productData).then(result => {
            if (result.data.errorCode && result.data.errorCode === '0') {
              this.$Message.success('产品保存成功！')
              // 保存之后，当前弹窗数据清空关闭
              this.productData = {
                productType: '',
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
                pic: '',
                productVersion: ''
              }
              this.getProductByCondition()
              this.drawer = false
            } else {
              if (addProductBoolean) {
                this.$Message.error('添加产品失败:' + result.data.msg)
              } else {
                this.$Message.error('更新产品失败：' + result.data.msg)
              }
            }
          })
        } else {
          if (addProductBoolean) {
            this.$Message.error('当前用户没有添加产品权限')
          } else {
            this.$Message.error('当前用户没有更新产品权限')
          }
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('保存产品失败！')
      })
    },
    // 添加产品按钮事件
    addProductByType (type) {
      this.productType = type
      this.productData.productTypeName = this.productTypeToTypeName[type]
      this.uploadList = []
      this.showAddDrawer()
    },
    // 关闭 编辑产品 的弹窗，把已填写的数据清空
    cancelSaveProduct () {
      this.productData = {
        productType: '',
        id: '',
        categoryType: '',
        branch: '',
        code: '',
        model: '',
        lifecycleStage: '',
        saleChannel: '',
        functionIds: [],
        scenarioIds: [],
        sN8: '',
        voiceFunctionIds: [],
        ecologyEntranceIds: [],
        sensorIds: [],
        pic: '',
        productVersion: ''
      }
      this.drawer = false
    },
    // 点击右上角的 关闭 按钮，关闭 编辑产品 的弹窗，把已填写的数据清空
    closeDrawer () {
      this.productData = {
        productType: '',
        id: '',
        categoryType: '',
        branch: '',
        code: '',
        model: '',
        lifecycleStage: '',
        saleChannel: '',
        functionIds: [],
        scenarioIds: [],
        sN8: '',
        voiceFunctionIds: [],
        ecologyEntranceIds: [],
        sensorIds: [],
        pic: '',
        productVersion: ''
      }
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
    // 上传文件预处理，读取文件内容，只接受 xlsx 和 xls 格式文件
    handleBeforeUpload (file) {
      // 获取登录用户的token，根据token获取当前用户是否有权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，获取用户权限存储到 this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 判断是否有 导入权限
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
          this.$Message.error('当前用户没有导入权限')
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
    // 上传文件
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
        // 将excel中的数据转化成表头数组 和 数据数组
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
          return
        }
        // 遍历数据
        results.forEach((data, index, array) => {
          // 将每一行的数据转化成产品信息
          const transFileToData = this.transFileDataToProduct(data)
          // 验证没有通过
          if (!transFileToData || !transFileToData.validate) {
            data['错误信息'] = transFileToData.errorMsg
            this.invalidData.push(data)
            this.uploadDataCount = this.uploadDataCount - 1
            // 展示导入结果和失败的数据
            if (this.uploadDataCount <= 0) {
              this.$Message.success('导入成功 ' + this.importTotal + ' 条数据，导入失败 ' + this.invalidData.length + ' 条数据！')

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
              this.getProductByCondition()
            }
          } else {
            // 数据验证通过，保存数据
            saveProduct(transFileToData.result).then(res => {
              if (res.data.errorCode && res.data.errorCode === '0') {
                this.importTotal = this.importTotal + 1
              } else {
                data['错误信息'] = res.data.msg
                this.invalidData.push(data)
              }
              // 计算是否导入完毕
              this.uploadDataCount = this.uploadDataCount - 1
              // 展示导入结果
              if (this.uploadDataCount <= 0) {
                this.$Message.success('导入成功 ' + this.importTotal + ' 条数据，导入失败 ' + this.invalidData.length + ' 条数据！')

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
                this.getProductByCondition()
              }
            })
          }
        })
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
      let validate = true
      let errorMsg = ''
      const result = null

      const categoryTypeName = data['品类']
      const branchName = data['品牌']
      const code = data['产品编号']
      const model = data['产品型号']
      const functionString = data['功能']
      const scenarioString = data['场景']
      const SN8 = data['SN8']
      const productVersion = data['版本']
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
      const productTypeToImport = this.productTypeNameToProductType[categoryTypeName]
      if (!productTypeToImport) {
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
        productType: productTypeToImport,
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
    // 根据产品类型和产品功能，返回产品关联的功能id
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
    // 根据产品类型和场景名称，获取产品的场景id
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
          let sensorId = this.productTypeToSensorNameAndId[productType][sensorName]
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
    // 获取产品类型 产品品类 品牌 功能 场景 等字典
    queryDictionary () {
      // 获取所有产品类型
      getProductType().then(res => {
        if (res.data.result && res.data.errorCode === '0') {
          // 产品类型只对应有权限的类型
          this.allProductType = []
          res.data.result.forEach((item) => {
            let authTemp = this.productTypeToAuth[item.code]
            if (hasOneOf(['super_admin', 'admin', authTemp], this.access)) {
              this.allProductType.push(item)
            }
          })

          // this.allProductType = res.data.result
          // 对于每一个产品类型，查找其对应品类 功能 场景
          res.data.result.forEach((item) => {
            // 获取产品类型名称对应产品类型编码
            this.productTypeNameToProductType[item.value] = item.code
            // 获取对应产品类型的品类
            getProductCategoryByProductType(item.code).then(result => {
              if (result.data.result && result.data.errorCode === '0') {
                let categoryAll = result.data.result
                this.productTypeToCategory[item.code] = categoryAll
                categoryAll.forEach((cate) => {
                  this.categoryNameToProductType[cate.value] = item.code
                  this.categoryNameToCategoryType[cate.value] = cate.code
                })
              }
            })
            // 获取对应产品类型的功能
            getFunctionByType(item.code).then(result => {
              if (result.data.result && result.data.errorCode === '0') {
                let allFunctionsByType = result.data.result
                this.productTypeToFunctionList[item.code] = allFunctionsByType
                let functionNameToFunctionId = {}
                allFunctionsByType.forEach((func) => {
                  functionNameToFunctionId[func.functionName] = func.id
                  if (this.allProductTypeFunctionList) {
                    if (this.allProductTypeFunctionList.indexOf(func.functionName) <= -1) {
                      this.allProductTypeFunctionList.push(func.functionName)
                    }
                  } else {
                    this.allProductTypeFunctionList = []
                    this.allProductTypeFunctionList.push(func.functionName)
                  }
                })
                this.productTypeToFuncNameAndId[item.code] = functionNameToFunctionId
              }
            })
            // 获取对应产品类型的场景
            getScenarioByType(item.code).then(result => {
              if (result.data.result) {
                let allScenByType = result.data.result
                this.productTypeToScenarioList[item.code] = allScenByType
                let scenarioNameToScenarioId = {}
                allScenByType.forEach((scen) => {
                  scenarioNameToScenarioId[scen.scenarioName] = scen.id
                  if (this.allProductTypeScenarioList) {
                    if (this.allProductTypeScenarioList.indexOf(scen.scenarioName) <= -1) {
                      this.allProductTypeScenarioList.push(scen.scenarioName)
                    }
                  } else {
                    this.allProductTypeScenarioList = []
                    this.allProductTypeScenarioList.push(scen.scenarioName)
                  }

                })
                this.productTypeToScenNameAndId[item.code] = scenarioNameToScenarioId
              }
            })
            // 获取对应的传感器
            getSensorByType(item.code).then(result => {
              if (result.data.result) {
                let allSensorByType = result.data.result
                this.productTypeToSensorList[item.code] = allSensorByType
                let sensorNameToSensorId = {}
                allSensorByType.forEach((sensor) => {
                  sensorNameToSensorId[sensor.sensorName] = sensor.id
                  if (this.allProductTypeSensorList) {
                    if (this.allProductTypeSensorList.indexOf(sensor.sensorName) <= -1) {
                      this.allProductTypeSensorList.push(sensor.sensorName)
                    }
                  } else {
                    this.allProductTypeSensorList = []
                    this.allProductTypeSensorList.push(sensor.sensorName)
                  }

                })
                this.productTypeToSensorNameAndId[item.code] = sensorNameToSensorId
              }
            })
          })
        }
      })
      // 获取品牌字典
      getBranchList().then(res => {
        if (res.data.result && res.data.errorCode === '0') {
          let allBranchDict = res.data.result
          this.branchList = allBranchDict
          allBranchDict.forEach((item) => {
            this.branchNameToBranchCode[item.value] = item.code
          })
        }
      })
      // 获取生态入口
      getEcologyEntrance().then(res => {
        if (res.data.result && res.data.errorCode === '0') {
          let allEcologyEntranceDict = res.data.result
          this.allEcologyEntranceList = allEcologyEntranceDict
          if (this.allEcologyEntranceList) {
            this.allEcologyEntranceList.forEach(value => {
              this.ecologyEntranceNameToId[value.name] = value.id
            })
          }
        }
      })
      // 获取语音功能
      getVoiceFunction().then(res => {
        if (res.data.result && res.data.errorCode === '0') {
          let allVoiceFunctionDict = res.data.result
          this.allVoiceFunctionList = allVoiceFunctionDict
          if (this.allVoiceFunctionList) {
            this.allVoiceFunctionList.forEach(value => {
              this.voiceFunctionNameToId[value.name] = value.id
            })
          }
        }
      })
    },
    // 下载批量导入模板，导入模板第一行是各个属性名称，第二行是每一个属性的描述
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
      categoryDescription = '不能为空，'
      this.allProductType.forEach((item) => {
        let productTypeName = item.value
        let allCategoryByTypeString = ''
        /*        categoryDescription = categoryDescription + productTypeName + '产品的可选项为：'
        let cateList = this.productTypeToCategory[item.code]
        cateList.forEach((cateItem) => {
          allCategoryByTypeString = allCategoryByTypeString + cateItem.value + '、'
        })
        if (allCategoryByTypeString.length > 0) {
          allCategoryByTypeString = allCategoryByTypeString.substring(0, allCategoryByTypeString.length - 1)
        } */
        if (categoryDescription === '不能为空，') {
          categoryDescription = categoryDescription + '产品品类的可选项为：'
          this.allProductType.forEach((itemProduct) => {
            allCategoryByTypeString = allCategoryByTypeString + itemProduct.value + '、'
          })
          if (allCategoryByTypeString.length > 0) {
            allCategoryByTypeString = allCategoryByTypeString.substring(0, allCategoryByTypeString.length - 1)
          }
          categoryDescription = categoryDescription + allCategoryByTypeString + ';'
        }

        functionDescription = functionDescription + productTypeName + '产品的可选项为：'
        let funcListByType = this.productTypeToFunctionList[item.code]
        let allFuncStringByType = ''
        funcListByType.forEach((funcItem) => {
          allFuncStringByType = allFuncStringByType + funcItem.functionName + '、'
        })
        if (allFuncStringByType.length > 0) {
          allFuncStringByType = allFuncStringByType.substring(0, allFuncStringByType.length - 1)
        }
        functionDescription = functionDescription + allFuncStringByType + ';' + '\r\n'

        scenarioDescription = scenarioDescription + productTypeName + '产品的可选项为：'
        let scenarioListByType = this.productTypeToScenarioList[item.code]
        let allScenarioListByTypeString = ''
        scenarioListByType.forEach((scenItem) => {
          allScenarioListByTypeString = allScenarioListByTypeString + scenItem.scenarioName + '、'
        })
        if (allScenarioListByTypeString.length > 0) {
          allScenarioListByTypeString = allScenarioListByTypeString.substring(0, allScenarioListByTypeString.length - 1)
        }
        scenarioDescription = scenarioDescription + allScenarioListByTypeString + ';' + '\r\n'

        sensorDescription = sensorDescription + productTypeName + '产品的可选项为：'
        let sensorListByType = this.productTypeToSensorList[item.code]
        let allSensorListByTypeString = ''
        sensorListByType.forEach((sensorItem) => {
          allSensorListByTypeString = allSensorListByTypeString + sensorItem.sensorName + '、'
        })
        if (allSensorListByTypeString.length > 0) {
          allSensorListByTypeString = allSensorListByTypeString.substring(0, allSensorListByTypeString.length - 1)
        }
        sensorDescription = sensorDescription + allSensorListByTypeString + ';' + '\r\n'
      })
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
    // 搜索产品
    searchData () {

      this.loadingProduct = true
      // 获取登录用户的token，根据token获取当前用户是否有权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，通过用户权限和跳转的页面的name来判断是否有权限访问;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        this.getProductByCondition()
      }).catch(e => {
        this.loadingProduct = false
      })
    },
    // 根据搜索框条件，重新加载数据
    getProductByCondition () {
      this.loadingProduct = true
      // 如果没选产品类型条件，则产品类型是有权限的所有类型
      if (!this.productDataForSearch.productTypeSelected || this.productDataForSearch.productTypeSelected.length < 1) {
        this.productDataForSearch.productType = []
        let typeTemp = []
        if (this.viewAccessAdmin) {
          this.allProductType.forEach((item) => {
            typeTemp.push(item.code)
          })
        } else {
          this.$store.state.user.access.forEach(value => {
            if (this.authToProductType[value]) {
              typeTemp.push(this.authToProductType[value])
            }
          })
        }
        this.productDataForSearch.productType = typeTemp
      } else {
        let typeTemp = []
        typeTemp.push(this.productDataForSearch.productTypeSelected)
        this.productDataForSearch.productType = typeTemp
      }
      if (!this.pageNumber) {
        this.pageNumber = 1
      }
      this.productDataForSearch.pageNumber = this.pageNumber
      if (!this.pageSize) {
        this.pageSize = 10
      }
      this.productDataForSearch.pageSize = this.pageSize

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
        //this.tableDataCount = this.tableData.length
      }).catch((reason) => {
        this.$Message.error('搜索产品失败：' + reason)
        this.loadingProduct = false
      }).finally(() => {
        this.loadingProduct = false
      })
    },
    searchProductTypeSelectChange () {
      this.productDataForSearch.functionName = ''
      this.productDataForSearch.function = ''
      this.productDataForSearch.scenarioName = ''
      this.productDataForSearch.scenario = ''
      this.productDataForSearch.sensorName = ''
      this.productDataForSearch.sensor = ''
    }
  },
  mounted () {
    // this.uploadList = this.$refs.upload.fileList
  },
  beforeMount () {

    this.loadingProduct = true
    this.queryDictionary()
    // 初始获取所有产品
    getProductType().then(res => {
      if (res.data.result && res.data.errorCode === '0') {
        // 产品类型只对应有权限的类型
        let authForProduct = []
        res.data.result.forEach((item) => {
          let authTemp = this.productTypeToAuth[item.code]
          if (hasOneOf(['super_admin', 'admin', authTemp], this.access)) {
            authForProduct.push(item.code)
          }
        })
        queryProduct({ 'productType': authForProduct }).then(res => {
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
        }).catch((reason) => {
          this.$Message.error('获取产品失败：' + reason)
          this.loadingProduct = false
        }).finally(() => {
          this.loadingProduct = false
        })
      }
    }).catch((reason) => {
      this.$Message.error('获取产品失败：' + reason)
      this.loadingProduct = false
    }).finally(() => {
    })
    this.setColumns()
  },
  computed: {
    access () {
      return this.$store.state.user.access
    },
    // 判断是否是admin用户，
    viewAccessAdmin () {
      return hasOneOf(['super_admin', 'admin'], this.access)
    },
    // 是否有电热产品类型的权限
    accessElectricHeater () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['electric_heater']], this.access)
    },
    // 是否有当前产品类型的权限
    accessGasHeaterStove () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['gas_heater_stove']], this.access)
    },
    // 是否有当前产品类型的权限
    accessWaterPurification () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['water_purification']], this.access)
    },
    // 是否有当前产品类型的权限
    accessWaterDrink () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['water_drink']], this.access)
    },
    // 是否有当前产品类型的权限
    accessRangHoodType () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['rang_hood_type']], this.access)
    },
    // 是否有当前产品类型的权限
    accessIntegratedGasCombinedKitchen () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['integrated_gas_combined_kitchen']], this.access)
    },
    // 是否有当前产品类型的权限
    accessDiswacherType () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['diswasher_type']], this.access)
    },
    // 是否有当前产品类型的权限
    accessDisinfectionCabinetType () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['disinfection_cabinet_type']], this.access)
    },
    // 是否有当前产品类型的权限
    accessGasStove () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['gas_stove']], this.access)
    },
    // 是否有当前产品类型的权限
    accessGasCombinedKitchen () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth['gas_combined_kitchen']], this.access)
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

.demo-drawer-footer {
  width: 100%;
  position: absolute;
  bottom: 0;
  left: 0;
  border-top: 1px solid #e8e8e8;
  padding: 10px 16px;
  text-align: right;
  background: #fff;
}
</style>
