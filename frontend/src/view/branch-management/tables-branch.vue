<template>
  <div>
    <Button type="primary" size="default" v-if="accessAdmin" @click="showAddModal">添加</Button>
    <Modal
      v-model="modal1"
      :title="branchModalTitle"
      @on-ok="ok"
      @on-cancel="cancel"
      :loading="loading"
      width="540">
      <p style="margin-top: 10px;margin-bottom: 10px">
        品牌名称：<input clearable size="65" autofocus v-model="addInput" placeholder="请输入20个字符以内的品牌名称，且不能与已存在重复"
                    maxlength="20"/>
      </p>
      <div slot="footer">
        <Button @click="cancel">取消</Button>
        <Button type="primary" :loading="loading" @click="ok">确定</Button>
      </div>
    </Modal>
    <Card>

      <tables ref="tables" searchable border stripe search-place="" v-model="tableData" :columns="columns"
              @on-save-edit="saveEdit"/>

    </Card>
  </div>
</template>

<script>
import Tables from '_c/tables'
import {
  saveVoiceFunction,
  getBranchList,
  saveBranch,
  deleteBranchByCode
} from '@/api/data'
import { hasOneOf } from '@/libs/tools'
import store from '@/store'
import { getToken, setToken } from '@/libs/util'

export default {
  name: 'tables_branch',
  components: {
    Tables
  },
  data () {
    return {
      branchModalTitle: '添加品牌',
      loading: false,
      addInput: '',
      branchCode:'',
      modal1: false,
      productTypeToAuth: {
        electric_heater: 'function_electric_heater',
        gas_heater_stove: 'function_gas_heater_stove',
        water_purification: 'function_water_purification',
        water_drink: 'function_water_drink',
        rang_hood_type: 'function_rang_hood_type',
        integrated_gas_combined_kitchen: 'function_integrated_gas_combined_kitchen',
        diswasher_type: 'function_diswasher_type',
        disinfection_cabinet_type: 'function_disinfection_cabinet_type',
        gas_stove: 'funciton_gas_stove',
        gas_combined_kitchen: 'function_gas_combined_kitchen'
      },
      columns: [],
      tableData: []
    }
  },
  methods: {
    showAddModal () {
      this.branchModalTitle = '添加品牌'
      this.modal1 = true
    },
    // 保存更新
    saveEdit (params) {
      // 校验功能名称
      if (!params || !params.value || params.value.trim().length < 1) {
        this.$Message.error({
          content: '品牌名称不可以为空！',
          duration: 5
        })
        // 保存失败之后，表格上该行的数据置为原来的
        this.tableData[params.index].name = params.row.name
        return
      }

      if (params.value != null && params.value.length > 20) {
        this.$Message.error({
          content: '品牌名称长度不能超过20个字！',
          duration: 5
        })
        // 保存失败之后，表格上该行的数据置为原来的
        this.tableData[params.index].name = params.row.name
        return
      }

      // 获取用户权限，
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      }
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，获取用户权限access， 存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        this.$store.state.user.access = user.access
        // 判断是否是有权限更新 以及 是否有当前页面的权限
        if (this.accessAdmin) {
          let p = params.row
          let branch_origin = p.name
          p.name = params.value
          saveVoiceFunction(p).then(res => {
            if (res.data.errorCode === '0') {
              this.$Message.success('更新成功')
            } else {
              this.$Message.error('更新失败:' + res.data.msg)
              // 保存失败之后，表格上该行的数据置为原来的
              this.tableData[params.index].name = branch_origin
            }
          })
        } else {
          // 保存失败之后，表格上该行的数据置为原来的
          this.tableData[params.index].name = params.row.name
          if (!this.accessVoiceFunction) {
            this.$Message.error('当前用户没有语音功能的权限！')
          } else {
            this.$Message.error('当前用户没有更新语音功能的权限！')
          }
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        // 保存失败之后，表格上该行的数据置为原来的
        this.tableData[params.index].name = params.row.name
        this.$Message.error('当前用户没有更新语音功能的权限！')
      })
    },
    setColumns () {
      // 如果有更新功能的权限，则 功能 一列数据是可以编辑的
      this.columns = []
      this.columns.push({
        title: '品牌',
        align: 'center',
        editable: false,
        key: 'value'
      })
      // 判断是否有删除权限，控制是否显示 删除 按钮
      if (this.accessAdmin) {
        this.columns.push(
          {
            title: '操作',
            key: 'action',
            maxWidth: 125,
            align: 'center',
            render: (h, params) => {
              let deleteButton = h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                style: {
                  marginLeft: '5px'
                },
                on: {
                  click: () => {
                    // 获取用户权限
                    const token = getToken()
                    store.commit('setToken', token)
                    if (!token) {
                      this.$store.state.user.access = []
                    }
                    store.dispatch('getUserInfo').then(user => {
                      // 拉取用户信息，获取用户权限access， 存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
                      this.$store.state.user.access = user.access
                      // 判断是否有当前页面的权限
                      if (this.accessAdmin) {
                        // 判断时候有删除功能权限
                        if (this.accessAdmin) {
                          this.$Modal.confirm({
                            title: '',
                            content: '一旦删除将无法恢复，确定要删除吗？',
                            onOk: () => {
                              this.remove(params.index, params.row.code)
                            },
                            onCancel: () => {
                              // this.$Message.info('Clicked cancel');
                            }
                          })
                        } else {
                          this.$Message.error('当前用户没有删除语音功能的权限！')
                        }
                      } else {
                        this.$Message.error('当前用户没有语音功能的权限！')
                      }
                    }).catch(() => {
                      setToken('')
                      this.$store.state.user.access = []
                      this.$Message.error('删除语音功能失败！')
                    })
                  }
                }
              }, '删除')
              let editButton = h('Button', {
                props: {
                  type: 'primary',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.branchModalTitle = '编辑品牌'
                    this.modal1 = true
                    this.addInput =params.row.value
                    this.branchCode = params.row.code
                  }
                }
              }, '编辑')
              let buttons = []
              buttons.push(editButton)
              buttons.push(deleteButton)
              return h('div', buttons)
            }
          })
      }
    },
    // 删除功能
    remove (index, code) {
      deleteBranchByCode(code).then(res => {
        if (res.data.errorCode === '0') {
          this.$Message.success('删除品牌成功！')
          this.getAllBranch()
        } else {
          this.$Message.error('删除品牌失败：'+ res.data.msg)
        }
      }).catch(reason => {
        this.$Message.error('删除品牌失败：'+ reason)
      })
    },
    getAllBranch () {
      getBranchList().then(result => {
        if (result.data.errorCode === '0') {
          this.tableData = result.data.result
        } else {
          this.$Message.success('获取品牌列表失败：' + result.data.msg)
        }
      }).catch(reason => {
        this.$Message.success('获取品牌列表失败：' + reason)
      }).finally(() => {
      })
    },
    // 添加新品牌，
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
        this.$store.state.user.access = user.access
        // 判断是否是有 当前页面权限 和 添加功能权限
        if (this.accessAdmin) {
          this.loading = true
          // 校验功能名称
          if (!this.addInput || this.addInput.trim() === '') {
            this.loading = false
            this.$Message.error({
              content: '品牌名称不能为空！',
              duration: 5
            })
            return
          }
          if (!this.addInput.trim().length > 20) {
            this.loading = false
            this.$Message.error({
              content: '品牌名称长度不能超过20！',
              duration: 5
            })
            return
          }
          saveBranch({ name: this.addInput ,code:this.branchCode}).then(res => {
            if (res.data.errorCode === '0') {
              this.modal1 = false
              this.addInput = ''
              this.$Message.success('品牌添加成功！')
              this.getAllBranch()
            } else {
              this.$Message.error({
                content: '品牌添加失败：' + res.data.msg,
                duration: 3
              })
            }
          }).catch(reason => {
            this.$Message.success('品牌添加失败:' + reason)
            this.loading = false
          }).finally(() => {
            this.loading = false
          })
        } else {
          this.loading = false
          this.$Message.error('当前用户没有品牌的权限！')
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        this.$Message.error('添加品牌失败！')
      })
    },
    cancel () {
      this.addInput = ''
      this.loading = false
      this.modal1 = false
    }
  },
  mounted () {
    this.getAllBranch()
    /*getBranchList().then(res => {
      this.tableData = res.data.result
    })*/
    /*getVoiceFunction().then(res => {
      this.tableData = res.data.result
    })*/
  },
  beforeMount () {
    this.setColumns()
  },
  computed: {
    access () {
      return this.$store.state.user.access
    },
    accessAdmin () {
      return hasOneOf(['super_admin', 'admin'], this.access)
    }
    /*//  是否有添加功能权限
    accessAdd () {
      return hasOneOf(['super_admin', 'admin', 'voice_function_add'], this.access)
    },
    //  是否有更新功能权限
    accessUpdate () {
      return hasOneOf(['super_admin', 'admin', 'voice_function_update'], this.access)
    },
    //  是否有删除功能权限
    accessDelete () {
      return hasOneOf(['super_admin', 'admin', 'voice_function_delete'], this.access)
    },
    //  是否有当前页面的权限
    accessVoiceFunction () {
      return hasOneOf(['super_admin', 'admin', 'voice_function'], this.access)
    }*/
  }
}
</script>

<style>

</style>
