<template>
  <div>
      <span v-if="accessAdd">
        <Button type="primary" @click="showAddDrawer">添加</Button>
      </span>
    <Drawer
      :title="drawerTitle"
      v-model="drawer"
      width="720"
      :mask-closable="false"
      :styles="styles"
      @on-close="closeDrawer">
      <Form ref="userInfoForm" :model="userData">
        <Row :gutter="32">
          <Col span="24">
            <FormItem label="用户名" label-position="top" prop="userName"
                      :rules="{type: 'string', pattern: /^\w+$/,required: true,message: '用户名不能为空,只能由数字、字母、下划线组成', trigger: 'blur'}">
              <div style="text-align: right" v-if="disableUsername">
                <input style="width:600px; margin-right: 20px" disabled v-model="userData.userName"
                       placeholder="请输入20个字符以内的用户名,只能由数字、字母、下划线组成"></input>
              </div>
              <div style="text-align: right" v-else>
                <input style="width:600px; margin-right: 20px" v-model="userData.userName" maxlength="20"
                       placeholder="请输入20个字符以内的用户名，,只能由数字、字母、下划线组成" show-word-limit></input>
              </div>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="24">
            <FormItem label="密码" label-position="top" prop="password"
                      :rules="{required: true,message: '密码不能为空', trigger: 'blur'}">
              <div style="text-align: right">
                <input style="width:600px; margin-right: 20px" type="password" password v-model="userData.password"
                       placeholder="请输入密码,长度在20个字符以内" maxlength="20"
                       show-word-limit></input>
              </div>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="32">
          <Col span="24">
            <FormItem label="用户权限" label-position="top">
              <div style="margin-left: 70px">
                <Transfer
                  :data="allAuth"
                  :target-keys="targetKeys"
                  :render-format="render1"
                  :list-style="listStyle"
                  @on-change="handleChange1">
                </Transfer>
              </div>
            </FormItem>
          </Col>
        </Row>
      </Form>
      <div class="demo-drawer-footer">
        <div style="text-align: right; margin-right: 50px">
          <Button style="margin-right: 8px" @click="cancelSaveUser">取消</Button>
          <Button type="primary" @click="saveUser">保存</Button>
        </div>
      </div>
    </Drawer>

    <Card>
      <span>共查询到 {{ tableDataCount }} 条数据</span>
      <tables ref="tables" border stripe v-model="tableData" :columns="columns"/>
    </Card>
  </div>
</template>

<script>
import Tables from '_c/tables'
import {
  getAllUser,
  getAllAuth,
  saveUser,
  deleteUserById
} from '@/api/data'
import { hasOneOf } from '@/libs/tools'
import store from '@/store'
import { getToken, setToken } from '@/libs/util'

export default {
  name: 'tables_page',
  components: {
    Tables
  },
  data () {
    return {
      disableUsername: true,
      targetKeys: [],
      allAuth: [],
      userData: {},
      tableDataCount: 0,
      styles: {
        height: 'calc(100% - 55px)',
        overflow: 'auto',
        position: 'static'
      },
      listStyle: {
        height: '',
        minHeight: '210px',
        maxHeight: '1383px',
        width: '260px'
      },
      drawer: false,
      drawerTitle: '添加用户',
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
    setColumns () {
      this.columns.push({
        title: '用户名',
        key: 'userName',
        width: 200
      }, {
        title: '权限',
        key: 'authString'
      })
      // 如果有admin权限，显示一列，包括编辑按钮和删除按钮
      if (this.accessUpdate || this.accessDelete) {
        this.columns.push({
          title: '操作',
          key: 'action',
          width: 120,
          align: 'center',
          render: (h, params) => {
            // admin 和 super_admin  用户暂时不允许修改
            if (params.row.userName === 'admin' || params.row.userName === 'super_admin') {
              return h('div', [])
            }
            // 根据权限，显示 修改 和 删除 按钮
            let updateButton = h('Button', {
              props: {
                type: 'primary',
                size: 'small'
              },
              on: {
                // 编辑按钮点击事件
                click: () => {
                  // 用户数据，根据当前选择用户获取
                  this.userData = params.row
                  this.targetKeys = this.userData.authIds
                  this.drawerTitle = '修改用户'
                  this.showAddDrawer()
                }
              }
            }, '修改')
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
                    title: '确定要删除该用户吗？',
                    onOk: () => {
                      this.remove(params.index, params.row.id)
                    },
                    onCancel: () => {
                    }
                  })
                }
              }
            }, '删除')
            let buttonsOperation = []
            if (this.accessUpdate) {
              buttonsOperation.push(updateButton)
            }
            if (this.accessDelete) {
              buttonsOperation.push(deleteButton)
            }
            return h('div', buttonsOperation)
          }
        })
      }
    },
    // 删除用户
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
        // 拉取用户信息，获取用户权限access， 存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 判断是否有 用户管理 权限和 删除用户 权限
        if (this.accessUserManage && this.accessDelete) {
          deleteUserById(id).then(res => {
            if (res.data.errorCode && res.data.errorCode === '0') {
              this.tableData.splice(index, 1)
              this.tableDataCount = this.tableData.length
              this.$Message.success('删除用户成功！')
            } else {
              this.$Message.error('删除用户失败！')
            }
          })
        } else {
          if (!this.accessUserManage) {
            this.$Message.error('当前用户没有用户管理权限！')
          } else {
            this.$Message.error('当前用户没有删除用户权限！')
          }
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('删除用户失败！')
      })
    },
    // 展示添加 编辑用户的弹窗
    showAddDrawer () {
      if (this.userData.userName) {
        this.disableUsername = true
      } else {
        this.disableUsername = false
        this.drawerTitle = '添加用户' // 如果是新增加用户，弹窗标题是 添加用户
      }
      this.drawer = true
    },
    // 保存、更新用户信息
    saveUser () {
      this.$refs.userInfoForm.validate((valid) => {
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
            // 根据是否有 userData 是否有 id 判断是更新还是新增加
            let updateUserBoolean = false
            let addUserBoolean = false
            if (this.userData.id && this.userData.id !== '') {
              updateUserBoolean = true
              addUserBoolean = false
            } else {
              updateUserBoolean = false
              addUserBoolean = true
            }

            // 判断用户是否有用户权限管理页面的权限，而且，如果是更新用户就要有更新的权限，如果是新增用户，就要有添加用户的权限
            if (((this.accessAdd && addUserBoolean) || (this.accessUpdate && updateUserBoolean)) && this.accessUserManage) {
              this.userData.authIds = this.targetKeys
              saveUser(this.userData).then(result => {
                if (result.data.errorCode && result.data.errorCode === '0') {
                  this.$Message.success('用户保存成功！')
                  // 保存之后，当前弹窗数据清空关闭
                  this.userData = {}
                  this.targetKeys = []
                  // 重新加载列表
                  getAllUser().then(res => {
                    if (res.data.errorCode && res.data.errorCode === '0') {
                      this.tableData = res.data.result
                      this.tableDataCount = this.tableData.length
                    }
                  })
                  this.drawer = false
                } else {
                  this.$Message.error('用户保存失败')
                }
              })
            } else {
              if (!this.accessUserManage) {
                this.$Message.error('当前用户没有用户管理的权限！')
              } else if (addUserBoolean) {
                this.$Message.error('当前用户没有添加用户的权限！')
              } else {
                this.$Message.error('当前用户没有更新用户的权限！')
              }
            }
          }).catch(() => {
            setToken('')
            this.$store.state.user.access = []
            this.$Message.error('用户保存失败！')
          })
        }
      })
    },
    // 关闭 编辑 的弹窗，把已填写的数据清空
    cancelSaveUser () {
      this.userData = {}
      this.targetKeys = []
      this.drawer = false
    },
    // 点击右上角的 关闭 按钮，关闭 配置用户 的弹窗，把已填写的数据清空
    closeDrawer () {
      this.userData = {}
      this.targetKeys = []
    },
    // 用户权限的穿梭框，根据页面高度跳转穿梭框的高度
    changeHeight () {
      this.listStyle.height = window.innerHeight - 300 + 'px'
    }
  },
  mounted () {
    // 初始获取所有用户
    getAllUser().then(res => {
      if (res.data.result) {
        this.tableData = res.data.result
      } else {
        this.tableData = []
      }
      this.tableDataCount = this.tableData.length
    })
    getAllAuth().then(res => {
      if (res.data.result) {
        res.data.result.forEach((item) => {
          if (item.authCode === 'admin' || item.authCode === 'super_admin') {
            this.allAuth.push({ key: item.id, label: item.authName, disabled: true })
          } else {
            this.allAuth.push({ key: item.id, label: item.authName })
          }
        })
      }
    })
    //  用户权限的穿梭框，根据页面高度跳转穿梭框的高度
    window.addEventListener('resize', this.changeHeight)
    //   用户权限的穿梭框，初始化穿梭框的高度
    this.changeHeight()
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
      return hasOneOf(['super_admin', 'admin', 'user_add'], this.access)
    },
    //  是否有更新功能权限
    accessUpdate () {
      return hasOneOf(['super_admin', 'admin', 'user_update'], this.access)
    },
    //  是否有删除功能权限
    accessDelete () {
      return hasOneOf(['super_admin', 'admin', 'user_delete'], this.access)
    },
    //  是否有当前页面权限
    accessUserManage () {
      return hasOneOf(['super_admin', 'admin', 'user_manage'], this.access)
    }
  }
}
</script>

<style>

</style>
