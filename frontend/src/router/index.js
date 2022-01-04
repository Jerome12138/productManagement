import Vue from 'vue'
import Router from 'vue-router'
import routes from './routers'
import store from '@/store'
import iView from 'iview'
import { setToken, getToken, canTurnTo, setTitle } from '@/libs/util'
import config from '@/config'
const { homeName } = config
// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = Router.prototype.push
Router.prototype.push = function push (location) {
  return originalPush.call(this, location).catch(err => err)
}
Vue.use(Router)
const router = new Router({
  routes,
  mode: 'history',
  base: '/pm/'
})
const LOGIN_PAGE_NAME = 'login'

const turnTo = (to, access, next) => {
  if (canTurnTo(to.name, access, routes)) {
    next() // 有权限，可访问
  } else if (to.name === homeName) {
    // 没有home页面的权限时，根据顺序依次寻找有权限的页面，如果都没有，跳转到401
    let redirectOrNot = false
    // 没有home页面权限时，按数组顺序，依次查看是否有权限，有权限的跳转到对应页面，
    let routerNames = ['电热水器', '燃气热水器', '燃气炉', '净水机', '饮水机(含净饮机)', '吸油烟机', '集成灶', '燃气灶(含组合灶)', '洗碗机', '消毒柜',
      '功能-电热水器', '功能-燃气热水器', '功能-燃气炉', '功能-净水机', '功能-饮水机(含净饮机)', '功能-吸油烟机', '功能-集成灶', '功能-燃气灶(含组合灶)', '功能-洗碗机', '功能-消毒柜',
      '场景-电热水器', '场景-燃气热水器', '场景-燃气炉', '场景-净水机', '场景-饮水机(含净饮机)', '场景-吸油烟机', '场景-集成灶', '场景-燃气灶(含组合灶)', '场景-洗碗机', '场景-消毒柜',
      '传感器-电热水器', '传感器-燃气热水器', '传感器-燃气炉', '传感器-净水机', '传感器-饮水机(含净饮机)', '传感器-吸油烟机', '传感器-集成灶', '传感器-燃气灶(含组合灶)', '传感器-洗碗机', '传感器-消毒柜',
      '语音功能', '生态入口', '用户管理', '任务管理', '审核组管理']
    let redirectName = to.name
    try {
      for (let i = 0; i < routerNames.length; i++) {
        if (canTurnTo(routerNames[i], store.state.user.access, routes)) {
          redirectName = routerNames[i]
          redirectOrNot = true
          throw new Error() // 找到有权限的页面，throw new error 是为了退出循环
        }
      }
    } catch (e) {}
    // 如果找到了有权限的页面，跳转到该页面
    if (redirectOrNot) {
      next({
        name: redirectName // 跳转到homeName页
      })
    } else {
      // 所有页面都没有权限，跳转到401 ， 清空token
      next({ replace: true, name: 'error_401' })// 无权限，重定向到401页面
      setToken('') // 且token清空，返回上一页时，就返回到了登录页面
    }
  } else next({ replace: true, name: 'error_401' }) // 无权限，重定向到401页面
}

router.beforeEach((to, from, next) => {
  iView.LoadingBar.start()
  const token = getToken()
  if (!token && to.name !== LOGIN_PAGE_NAME) {
    // 未登录且要跳转的页面不是登录页
    next({
      name: LOGIN_PAGE_NAME // 跳转到登录页
    })
  } else if (!token && to.name === LOGIN_PAGE_NAME) {
    // 未登陆且要跳转的页面是登录页
    next() // 跳转
  } else if (token && to.name === LOGIN_PAGE_NAME) {
    // 已登录且要跳转的页面是登录页
    next({
      name: homeName // 跳转到homeName页
    })
  } else {
    if (store.state.user.hasGetInfo) {
      turnTo(to, store.state.user.access, next)
    } else {
      store.dispatch('getUserInfo').then(user => {
        // 拉取用户信息，通过用户权限和跳转的页面的name来判断是否有权限访问;access必须是一个数组，如：['super_admin'] ['super_admin', 'admin']
        turnTo(to, user.access, next)
      }).catch(() => {
        setToken('')
        next({
          name: 'login'
        })
      })
    }
  }
})

router.afterEach(to => {
  setTitle(to, router.app)
  iView.LoadingBar.finish()
  window.scrollTo(0, 0)
})

export default router
