<template>
  <div>
    <Button v-if="accessAddTask" type="primary" size="default" @click="showAddTaskModal">新建任务</Button>
    <modalAddTask v-model="modal1" :propTaskData="taskData" @setAddProductModal="setAddProductModal($event)" ref="modalAddTask"></modalAddTask>
    <modalAddProduct v-model="showAddProductModal" :productType="addProductType" @saveProductSuccess="saveProductSuccess"></modalAddProduct>
    <drawerTaskDetail
      v-model="taskDetailDrawer"
      :taskId="taskDetailId"
    ></drawerTaskDetail>
    <Tabs style="margin-top: 10px" @on-click="getTaskList">
      <TabPane :label="unHandleTabContent" name="unHandleList">
        <Card>
          <List v-if="unhandledTaskList.length>0">
            <ListItem v-for="item in unhandledTaskList" :key=item.id :value="item.id">
              <span style="white-space: nowrap;text-overflow:ellipsis;overflow:hidden;" :title=item.title
                    @click="taskDetail(item.id)">{{ item.title }}</span>
            </ListItem>
          </List>
          <span v-else> 暂无数据 </span>
        </Card>
      </TabPane>
      <TabPane label="已处理" name="handledList">
        <Card>
          <List v-if="handledTaskList.length>0">
            <ListItem v-for="item in handledTaskList" :key=item.id :value="item.id">
              <span style="white-space: nowrap;text-overflow:ellipsis;overflow:hidden;" :title=item.title
                    @click="taskDetail(item.id)">{{ item.title }}</span>
            </ListItem>
          </List>
          <span v-else>暂无数据</span>
        </Card>
      </TabPane>
    </Tabs>

  </div>
</template>

<script>
import Tables from '_c/tables'
import {
  getAllUserIdAndName,
  getEcologyEntrance,
  queryAuditGroupByUserId,
  queryUnhandledTaskList,
  queryHandledTaskList,
  getProductType,
  getFunctionByType,
  getScenarioByType,
  getSensorByType,
  getVoiceFunction,
  getProductModel
} from '@/api/data'
import store from '@/store'
import { getToken, setToken } from '@/libs/util'
import { hasOneOf } from '@/libs/tools'
import modalAddTask from './components/modalAddTask.vue'
import modalAddProduct from './components/modalAddProduct.vue'
import drawerTaskDetail from './components/drawerTaskDetail.vue'

export default {
  name: 'taskManage',
  components: {
    Tables,
    modalAddTask,
    modalAddProduct,
    drawerTaskDetail,
  },
  data () {
    return {
      unHandleCount: 0,
      unHandleTabContent: (h) => {
        return h('div', [
          h('span', '未处理'),
          h('Badge', {
            props: {
              count: this.unHandleCount
            },
            style: {
              marginLeft: '5px'
            }
          })
        ])
      },
      unhandledTaskList: [],
      handledTaskList: [],
      allUser: [],
      groupIdToUserName: {},
      groupIdToUserIds: {},
      auditGroupList: [],
      taskData: {
        title: 'XXXX新品开发任务',
        content: '',
        actorUserId: '',
        auditGroupId: '',
        auditGroupUserIds: '',
        productType: '',
        productIds: [],
        // productFunctionType: [],
        // productScenarioType: [],
        // productSensorType: [],
        // productVoiceFunctionType: [],
        // productEcologyEntranceType: [],
        productModel: ''
      },
      taskDetailDrawer: false,
      loading: false,
      modal1: false,
      columns: [{
        title: '处理人',
        align: 'left',
        maxWidth: 100,
        key: 'userName'
      }, {
        title: '任务角色',
        align: 'left',
        maxWidth: 85,
        key: 'roleName'
      }, {
        title: '操作',
        align: 'left',
        maxWidth: 121,
        key: 'operationName'
      }, {
        title: '意见',
        align: 'left',
        key: 'opinion'
      }, {
        title: '时间',
        align: 'left',
        maxWidth: 150,
        key: 'processTime'
      }],
      tableData: [],
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
      taskHandleRules: [],
      spinShow: true,
      productTypeToFunctionList: {},
      productTypeToScenarioList: {},
      productTypeToSensorList: {},
      allProductType: [],
      allVoiceFunctionList: [],
      allEcologyEntranceList: [],
      allProductModel: {},
      showAddProductModal: false,
      addProductType: '',
      taskDetailId: 0,
    }
  },
  methods: {
    content () {
      if (this.taskDetailData.status === 'audit_fail_confirming' && this.isSponsor) {
        return {
          required: true,
          message: '内容不能为空',
          trigger: 'blur'
        }
      } else {
        return {}
      }
    },
    changeProductType () {
      this.taskData.productFunctionType = []
      this.taskData.productScenarioType = []
      this.taskData.productSensorType = []
      this.taskData.productModel = ''
    },
    showAddTaskModal () {
      this.modal1 = true
      let functionLength = 0
      let scenarioLength = 0
      let sensorLength = 0
      let getFunctionFinish = false
      let getScenarioFinish = false
      let getSensorFinish = false
      let getVoiceFunctionFinish = false
      let getEcologyEntranceFinish = false
      let getModelFinish = false
      // 获取所有产品类型
      getProductType().then(res => {
        if (res.data.errorCode === '0' && res.data.result) {
          this.allProductType = res.data.result
          res.data.result.forEach((item) => {
            // 获取对应产品类型的功能
            getFunctionByType(item.code).then(result => {
              if (result.data.result && result.data.errorCode === '0') {
                this.productTypeToFunctionList[item.code] = result.data.result
              }
              functionLength++
              if (functionLength === this.allProductType.length) {
                getFunctionFinish = true
                if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
                  this.spinShow = false
                }
              }
            })
            // 获取对应产品类型的场景
            getScenarioByType(item.code).then(result => {
              if (result.data.result) {
                this.productTypeToScenarioList[item.code] = result.data.result
              }
              scenarioLength++
              if (scenarioLength === this.allProductType.length) {
                getScenarioFinish = true
                if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
                  this.spinShow = false
                }
              }
            })
            // 获取对应的传感器
            getSensorByType(item.code).then(result => {
              if (result.data.result) {
                this.productTypeToSensorList[item.code] = result.data.result
              }
              sensorLength++
              if (sensorLength === this.allProductType.length) {
                getSensorFinish = true
                if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
                  this.spinShow = false
                }
              }
            })
          })
        } else {
          getFunctionFinish = true
          getScenarioFinish = true
          getSensorFinish = true
          if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
            this.spinShow = false
          }
        }
      })

      // 获取生态入口
      getEcologyEntrance().then(res => {
        if (res.data.result && res.data.errorCode === '0') {
          this.allEcologyEntranceList = res.data.result
        }
        getEcologyEntranceFinish = true
        if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
          this.spinShow = false
        }
      })
      // 获取语音功能
      getVoiceFunction().then(res => {
        if (res.data.result && res.data.errorCode === '0') {
          this.allVoiceFunctionList = res.data.result
        }
        getVoiceFunctionFinish = true
        if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
          this.spinShow = false
        }
      })
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
        }
        getModelFinish = true
        if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
          this.spinShow = false
        }
      })
    },
    taskDetail (taskId) {
      this.taskDetailDrawer = true
      this.spinDrawerShow = true
      this.taskDetailId = taskId
    },
    getUnhandledTaskList () {
      let userId = this.$store.state.user.userId
      queryUnhandledTaskList(userId).then(res => {
        if (res.data.errorCode === '0' && res.data.result) {
          this.unhandledTaskList = res.data.result
          this.unHandleCount = this.unhandledTaskList.length
        }
      })
    },
    getHandledTaskList () {
      let userId = this.$store.state.user.userId
      queryHandledTaskList(userId).then(res => {
        if (res.data.errorCode === '0' && res.data.result) {
          this.handledTaskList = res.data.result
        }
      })
    },
    getTaskList (name) {
      if (name === 'unHandleList') {
        this.getUnhandledTaskList()
      } else if (name === 'handledList') {
        this.getHandledTaskList()
      }
    },
    setAddProductModal (productType) {
      this.showAddProductModal=true
      this.addProductType=productType
    },
    saveProductSuccess () {
      this.$refs.modalAddTask.initProductModel()
    },
  },
  mounted () {
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
    this.getUnhandledTaskList()
  },
  beforeMount () {
  },
  computed: {
    access () {
      return this.$store.state.user.access
    },
    //  是否有添加功能权限
    accessAddTask () {
      return hasOneOf(['super_admin', 'admin', 'task_add'], this.access)
    }
  }
}
</script>

<style>
</style>
