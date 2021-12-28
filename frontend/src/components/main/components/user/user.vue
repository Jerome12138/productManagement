<template>
  <div class="user-avator-dropdown">
    <Dropdown @on-click="handleClick">
      <!--<Badge :dot="!!messageUnreadCount">
        <Avatar :src="userAvator"/>
      </Badge>-->
      <Badge>
        <Avatar :src="userAvator"/>
      </Badge>
      <Icon :size="18" type="md-arrow-dropdown"></Icon>
      <DropdownMenu slot="list">
        <!-- <DropdownItem name="message">
           消息中心<Badge style="margin-left: 10px" :count="messageUnreadCount"></Badge>
         </DropdownItem>-->
        <DropdownItem name="updatePassword">修改密码</DropdownItem>
        <DropdownItem name="logout">退出登录</DropdownItem>
      </DropdownMenu>
    </Dropdown>
    <Modal
      v-model="modal1"
      title="修改密码"
      @on-ok="savePassword"
      @on-cancel="cancel"
      :loading="loading"
    >
      <Form ref="updatePasswordForm" label-position="right" :label-width="80">
        <Row :gutter="0">
          <Col span="24">
            <FormItem label="原密码:" prop="passInputOrigin" :rules="{required:true,message:'不能为空', trigger: 'blur'}">
              <input size="60" autofocus type="password" v-model="passInputOrigin" placeholder="请输入用户原来的密码"
                     maxlength="20"/>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="0">
          <Col span="24">
            <FormItem label="新密码:" prop="passInputNew" :rules="{required:true,message:'不能为空', trigger: 'blur'}">
              <input size="60" autofocus type="password" v-model="passInputNew" placeholder="请输入新密码,长度在20个字符以内"
                     maxlength="20"/>
            </FormItem>
          </Col>
        </Row>
        <Row :gutter="0">
          <Col span="24">
            <FormItem label="确认新密码:" prop="passInputNewConfirm"
                      :rules="{required:true,message:'不能为空', trigger: 'blur'}">
              <input size="60" autofocus type="password" v-model="passInputNewConfirm" placeholder="请输入新密码,长度在20个字符以内"
                     maxlength="20"/>
            </FormItem>
          </Col>
        </Row>
      </Form>
      <div slot="footer">
        <Button @click="cancel">取消</Button>
        <Button type="primary" @click="savePassword">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import './user.less'
import { mapActions } from 'vuex'

export default {
  name: 'User',
  data () {
    return {
      modal1: false,
      passInputOrigin: '',
      passInputNew: '',
      passInputNewConfirm: '',
      loading: false
    }
  },
  props: {
    userAvator: {
      type: String,
      default: ''
    },
    messageUnreadCount: {
      type: Number,
      default: 0
    },
    userName: {
      type: String,
      default: ''
    }
  },
  methods: {
    ...mapActions([
      'handleLogOut',
      'updatePasswordForUser'
    ]),
    logout () {
      this.handleLogOut().then(() => {
        this.$router.push({
          name: 'login'
        })
      })
    },
    message () {
      this.$router.push({
        name: 'message_page'
      })
    },
    updatePassword () {
      this.modal1 = true
    },
    savePassword () {
      this.$refs.updatePasswordForm.validate((valid) => {
        if (valid) {
          this.loading = true
          if (!this.passInputOrigin) {
            this.$Message.error('原密码不可以为空')
            return
          }
          if (!this.passInputNew) {
            this.$Message.error('新密码不可以为空')
            return
          }
          if (this.passInputNew !== this.passInputNewConfirm) {
            this.$Message.error('确认新密码与新密码不一致！')
            return
          }
          this.loading = true
          let passwordOrigin = this.passInputOrigin
          let passwordNew = this.passInputNew
          this.updatePasswordForUser({ passwordOrigin, passwordNew }).then(res => {
            if (res.data.errorCode === '0') {
              this.modal1 = false
              this.loading = false
              this.$Message.success('修改成功！')
              this.$router.push({
                name: 'login'
              })
            } else {
              this.loading = false
              this.$Message.error(res.data.msg)
            }
          })
        }
      })
    },
    cancel () {
      this.passInputNew = ''
      this.passInputOrigin = ''
      this.passInputNewConfirm = ''
      this.modal1 = false
      this.loading = false
    },
    handleClick (name) {
      switch (name) {
        case 'logout':
          this.logout()
          break
        case 'message':
          this.message()
          break
        case 'updatePassword':
          this.updatePassword()
          break
      }
    }
  }
}
</script>
