<template>
  <div>
    <Button v-if="accessAdd" type="primary" size="default" @click="modal1=true">添加</Button>
    <Modal
      v-model="modal1"
      title="添加场景"
      @on-ok="ok"
      @on-cancel="cancel"
      :loading="loading"
    >
      <p>场景名称：<input size="65" autofocus v-model="addInput" placeholder="请输入20个字符以内的场景名称，不能包含、字符，且不能与已存在重复"
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
                @on-start-edit="startEdit" @on-cancel-edit="cancelEdit"
                @on-save-edit="saveEdit"/>
      </div>
      <div v-else>
        <tables ref="tables" searchable border stripe search-place="" v-model="tableData" :columns="columns"
                @on-start-edit="startEdit" @on-cancel-edit="cancelEdit"
                @on-save-edit="saveEdit"/>
      </div>
    </Card>
  </div>
</template>

<script>
import Tables from '_c/tables'
import { deleteScenarioById, getScenarioByType, updateScenario, saveScenario } from '@/api/data'
import { hasOneOf } from '@/libs/tools'
import { getToken, setToken } from '@/libs/util'
import store from '@/store'

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
        electric_heater: 'scenario_electric_heater',
        gas_heater_stove: 'scenario_gas_heater_stove',
        water_purification: 'scenario_water_purification',
        water_drink: 'scenario_water_drink',
        rang_hood_type: 'scenario_rang_hood_type',
        integrated_gas_combined_kitchen: 'scenario_integrated_gas_combined_kitchen',
        diswasher_type: 'scenario_diswasher_type',
        disinfection_cabinet_type: 'scenario_disinfection_cabinet_type',
        gas_stove: 'scenario_gas_stove',
        gas_combined_kitchen: 'scenario_gas_combined_kitchen'
      },
      columns: [],
      tableData: []
    }
  },
  methods: {
    startEdit (params) {
      this.$Message.info({
        content: '场景名称不能为空，长度不能超过20个字，不能包含、符号，也不能与已存在重复！',
        duration: 3
      })
    },
    cancelEdit (params) {

    },
    // 更新
    saveEdit (params) {
      if (!params || !params.value || params.value.trim().length < 1) {
        this.$Message.error({
          content: '场景名称不能为空！',
          duration: 5
        })
        this.tableData[params.index].scenarioName = params.row.scenarioName
        return
      }

      if (params.value != null && params.value.trim().length > 20) {
        this.$Message.error({
          content: '场景名称长度不能超过20个字！',
          duration: 5
        })
        this.tableData[params.index].scenarioName = params.row.scenarioName
        return
      }

      if (params.value.indexOf('、') > -1) {
        this.$Message.error({
          content: '场景名称不能包含、字符！',
          duration: 5
        })
        this.tableData[params.index].scenarioName = params.row.scenarioName
        return
      }

      // 获取用户权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      } else {
        store.dispatch('getUserInfo').then(user => {
          // 拉取用户信息，获取用户权限存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
          this.$store.state.user.access = user.access

          let p = params.row
          let scenarioName_orgin = p.scenarioName
          p.scenarioName = params.value
          // 判断是否是有更新场景的权限 和 当前页面的权限
          if (this.accessUpdate && this.accessScenarioProductType) {
            // 开始更新
            updateScenario(p).then(res => {
              if (res.data.errorCode === '0') {
                this.$Message.success('更新成功')
              } else {
                this.$Message.info('更新失败:' + res.data.msg)
                this.tableData[params.index].scenarioName = scenarioName_orgin
              }
            })
          } else {
            this.tableData[params.index].scenarioName = scenarioName_orgin
            if (!this.accessScenarioProductType) {
              this.$Message.info('当前用户没有此类产品场景的权限！')
            } else {
              this.$Message.info('当前用户没有更新场景的权限！')
            }
          }
        }).catch(() => {
          setToken('')
          this.$store.state.user.access = []
          this.$Message.error('更新场景失败！')
        })
      }
    },
    setColumns () {
      // 如果有场景更新的权限，此列内容可以更新
      if (this.accessUpdate) {
        this.columns.push({
          title: '场景',
          key: 'scenarioName',
          editable: true,
          align: 'center'
        })
      } else {
        this.columns.push({
          title: '场景',
          key: 'scenarioName',
          editable: false,
          align: 'center'
        })
      }
      // 如果有删除场景的权限，展示操作一栏，操作一栏有删除按钮
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
                      this.$Modal.confirm({
                        title: '删除场景',
                        content: '确定要删除该场景吗？',
                        onOk: () => {
                          this.remove(params.index, params.row.id)
                        },
                        onCancel: () => {
                        }
                      })
                    }
                  }
                }, '删除')
              ])
            }
          })
      }
    },
    // 删除场景，删除之前先判断是否有权限
    remove (index, id) {
      // 获取用户权限
      const token = getToken()
      store.commit('setToken', token)
      if (!token) {
        this.$store.state.user.access = []
      } else {
        store.dispatch('getUserInfo').then(user => {
          // 拉取用户信息，获取用户权限存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
          this.$store.state.user.access = user.access
          // 判断是否是有当前页面的权限 和 是否有 删除场景的权限
          if (this.accessDelete && this.accessScenarioProductType) {
            // 删除场景
            deleteScenarioById(id).then(res => {
              if (res.data.errorCode === '0') {
                this.tableData.splice(index, 1)
                this.$Message.success('删除场景成功！')
              } else {
                this.$Message.error('删除场景失败！')
              }
            })
          } else {
            if (!this.accessScenarioProductType) {
              this.$Message.info('当前用户没有此类产品场景的权限！')
            } else {
              this.$Message.info('当前用户没有删除场景的权限！')
            }
          }
        }).catch(() => {
          setToken('')
          this.$store.state.user.access = []
          this.$Message.error('删除场景失败！')
        })
      }
    },
    // 添加新的
    ok () {
      this.loading = true
      // 校验场景名称
      if (!this.addInput || this.addInput.trim() === '') {
        this.loading = false
        this.$Message.error({
          content: '场景名称不能够为空！',
          duration: 5
        })
      } else if (!this.addInput.trim().length > 20) {
        this.loading = false
        this.$Message.error({
          content: '场景名称长度不能超过20！',
          duration: 5
        })
      } else if (this.addInput.indexOf('、') > -1) {
        this.loading = false
        this.$Message.error({
          content: '场景名称不能包含、符号！',
          duration: 5
        })
      } else {
        // 获取用户权限
        const token = getToken()
        store.commit('setToken', token)
        if (!token) {
          this.$store.state.user.access = []
        } else {
          store.dispatch('getUserInfo').then(user => {
            // 拉取用户信息，获取用户权限存储到this.$store.state.user.access;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
            this.$store.state.user.access = user.access
            // 判断是否是有修改的权限
            if (this.accessAdd && this.accessScenarioProductType) {
              // 保存新场景
              saveScenario({ scenarioName: this.addInput, typeCode: this.productType }).then(res => {
                if (res.data.errorCode === '0') {
                  this.loading = false
                  this.modal1 = false
                  this.addInput = ''
                  this.$Message.success('场景添加成功！')
                  getScenarioByType(this.productType).then(res => {
                    this.tableData = res.data.result
                  })
                } else {
                  this.loading = true
                  setTimeout(() => {
                    this.loading = false
                    this.modal1 = true
                    this.$Message.error('场景添加失败：' + res.data.msg)
                  }, 100)
                }
              })
            } else {
              this.loading = false
              this.modal1 = true
              if (!this.accessScenarioProductType) {
                this.$Message.info('当前用户没有此类产品场景的权限！')
              } else {
                this.$Message.info('当前用户没有添加场景的权限！')
              }
            }
          }).catch(() => {
            setToken('')
            this.$store.state.user.access = []
            this.$Message.error('添加场景失败！')
          })
        }
      }
    },
    cancel () {
      this.addInput = ''
      this.modal1 = false
      this.loading = false
    }
  },
  mounted () {
    // 产品类型是从页面传过来的
    this.productType = this.$route.meta.productType
    getScenarioByType(this.productType).then(res => {
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
    //  是否有添加场景权限
    accessAdd () {
      return hasOneOf(['super_admin', 'admin', 'scenario_add'], this.access)
    },
    //  是否有更新场景权限
    accessUpdate () {
      return hasOneOf(['super_admin', 'admin', 'scenario_update'], this.access)
    },
    //  是否有删除场景权限
    accessDelete () {
      return hasOneOf(['super_admin', 'admin', 'scenario_delete'], this.access)
    },
    //  是否有当前页面权限
    accessScenarioProductType () {
      return hasOneOf(['super_admin', 'admin', this.productTypeToAuth[this.productType]], this.access)
    }
  }
}
</script>

<style>

</style>
