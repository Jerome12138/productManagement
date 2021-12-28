<template>
  <div>
    <Button type="primary" size="default" @click="modal1=true">添加</Button>
    <Modal
      v-model="modal1"
      title="添加审核组"
      @on-ok="saveAuditGroup"
      @on-cancel="cancel"
      :loading="loading">
      <div>
        <i style="color:red">*</i>
        审核组名称：<input size="55" autofocus v-model="auditGroupData.groupName"
                     placeholder="请输入20个字符以内的审核组名称" maxlength="20"/>
      </div>
      <div style="margin-top: 20px">
        <i style="color:red">*</i>
        审核组成员：
        <div style="margin-top: 10px;margin-left: 35px">
          <Transfer
            :data="allUser"
            :target-keys="targetKeys"
            :render-format="render1"
            :list-style="listStyle"
            @on-change="handleChange1"
            :titles="['待选人员','已选人员']">
          </Transfer>
        </div>
      </div>
      <div slot="footer">
        <Button @click="cancel">取消</Button>
        <Button type="primary" @click="saveAuditGroup">确定</Button>
      </div>
    </Modal>
    <Card>
      <tables ref="tables" searchable border stripe search-place="" v-model="tableData" :columns="columns"/>
    </Card>
  </div>
</template>

<script>
import Tables from '_c/tables'
import { deleteAuditGroupById, getAllUser, saveAuditGroup, queryAuditGroupByUserId } from '@/api/data'
import { hasOneOf } from '@/libs/tools'

export default {
  name: 'tables_page',
  components: {
    Tables
  },
  data () {
    return {
      targetKeys: [],
      allUser: [],
      loading: true,
      addInput: '',
      modal1: false,
      auditGroupData: {
        id: '',
        createUserId: '',
        groupName: '',
        userIds: [],
        userNames: ''
      },
      listStyle: {
        height: '',
        minHeight: '',
        maxHeight: ''
      },
      columns: [],
      tableData: []
    }
  },
  methods: {
    render1 (item) {
      return item.label
    },
    handleChange1 (newTargetKeys, direction, moveKeys) {
      this.targetKeys = newTargetKeys
    },
    saveAuditGroup () {
      if (!this.auditGroupData.groupName.trim()) {
        this.$Message.error('审核组名称不能为空！')
        return
      }
      if (!this.targetKeys || this.targetKeys.length === 0) {
        this.$Message.error('审核组成员不能为空！')
        return
      }
      let createUserId = this.$store.state.user.userId
      this.auditGroupData.createUserId = createUserId
      this.auditGroupData.userIds = this.targetKeys
      saveAuditGroup(this.auditGroupData).then(res => {
        if (res.data.errorCode === '0') {
          this.$Message.success('保存成功！')
          this.clearAuditGroupData()
          this.queryAndBindAuditGroup()
          this.modal1 = false
        } else {
          this.$Message.error('保存失败：' + res.data.msg)
        }
      })
    },

    cancel () {
      this.modal1 = false
      this.clearAuditGroupData()
    },
    clearAuditGroupData () {
      this.targetKeys = []
      this.auditGroupData = {
        id: '',
        createUserId: '',
        groupName: '',
        userIds: [],
        userNames: ''
      }
    },
    queryAndBindAuditGroup () {
      let userId = this.$store.state.user.userId
      queryAuditGroupByUserId(userId).then(res => {
        if (res.data.result) {
          this.tableData = res.data.result
        }
      })
    },
    setColumns () {
      this.columns.push(
        {
          title: '审核组名称',
          align: 'left',
          maxWidth: 200,
          key: 'groupName'
        },
        {
          title: '小组成员',
          align: 'left',
          key: 'userNames'
        })

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
                this.auditGroupData.id = params.row.id
                this.auditGroupData.groupName = params.row.groupName
                this.targetKeys = params.row.userIds
                this.modal1 = true
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
                  title: '确定要删除吗？',
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
          operationButton.push(updateButton)
          operationButton.push(deleteButton)
          return h('div', operationButton)
        }
      })
    },
    // 删除审核小组
    remove (index, id) {
      deleteAuditGroupById(id).then(res => {
        if (res.data.errorCode === '0') {
          this.tableData.splice(index, 1)
          this.$Message.success('删除成功！')
        } else {
          this.$Message.error('删除失败:' + res.data.msg)
        }
      })
    },

    // 用户权限的穿梭框，根据页面高度跳转穿梭框的高度
    changeHeight () {
      let height1 = this.allUser.length * 30 + 44
      let height2 = window.innerHeight - 400
      this.listStyle.height = (height1 > height2 ? height2 : height1) + 'px'
      this.listStyle.minHeight = '210px'
    }
  },
  mounted () {
    // 初始获取所有用户
    getAllUser().then(res => {
      if (res.data.result) {
        res.data.result.forEach((item) => {
          if (item.userName === 'admin' || item.userName === 'super_admin') {
            /* this.allUser.push({ key: item.id, label: item.authName, disabled: true }) */
          } else {
            this.allUser.push({ key: item.id, label: item.userName })
          }
        })
      }
      // 初始穿梭框的高度
      this.changeHeight()
    })
    this.queryAndBindAuditGroup()
    //  用户权限的穿梭框，根据页面高度跳转穿梭框的高度
    window.addEventListener('resize', this.changeHeight)
  },
  beforeMount () {
    this.setColumns()
  },
  computed: {
    access () {
      return this.$store.state.user.access
    },
    //  是否有添加功能权限
    accessAdd () {
      return hasOneOf(['super_admin', 'admin', 'ecology_entrance_add'], this.access)
    },
    //  是否有更新功能权限
    accessUpdate () {
      return hasOneOf(['super_admin', 'admin', 'ecology_entrance_update'], this.access)
    },
    //  是否有删除功能权限
    accessDelete () {
      return hasOneOf(['super_admin', 'admin', 'ecology_entrance_delete'], this.access)
    },
    //  是否有当前页面的权限
    accessEcologyEntrance () {
      return hasOneOf(['super_admin', 'admin', 'ecology_entrance'], this.access)
    }
  }
}
</script>

<style>

</style>
