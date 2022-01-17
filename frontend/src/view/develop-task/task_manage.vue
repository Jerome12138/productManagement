<template>
  <div>
    <Button v-if="accessAddTask" type="primary" size="default" @click="showAddTaskModal">新建任务</Button>
    <modalAddTask v-model="modal1" :propTaskData="taskData" @setAddProductModal="setAddProductModal($event)" ref="modalAddTask"></modalAddTask>
    <modalAddProduct v-model="showAddProductModal" :productType="addProductType" @saveProductSuccess="saveProductSuccess"></modalAddProduct>
    <Drawer
      title="任务详情"
      v-model="taskDetailDrawer"
      width="720"
      :mask-closable="false"
      :styles="styles"
      :loading="handleTaskLoading"
      @on-close="closeTaskDetail">
      <!-- <Spin size="large" fix v-if="spinDrawerShow"></Spin> -->
      <Form ref="taskEditManage" :model="taskDetailData" :rules="taskRuleValidate">
        <Row :gutter="10">
          <Col span="3">
            <FormItem label="任务标题：">
            </FormItem>
          </Col>
          <Col span="21">
            <FormItem>
              <span>{{ taskDetailData.title }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="10" v-if="taskDetailData.status==='audit_fail_confirming' && isSponsor">
          <Col span="24">
            <FormItem v-if="taskDetailData.status==='audit_fail_confirming' && isSponsor" label="任务内容：" prop="content">
              <Input v-model="taskDetailData.content" type="textarea" :maxlength="500" placeholder="请输入500个字符以内的任务内容"
                     autosize></Input>
            </FormItem>
            <FormItem v-else label="" :rules="{}">
              <span>任务内容：</span><span style="white-space: pre">{{ taskDetailData.content }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row v-else>
          <Col span="3">
            <FormItem label="任务内容：">
            </FormItem>
          </Col>
          <Col span="21">
            <FormItem>
              <span style="white-space: pre">{{ taskDetailData.content }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="10">
          <Col span="12">
            <div v-if="taskDetailData.status==='audit_fail_confirming' && isSponsor">
              <FormItem label="产品类型:"
                        prop="productType">
                <Select v-model="taskDetailData.productType" placeholder="请选择产品类型" clearable
                        not-found-text="暂无产品类型"
                        @on-change="changeTaskDetailProductType">
                  <Option v-for="item in allProductType" :value="item.code" :key="item.code">{{ item.value }}</Option>
                </Select>
              </FormItem>
            </div>
            <FormItem v-else label="产品类型:" :rules="{}">
              <span>{{ taskDetailData.productTypeName }}</span>
            </FormItem>
          </Col>
          <Col span="10">
            <div v-if="taskDetailData.status==='audit_fail_confirming' && isSponsor">
              <FormItem label="产品型号:" prop="productModel">
                <Select v-model="taskDetailData.productModel" placeholder="请选择产品型号" clearable
                        not-found-text="请先选择产品类型，并确认已选类型有产品">
                  <Option v-for="item in allProductModel[taskDetailData.productType]"
                          :value="item.model" :key="item.model">{{ item.model }}
                  </Option>
                </Select>
              </FormItem>
            </div>
            <FormItem v-else label="产品型号:" :rules="{}">
              <span>{{ taskDetailData.productModel }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="10">
          <Col span="12">
            <FormItem label="产品功能:">
              <Select v-if="taskDetailData.status==='audit_fail_confirming' && isSponsor"
                      v-model="taskDetailData.productFunctionType" placeholder="请选择产品功能" clearable multiple
                      not-found-text="请先选择产品类型，并确认已选类型有功能选项">
                <Option v-for="item in productTypeToFunctionList[taskDetailData.productType]" :value="item.id"
                        :key="item.id">
                  {{ item.functionName }}
                </Option>
              </Select>
              <span v-else>{{ taskDetailData.productFunctionTypeNames }}</span>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="产品场景:">
              <Select v-if="taskDetailData.status==='audit_fail_confirming' && isSponsor"
                      v-model="taskDetailData.productScenarioType" placeholder="请选择产品场景" clearable multiple
                      not-found-text="请先选择产品类型，并确认已选类型有场景选项">
                <Option v-for="item in productTypeToScenarioList[taskDetailData.productType]"
                        :value="item.id" :key="item.id">{{ item.scenarioName }}
                </Option>
              </Select>
              <span v-else>{{ taskDetailData.productScenarioTypeNames }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="10">
          <Col span="12">
            <FormItem label="传感器:">
              <Select v-if="taskDetailData.status==='audit_fail_confirming' && isSponsor"
                      v-model="taskDetailData.productSensorType" placeholder="请选择产品传感器" clearable multiple
                      not-found-text="请先选择产品类型，并确认已选类型有传感器选项">
                <Option v-for="item in productTypeToSensorList[taskDetailData.productType]" :value="item.id"
                        :key="item.id">
                  {{ item.sensorName }}
                </Option>
              </Select>
              <span v-else>{{ taskDetailData.productSensorTypeNames }}</span>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="语音功能:">
              <Select v-if="taskDetailData.status==='audit_fail_confirming' && isSponsor"
                      v-model="taskDetailData.productVoiceFunctionType" placeholder="请选择产品语音功能" clearable multiple
                      not-found-text="暂无可选项，请确认是否有语音功能选项">
                <Option v-for="item in allVoiceFunctionList" :value="item.id" :key="item.id">{{ item.name }}</Option>
              </Select>
              <span v-else>{{ taskDetailData.productVoiceFunctionTypeNames }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="10">
          <Col span="12">
            <FormItem label="生态入口:">
              <Select v-if="taskDetailData.status==='audit_fail_confirming' && isSponsor"
                      v-model="taskDetailData.productEcologyEntranceType" placeholder="请选择产品生态入口" clearable multiple
                      not-found-text="暂无可选项，请确认是否有生态入口选项">
                <Option v-for="item in allEcologyEntranceList" :value="item.id" :key="item.id">{{ item.name }}</Option>
              </Select>
              <span v-else>{{ taskDetailData.productEcologyEntranceTypeNames }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="10">
          <Col span="8">
            <FormItem label="发起人：">
              <span>{{ taskDetailData.sponsorName }}</span>
            </FormItem>
          </Col>
          <Col span="8">
            <FormItem label="发起时间：">
              <span>{{ taskDetailData.sponsorTime }}</span>
            </FormItem>
          </Col>
          <Col span="8">
            <FormItem label="当前状态：">
              <span>{{ taskDetailData.statusName }}</span>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="10">
          <Col span="24">
            <FormItem label="当前处理人：">
              <span>{{ taskDetailData.currentHandlerNames }}</span>
            </FormItem>
          </Col>
        </Row>
        <div v-if="haveProcess">
          <Row :gutter="10">
            <Col span="24">
              <FormItem label="任务流程：">
                <br/>
                <tables ref="tables" searchable border stripe search-place="" v-model="taskDetailData.taskProcess"
                        :columns="columns"/>
              </FormItem>
            </Col>
          </Row>
        </div>
        <div v-if="(isCurrentHandler || isSponsor) && !taskDetailData.isTaskEnd">
          <Row :gutter="10">
            <Col span="24">
              <FormItem label="处理：" prop="handleDetail">
                <RadioGroup
                  v-if="(taskDetailData.currentRole==='auditor' || isSponsor) && taskDetailData.status==='auditing'"
                  v-model="taskDetailData.handleDetail">
                  <Radio v-if="isCurrentHandler" label="audit_pass">
                    <span>通过</span>
                  </Radio>
                  <Radio v-if="isCurrentHandler" label="audit_not_pass">
                    <span>不通过</span>
                  </Radio>
                  <Radio v-if="isSponsor" label="sponsor_end">
                    <span>结束</span>
                  </Radio>
                </RadioGroup>
                <RadioGroup
                  v-if="taskDetailData.currentRole==='sponsor' && taskDetailData.status==='audit_fail_confirming'"
                  v-model="taskDetailData.handleDetail">
                  <Radio label="sponsor_send_audit">
                    <span>发送审核</span>
                  </Radio>
                  <Radio label="sponsor_end">
                    <span>结束</span>
                  </Radio>
                </RadioGroup>
                <RadioGroup
                  v-if="taskDetailData.currentRole==='sponsor' && taskDetailData.status==='accept_reject_confirming'"
                  v-model="taskDetailData.handleDetail">
                  <Radio label="sponsor_reject_not_accept">
                    <span>驳回</span>
                  </Radio>
                  <Radio v-if="isSponsor" label="sponsor_end">
                    <span>结束</span>
                  </Radio>
                </RadioGroup>
                <RadioGroup v-if="taskDetailData.currentRole==='sponsor' && taskDetailData.status==='finish_confirming'"
                            v-model="taskDetailData.handleDetail">
                  <Radio label="sponsor_reject_finish">
                    <span>驳回</span>
                  </Radio>
                  <Radio v-if="isSponsor" label="sponsor_end">
                    <span>结束</span>
                  </Radio>
                </RadioGroup>
                <RadioGroup
                  v-if="taskDetailData.currentRole==='sponsor' && taskDetailData.status==='not_finish_confirming'"
                  v-model="taskDetailData.handleDetail">
                  <Radio label="sponsor_reject_not_finish">
                    <span>驳回</span>
                  </Radio>
                  <Radio v-if="isSponsor" label="sponsor_end">
                    <span>结束</span>
                  </Radio>
                </RadioGroup>
                <RadioGroup v-if="taskDetailData.currentRole==='actor' && taskDetailData.status==='accepting'"
                            v-model="taskDetailData.handleDetail">
                  <Radio v-if="isCurrentHandler" label="actor_accept">
                    <span>接受</span>
                  </Radio>
                  <Radio v-if="isCurrentHandler" label="actor_not_accept">
                    <span>拒绝</span>
                  </Radio>
                  <Radio v-if="isSponsor" label="sponsor_end">
                    <span>结束</span>
                  </Radio>
                </RadioGroup>
                <RadioGroup v-if="taskDetailData.currentRole==='actor' && taskDetailData.status==='finishing'"
                            v-model="taskDetailData.handleDetail">
                  <Radio v-if="isCurrentHandler" label="actor_finish">
                    <span>完成</span>
                  </Radio>
                  <Radio v-if="isCurrentHandler" label="actor_not_finish">
                    <span>未完成</span>
                  </Radio>
                  <Radio v-if="isSponsor" label="sponsor_end">
                    <span>结束</span>
                  </Radio>
                </RadioGroup>
              </FormItem>
            </Col>
          </Row>
          <Row :gutter="10">
            <Col span="24">
              <FormItem label="意见：" prop="handleOpinion">
                <Input type="textarea" v-model="taskDetailData.handleOpinion" :autosize="opinionSize"
                       placeholder="请输入500个字符以内的内容。" :maxlength="500" style="width: 613px"></Input>
              </FormItem>
            </Col>
          </Row>
          <div class="demo-drawer-footer">
            <Button style="margin-right: 8px" @click="closeTaskDetail">取消</Button>
            <Button type="primary" @click="handleTask">确认</Button>
          </div>
        </div>
      </Form>
    </Drawer>
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
  saveEcologyEntrance,
  saveTask,
  queryUnhandledTaskList,
  queryHandledTaskList,
  getTaskDetailById,
  handleTaskProcess,
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

export default {
  name: 'taskManage',
  components: {
    Tables,
    modalAddTask,
    modalAddProduct
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
      handleTaskLoading: false,
      opinionSize: {
        minRows: 2,
        maxRows: 6
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
      taskDetailData: {
        id: '',
        title: '',
        content: '',
        sponsorName: '',
        sponsorTime: '',
        sponsorId: '',
        currentHandlerIds: [],
        taskProcess: [],
        status: '',
        currentRole: '',
        handleOpinion: '',
        handleDetail: '',
        isTaskEnd: false,
        statusName: '',
        currentHandlerNames: '',
        productType: '',
        productFunctionType: [],
        productScenarioType: [],
        productSensorType: [],
        productVoiceFunctionType: [],
        productEcologyEntranceType: [],
        productTypeName: '',
        productFunctionTypeNames: '',
        productScenarioTypeNames: '',
        productSensorTypeNames: '',
        productVoiceFunctionTypeNames: '',
        productEcologyEntranceTypeNames: '',
        productModel: ''
      },
      taskDetailDrawer: false,
      styles: {
        height: 'calc(100% - 55px)',
        overflow: 'auto',
        paddingBottom: '53px',
        position: 'static'
      },
      modalStyles: {
        width: '820px'
      },
      loading: false,
      modal1: false,
      haveProcess: false,
      isCurrentHandler: false,
      isSponsor: false,
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
      spinDrawerShow: true,
      productTypeToFunctionList: {},
      productTypeToScenarioList: {},
      productTypeToSensorList: {},
      allProductType: [],
      allVoiceFunctionList: [],
      allEcologyEntranceList: [],
      allProductModel: {},
      showAddProductModal: false,
      addProductType: '',
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
    changeTaskDetailProductType () {
      this.taskDetailData.productFunctionType = []
      this.taskDetailData.productScenarioType = []
      this.taskDetailData.productSensorType = []
      this.taskDetailData.productModel = ''
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
    sleep (n) {
      let start = new Date().getTime()
      while (true) {
        if (new Date().getTime() - start > n) {
          break
        }
      }
    },
    handleTask () {
      this.$refs.taskEditManage.validate((valid) => {
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
            this.$store.state.user.userId = user.user_id
            if (user.user_id.toString() === this.taskDetailData.sponsorId.toString()) {
              this.isSponsor = true
            } else {
              this.isSponsor = false
            }
            if (hasOneOf([user.user_id], this.taskDetailData.currentHandlerIds)) {
              this.isCurrentHandler = true
            } else {
              this.isCurrentHandler = false
            }
            if (this.isSponsor || this.isCurrentHandler) {
              this.handleTaskLoading = true
              let taskOperation = {}
              taskOperation.taskId = this.taskDetailData.id
              taskOperation.userId = this.$store.state.user.userId
              taskOperation.operation = this.taskDetailData.handleDetail
              taskOperation.operationOpinion = this.taskDetailData.handleOpinion
              taskOperation.role = this.taskDetailData.currentRole
              if (this.isSponsor && this.taskDetailData.status === 'audit_fail_confirming' && taskOperation.operation === 'sponsor_send_audit') {
                let taskToUpdate = {}
                taskToUpdate.id = this.taskDetailData.id
                taskToUpdate.content = this.taskDetailData.content
                taskToUpdate.productModel = this.taskDetailData.productModel
                taskToUpdate.productFunctionType = this.taskDetailData.productFunctionType
                taskToUpdate.productScenarioType = this.taskDetailData.productScenarioType
                taskToUpdate.productSensorType = this.taskDetailData.productSensorType
                taskToUpdate.productVoiceFunctionType = this.taskDetailData.productVoiceFunctionType
                taskToUpdate.productEcologyEntranceType = this.taskDetailData.productEcologyEntranceType
                try {
                  saveTask(taskToUpdate).then(res => {
                    if (res.data.errorCode !== '0') {
                      this.$Message.error('保存失败:' + res.data.msg)
                      this.handleTaskLoading = false
                    } else {
                      handleTaskProcess(taskOperation).then(res => {
                        this.handleTaskLoading = false
                        if (res.data.errorCode === '0') {
                          this.$Message.success('处理成功')
                          this.taskDetailDrawer = false
                          this.getHandledTaskList()
                          this.getUnhandledTaskList()
                          this.clearTaskDetailData()
                        } else {
                          this.$Message.error('处理失败：' + res.data.msg)
                        }
                      })
                    }
                  })
                } catch (e) {
                  this.handleTaskLoading = false
                  this.$Message.error('保存失败:' + e)
                }
              } else {
                handleTaskProcess(taskOperation).then(res => {
                  this.handleTaskLoading = false
                  if (res.data.errorCode === '0') {
                    this.$Message.success('处理成功')
                    this.taskDetailDrawer = false
                    this.getHandledTaskList()
                    this.getUnhandledTaskList()
                    this.clearTaskDetailData()
                  } else {
                    this.$Message.error('处理失败：' + res.data.msg)
                  }
                })
              }
            } else {
              this.$Message.warning('当前用户不是该任务目前的处理人和发起人，无法处理任务！')
            }
          })
        }
      })
    },
    clearTaskDetailData () {
      this.taskDetailData.handleOpinion = ''
      this.taskDetailData.handleDetail = ''
    },
    closeTaskDetail () {
      this.clearTaskDetailData()
      this.taskDetailDrawer = false
    },
    taskDetail (taskId) {
      this.taskDetailDrawer = true
      this.spinDrawerShow = true
      getTaskDetailById(taskId).then(res => {
        if (res.data.errorCode === '0' && res.data.result) {
          this.taskDetailData.isTaskEnd = res.data.result.taskEnd
          this.taskDetailData.id = res.data.result.id
          this.taskDetailData.currentHandlerIds = res.data.result.currentHandlerIds
          this.taskDetailData.sponsorId = res.data.result.sponsorId
          this.taskDetailData.content = res.data.result.content
          this.taskDetailData.title = res.data.result.title
          this.taskDetailData.sponsorName = res.data.result.sponsorName
          this.taskDetailData.sponsorTime = res.data.result.sponsorTime
          this.taskDetailData.status = res.data.result.status
          this.taskDetailData.currentRole = res.data.result.currentRole
          this.taskDetailData.taskProcess = res.data.result.taskProcess
          this.taskDetailData.statusName = res.data.result.statusName
          this.taskDetailData.currentHandlerNames = res.data.result.currentHandlerNames

          this.taskDetailData.productType = res.data.result.productType
          this.taskDetailData.productModel = res.data.result.productModel
          this.taskDetailData.productFunctionType = res.data.result.productFunctionType
          this.taskDetailData.productScenarioType = res.data.result.productScenarioType
          this.taskDetailData.productSensorType = res.data.result.productSensorType
          this.taskDetailData.productVoiceFunctionType = res.data.result.productVoiceFunctionType
          this.taskDetailData.productEcologyEntranceType = res.data.result.productEcologyEntranceType
          this.taskDetailData.productTypeName = res.data.result.productTypeName
          this.taskDetailData.productFunctionTypeNames = res.data.result.productFunctionTypeNames
          this.taskDetailData.productScenarioTypeNames = res.data.result.productScenarioTypeNames
          this.taskDetailData.productSensorTypeNames = res.data.result.productSensorTypeNames
          this.taskDetailData.productVoiceFunctionTypeNames = res.data.result.productVoiceFunctionTypeNames
          this.taskDetailData.productEcologyEntranceTypeNames = res.data.result.productEcologyEntranceTypeNames

          if (this.taskDetailData.taskProcess.length > 0) {
            this.haveProcess = true
          } else {
            this.haveProcess = false
          }
          let userId = this.$store.state.user.userId
          if (hasOneOf([userId], this.taskDetailData.currentHandlerIds)) {
            this.isCurrentHandler = true
          } else {
            this.isCurrentHandler = false
          }
          if (userId.toString() === this.taskDetailData.sponsorId.toString()) {
            this.isSponsor = true
          } else {
            this.isSponsor = false
          }
          if (this.isSponsor && this.taskDetailData.status === 'audit_fail_confirming') {
            let functionLength = 0
            let scenarioLength = 0
            let sensorLength = 0
            let getFunctionFinish = false
            let getScenarioFinish = false
            let getSensorFinish = false
            let getVoiceFunctionFinish = false
            let getEcologyEntranceFinish = false
            let getModelFinish = false
            if (!this.allProductType || this.allProductType.length <= 0) {
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
                          this.spinDrawerShow = false
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
                          this.spinDrawerShow = false
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
                          this.spinDrawerShow = false
                        }
                      }
                    })
                  })
                } else {
                  getFunctionFinish = true
                  getScenarioFinish = true
                  getSensorFinish = true
                  if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
                    this.spinDrawerShow = false
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
                  this.spinDrawerShow = false
                }
              })
              // 获取语音功能
              getVoiceFunction().then(res => {
                if (res.data.result && res.data.errorCode === '0') {
                  this.allVoiceFunctionList = res.data.result
                }
                getVoiceFunctionFinish = true
                if (getFunctionFinish && getScenarioFinish && getSensorFinish && getVoiceFunctionFinish && getEcologyEntranceFinish && getModelFinish) {
                  this.spinDrawerShow = false
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
                  this.spinDrawerShow = false
                }
              })
            } else {
              this.spinDrawerShow = false
            }
          } else {
            this.spinDrawerShow = false
          }
        } else {
          this.spinDrawerShow = false
        }
      })
    },
    // 添加新功能，
    ok () {
      // 获取用户权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      // 根据token获取用户的权限
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，获取用户权限access， 存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.accessaccess = user.access
        // 判断是否是有 当前页面权限 和 添加功能权限
        if (this.accessAdd && this.accessEcologyEntrance) {
          this.loading = true
          // 校验功能名称
          if (!this.addInput || this.addInput.trim() === '') {
            this.loading = false
            this.modal1 = true
            this.$Message.error({
              content: '生态入口名称不能够为空！',
              duration: 5
            })
            return
          }
          if (!this.addInput.trim().length > 20) {
            this.loading = false
            this.modal1 = true
            this.$Message.error({
              content: '生态入口名称长度不能超过20！',
              duration: 5
            })
            return
          }

          if (this.addInput.indexOf('、') > -1) {
            this.loading = false
            this.modal1 = true
            this.$Message.error({
              content: '生态入口名称不能包含、符号！',
              duration: 5
            })
            return
          }

          saveEcologyEntrance({ name: this.addInput }).then(res => {
            if (res.data.errorCode === '0') {
              this.loading = false
              this.modal1 = false
              this.addInput = ''
              this.$Message.success('生态入口添加成功！')
              getEcologyEntrance().then(res => {
                this.tableData = res.data.result
              })
            } else {
              this.loading = true
              setTimeout(() => {
                this.loading = false
                this.modal1 = true
                this.$Message.error('生态入口添加失败：' + res.data.msg)
              }, 500)
            }
          })
        } else {
          this.loading = false
          this.modal1 = true
          if (!this.accessEcologyEntrance) {
            this.$Message.error('当前用户没有生态入口的权限！')
          } else {
            this.$Message.error('当前用户没有添加生态入口的权限！')
          }
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('添加生态入口失败！')
      })
    },
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
    cancel () {
      this.clearTaskData()
      this.modal1 = false
    },
    clearTaskData () {
      this.taskData.title = ''
      this.taskData.content = ''
      this.taskData.auditGroupId = ''
      this.taskData.actorUserId = ''
      this.taskData.createUserId = ''
      // this.taskData.productEcologyEntranceType = []
      // this.taskData.productFunctionType = []
      // this.taskData.productScenarioType = []
      // this.taskData.productSensorType = []
      this.taskData.productType = []
      // this.taskData.productVoiceFunctionType = []
      this.taskData.productModel = ''
      this.loading = false
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
