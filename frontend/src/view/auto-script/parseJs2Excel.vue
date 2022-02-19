<template>
  <div>
    <!-- <span v-if="accessAdd">
      <Button type="primary" @click="showAddDrawer">添加</Button>
    </span> -->
    <Upload action="http://101.43.119.118:88/pm/autoScript/parseJs2Excel" :before-upload="handleBeforeUpload" accept=".js">
      <Button icon="ios-cloud-upload-outline" :loading="uploadLoading" @click="handleUploadFile">上传文件</Button>
    </Upload>
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
    },




    // 上传文件预处理，读取文件内容，只接受 js 格式文件
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
        const fileExt = file.name.split('.').pop().toLocaleLowerCase()
        if (fileExt === 'js') {
          this.readFile(file)
          this.file = file
          return false
        } else {
          this.$Notice.warning({
            title: '文件类型错误',
            desc: '文件：' + file.name + '不是js文件，请选择后缀为.js的文件。'
          })
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('导入失败！')
      })
      return false
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
        (header.indexOf('功能') > -1) &&
        (header.indexOf('场景') > -1) &&
        (header.indexOf('语音功能') > -1) &&
        (header.indexOf('生态入口') > -1) &&
        (header.indexOf('传感器') > -1)
    },
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
