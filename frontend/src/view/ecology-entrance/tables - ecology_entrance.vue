<template>
  <div>
    <Button type="primary" size="default" v-if="accessAdd" @click="modal1=true">添加</Button>
    <Modal
      v-model="modal1"
      title="添加生态入口"
      @on-ok="ok"
      @on-cancel="cancel"
      :loading="loading"
      width="540">
      <p>生态入口名称：<input size="65" autofocus v-model="addInput" placeholder="请输入20个字符以内的生态入口名称，不能包含、符号，且不能与已存在重复"
                       maxlength="20"/>
      </p>
      <div slot="footer">
        <Button @click="cancel">取消</Button>
        <Button type="primary" :loading="loading" @click="ok">确定</Button>
      </div>
    </Modal>
    <Card>
      <div v-if="accessUpdate">
        <tables ref="tables" editable searchable border stripe search-place="" v-model="tableData" :columns="columns"
                @on-start-edit="startEdit" @on-cancel-edit="cancelEdit" @on-save-edit="saveEdit"/>
      </div>
      <div v-else>
        <tables ref="tables" searchable border stripe search-place="" v-model="tableData" :columns="columns"
                @on-start-edit="startEdit" @on-cancel-edit="cancelEdit" @on-save-edit="saveEdit"/>
      </div>
    </Card>
  </div>
</template>

<script>
import Tables from '_c/tables'
import { deleteEcologyEntranceById, getEcologyEntrance, saveEcologyEntrance } from '@/api/data'
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
      loading: false,
      addInput: '',
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
    startEdit (params) {
      this.$Message.info({
        content: '生态入口名称不能为空，长度不能超过20个字，不能包含、符号，且不能与已存在重复！',
        duration: 3
      })
    },
    cancelEdit (params) {

    },
    // 保存更新
    saveEdit (params) {
      // 校验功能名称
      if (!params || !params.value || params.value.trim().length < 1) {
        this.$Message.error({
          content: '生态入口名称不可以为空！',
          duration: 5
        })
        // 保存失败之后，表格上该行的数据置为原来的
        this.tableData[params.index].name = params.row.name
        return
      }
      if (params.value != null && params.value.length > 20) {
        this.$Message.error({
          content: '生态入口名称长度不能超过20个字！',
          duration: 5
        })
        // 保存失败之后，表格上该行的数据置为原来的
        this.tableData[params.index].name = params.row.name
        return
      }
      if (params.value.indexOf('、') > -1) {
        this.$Message.error({
          content: '生态入口名称不可以包含、字符！',
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
        if (this.accessUpdate && this.accessEcologyEntrance) {
          let p = params.row
          let functionName_orgin = p.name
          p.name = params.value
          saveEcologyEntrance(p).then(res => {
            if (res.data.errorCode === '0') {
              this.$Message.success('更新成功')
            } else {
              this.$Message.info('更新失败:' + res.data.msg)
              // 保存失败之后，表格上该行的数据置为原来的
              this.tableData[params.index].name = functionName_orgin
            }
          })
        } else {
          // 保存失败之后，表格上该行的数据置为原来的
          this.tableData[params.index].name = params.row.name
          if (!this.accessEcologyEntrance) {
            this.$Message.error('当前用户没有生态入口的权限！')
          } else {
            this.$Message.error('当前用户没有更新生态入口的权限！')
          }
        }
      }).catch(() => {
        setToken('')
        this.$store.state.user.access = []
        // 保存失败之后，表格上该行的数据置为原来的
        this.tableData[params.index].name = params.row.name
        this.$Message.error('当前用户没有更新生态入口的权限！')
      })
    },
    setColumns () {
      // 如果有更新生态入口的权限，则 生态入口 一列数据是可以编辑的
      if (this.accessUpdate) {
        this.columns.push({
          title: '生态入口',
          align: 'left',
          editable: true,
          key: 'name'
        })
      } else {
        this.columns.push({
          title: '生态入口',
          align: 'left',
          editable: false,
          key: 'name'
        })
      }
      // 判断是否有删除权限，控制是否显示 删除 按钮
      if (this.accessDelete) {
        this.columns.push(
          {
            title: '操作',
            key: 'action',
            width: 80,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
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
                        if (this.accessEcologyEntrance) {
                          // 判断时候有删除生态入口权限
                          if (this.accessDelete) {
                            this.$Modal.confirm({
                              title: '删除生态入口',
                              content: '确定要删除该生态入口吗？',
                              onOk: () => {
                                this.remove(params.index, params.row.id)
                              },
                              onCancel: () => {
                                // this.$Message.info('Clicked cancel');
                              }
                            })
                          } else {
                            this.$Message.error('当前用户没有删除生态入口的权限！')
                          }
                        } else {
                          this.$Message.error('当前用户没有生态入口的权限！')
                        }
                      }).catch(() => {
                        setToken('')
                        this.$store.state.user.access = []
                        this.$Message.error('删除生态入口失败！')
                      })
                    }
                  }
                }, '删除')
              ])
            }
          })
      }
    },
    // 删除生态入口
    remove (index, id) {
      deleteEcologyEntranceById(id).then(res => {
        if (res.data.errorCode === '0') {
          this.tableData.splice(index, 1)
          this.$Message.success('删除生态入口成功！')
        } else {
          this.$Message.error('删除生态入口失败！')
        }
      })
    },
    // 添加新生态入口，
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
        // 判断是否是有 当前页面权限 和 添加生态入口权限
        if (this.accessAdd && this.accessEcologyEntrance) {
          this.loading = true
          // 校验生态入口名称
          if (!this.addInput || this.addInput.trim() === '') {
            this.loading = false
            this.$Message.error({
              content: '生态入口名称不能够为空！',
              duration: 5
            })
            return
          }
          if (!this.addInput.trim().length > 20) {
            this.loading = false
            this.$Message.error({
              content: '生态入口名称长度不能超过20！',
              duration: 5
            })
            return
          }

          if (this.addInput.indexOf('、') > -1) {
            this.loading = false
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
              this.loading = false
              this.$Message.error({
                content: '生态入口添加失败：' + res.data.msg,
                duration: 5
              })
            }
          })
        } else {
          this.loading = false
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
    cancel () {
      this.addInput = ''
      this.loading = false
      this.modal1 = false
    }
  },
  mounted () {
    getEcologyEntrance().then(res => {
      this.tableData = res.data.result
    })
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
