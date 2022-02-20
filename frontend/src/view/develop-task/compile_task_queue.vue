<template>
  <div>
    <Card>
      <tables ref="tables" searchable border stripe search-place="" v-model="tableData" :columns="columns"
              @on-start-edit="startEdit" @on-cancel-edit="cancelEdit" @on-save-edit="saveEdit"/>
    </Card>
  </div>
</template>

<script>
import Tables from '_c/tables'
import { getQueue } from '@/api/data'
import { hasOneOf } from '@/libs/tools'
import config from '@/config'

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
      columns: [],
      tableData: []
    }
  },
  methods: {
    setColumns () {
      this.columns.push({
        title: '批次号',
        align: 'center',
        editable: false,
        key: 'id'
      })
      this.columns.push({
        title: '任务类型',
        align: 'center',
        editable: false,
        key: 'taskType'
      })
      this.columns.push({
        title: '任务id',
        align: 'center',
        editable: false,
        key: 'developTaskId'
      })
      this.columns.push({
        title: '操作人',
        align: 'center',
        editable: false,
        key: 'userId'
      })
      this.columns.push({
        title: '操作时间',
        align: 'center',
        editable: false,
        key: 'createDateTime'
      })
      this.columns.push({
        title: '状态',
        align: 'center',
        editable: false,
        key: 'status'
      })
      this.columns.push({
        title: '操作',
        key: 'action',
        width: 80,
        align: 'center',
        render: (h, params) => {
          if (params.row.status === '已完成') {
            return h('div', [
              h('a', {
                attrs: {
                  // href: `${config.baseUrl.dev}/pm/task/fileDownload?fileId=${params.row.result}` // 正式用
                  href: `${config.baseUrl.dev}task/fileDownload?fileId=${params.row.result}` // 调试用
                }
              }, '下载')
            ])
          } else {
            return h('div', [
            ])
          }
        }
      })
    }
  },
  mounted () {
    this.productType = this.$route.meta.productType
    getQueue().then(res => {
      this.tableData = res.data.result
    })
  },
  beforeMount () {
    this.setColumns()
  },
  computed: {
    access () {
      return this.$store.state.user.access
    }
  }
}
</script>

<style>

</style>
