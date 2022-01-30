<template>
  <div>
    <Button v-if="accessAddTask" type="primary" size="default" @click="showAddTaskModal=true">新建任务</Button>
    <modalAddTask v-model="showAddTaskModal"></modalAddTask>
    <drawerTaskDetail v-model="taskDetailDrawer" :taskId="taskDetailId"></drawerTaskDetail>
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
  queryUnhandledTaskList,
  queryHandledTaskList,
} from '@/api/data'
import { hasOneOf } from '@/libs/tools'
import modalAddTask from './components/modalAddTask.vue'
import drawerTaskDetail from './components/drawerTaskDetail.vue'

export default {
  name: 'taskManage',
  components: {
    Tables,
    modalAddTask,
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
      taskDetailDrawer: false,
      showAddTaskModal: false,
      taskDetailId: 0,
    }
  },
  methods: {
    taskDetail (taskId) {
      this.taskDetailDrawer = true
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
  },
  mounted () {
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
