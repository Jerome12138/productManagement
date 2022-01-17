export default {
  /**
   * @description 配置显示在浏览器标签的title
   */
  title: '产品管理',
  /**
   * @description token在Cookie中存储的天数，默认1天
   */
  cookieExpires: 0.5,
  /**
   * @description 是否使用国际化，默认为false
   *              如果不使用，则需要在路由中给需要在菜单中展示的路由设置meta: {title: 'xxx'}
   *              用来在菜单中显示文字
   */
  useI18n: false,
  /**
   * @description api请求基础路径
   */
  baseUrl: {
    dev: 'http://101.43.119.118:12108/pm/',
    // dev: 'http://121.43.198.225:8080/',
    pro: 'http://101.43.119.118:88/pm/'
  },
  /**
   * @description 默认打开的首页的路由name值，默认为home
   */
  homeName: 'all',
  /**
   * @description 需要加载的插件
   */
  plugin: {
    'error-store': {
      showInHeader: true, // 设为false后不会在顶部显示错误日志徽标
      developmentOff: true // 设为true后在开发环境不会收集错误信息，方便开发中排查错误
    }
  }
}
