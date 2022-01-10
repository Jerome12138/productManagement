import Main from '@/components/main'
// import parentView from '@/components/parent-view'

/**
 * iview-admin中meta除了原生参数外可配置的参数:
 * meta: {
 *  title: { String|Number|Function }
 *         显示在侧边栏、面包屑和标签栏的文字
 *         使用'{{ 多语言字段 }}'形式结合多语言使用，例子看多语言的路由配置;
 *         可以传入一个回调函数，参数是当前路由对象，例子看动态路由和带参路由
 *  hideInBread: (false) 设为true后此级路由将不会出现在面包屑中，示例看QQ群路由配置
 *  hideInMenu: (false) 设为true后在左侧菜单不会显示该页面选项
 *  notCache: (false) 设为true后页面在切换标签后不会缓存，如果需要缓存，无需设置这个字段，而且需要设置页面组件name属性和路由配置的name一致
 *  access: (null) 可访问该页面的权限数组，当前路由设置的权限会影响子路由
 *  icon: (-) 该页面在左侧菜单、面包屑和标签导航处显示的图标，如果是自定义图标，需要在图标名称前加下划线'_'
 *  beforeCloseName: (-) 设置该字段，则在关闭当前tab页时会去'@/router/before-close.js'里寻找该字段名对应的方法，作为关闭前的钩子函数
 * }
 */

export default [
  {
    path: '/login',
    name: 'login',
    meta: {
      title: 'Login - 登录',
      hideInMenu: true
    },
    component: () => import('@/view/login/login.vue')
  },
  {
    path: '/argu',
    name: 'argu',
    meta: {
      hideInMenu: true
    },
    component: Main,
    children: [
      {
        path: 'params/:id',
        name: 'params',
        meta: {
          icon: 'md-flower',
          title: route => `{{ params }}-${route.params.id}`,
          notCache: true,
          beforeCloseName: 'before_close_normal'
        },
        component: () => import('@/view/argu-page/params.vue')
      },
      {
        path: 'query',
        name: 'query',
        meta: {
          icon: 'md-flower',
          title: route => `{{ query }}-${route.query.id}`,
          notCache: true
        },
        component: () => import('@/view/argu-page/query.vue')
      }
    ]
  },
  {
    path: '/401',
    name: 'error_401',
    meta: {
      hideInMenu: true
    },
    component: () => import('@/view/error-page/401.vue')
  },
  {
    path: '/500',
    name: 'error_500',
    meta: {
      hideInMenu: true
    },
    component: () => import('@/view/error-page/500.vue')
  },
  {
    path: '*',
    name: 'error_404',
    meta: {
      hideInMenu: true
    },
    component: () => import('@/view/error-page/404.vue')
  },
  {
    path: '/developTask',
    name: '开发任务',
    meta: {
      access: ['super_admin', 'admin', 'develop_task'],
      title: '配置管理',
      icon: 'md-list-box'
    },
    component: Main,
    children: [
      {
        path: '/task_manage',
        name: '任务管理',
        meta: {
          access: ['super_admin', 'admin', 'develop_task'],
          title: '任务管理',
          icon: 'md-list-box'
        },
        component: () => import('@/view/develop-task/task_manage.vue')
      },
      {
        path: '/auditGroup',
        name: '审核组管理',
        meta: {
          access: ['super_admin', 'admin', 'develop_task'],
          title: '审核组管理',
          icon: 'md-people'
        },
        component: () => import('@/view/develop-task/audit_group_manage.vue')
      }
    ]
  },
  {
    path: '/',
    name: '产品管理',
    component: Main,
    redirect: { name: 'all' },
    meta: {
      access: [
        'super_admin',
        'admin',
        'product_all',
        'product_electric_heater',
        'product_gas_heater_stove',
        'product_gas_stove',
        'product_water_purification',
        'product_water_drink',
        'product_rang_hood_type',
        'product_integrated_gas_combined_kitchen',
        'product_gas_combined_kitchen',
        'product_diswasher_type',
        'product_disinfection_cabinet_type'
      ],
      title: '产品管理',
      icon: 'ios-list',
      hideInMenu: false
    },
    children: [
      {
        path: 'all',
        name: 'all',
        meta: {
          title: 'all',
          access: ['super_admin', 'admin', 'product_all']
        },
        component: () => import('@/view/product/tables - all_product.vue')
      }, {
        path: 'electric_heater',
        name: '电热水器',
        meta: {
          productType: 'electric_heater',
          title: '电热水器',
          access: ['super_admin', 'admin', 'product_electric_heater']
        },
        component: () => import('@/view/product/tables-product.vue')
      }, {
        path: 'electric_heater_add',
        name: '电热水器-添加',
        meta: {
          productType: 'electric_heater',
          title: '电热水器-添加',
          access: ['super_admin', 'admin', 'product_electric_heater']
        },
        component: () => import('@/view/product/tables - electric_heater_add.vue')
      },
      // {
      //   path: 'gas_heater_stove',
      //   name: '燃气热水器',
      //   meta: {
      //     productType: 'gas_heater_stove',
      //     title: '燃气热水器',
      //     access: ['super_admin', 'admin', 'product_gas_heater_stove']
      //   },
      //   component: () => import('@/view/product/tables-product.vue')
      // },
      // {
      //   path: 'gas_stove',
      //   name: '燃气炉',
      //   meta: {
      //     productType: 'gas_stove',
      //     title: '燃气炉',
      //     access: ['super_admin', 'admin', 'product_gas_stove']
      //   },
      //   component: () => import('@/view/product/tables-product.vue')
      // },
      // {
      //   path: 'water_purification',
      //   name: '净水机',
      //   meta: {
      //     productType: 'water_purification',
      //     title: '净水机',
      //     access: ['super_admin', 'admin', 'product_water_purification']
      //   },
      //   component: () => import('@/view/product/tables-product.vue')
      // },
      // {
      //   path: 'water_drink',
      //   name: '饮水机(含净饮机)',
      //   meta: {
      //     productType: 'water_drink',
      //     title: '饮水机(含净饮机)',
      //     access: ['super_admin', 'admin', 'product_water_drink']
      //   },
      //   component: () => import('@/view/product/tables-product.vue')
      // },
      // {
      //   path: 'rang_hood_type',
      //   name: '吸油烟机',
      //   meta: {
      //     productType: 'rang_hood_type',
      //     title: '吸油烟机',
      //     access: ['super_admin', 'admin', 'product_rang_hood_type']
      //   },
      //   component: () => import('@/view/product/tables-product.vue')
      // },
      // {
      //   path: 'integrated_gas_combined_kitchen',
      //   name: '集成灶',
      //   meta: {
      //     productType: 'integrated_gas_combined_kitchen',
      //     title: '集成灶',
      //     access: ['super_admin', 'admin', 'product_integrated_gas_combined_kitchen']
      //   },
      //   component: () => import('@/view/product/tables-product.vue')
      // },
      // {
      //   path: 'gas_combined_kitchen',
      //   name: '燃气灶(含组合灶)',
      //   meta: {
      //     productType: 'gas_combined_kitchen',
      //     title: '集成灶、燃气灶、组合灶',
      //     access: ['super_admin', 'admin', 'product_gas_combined_kitchen']
      //   },
      //   component: () => import('@/view/product/tables-product.vue')
      // },
      // {
      //   path: 'diswasher_type',
      //   name: '洗碗机',
      //   meta: {
      //     productType: 'diswasher_type',
      //     title: '洗碗机',
      //     access: ['super_admin', 'admin', 'product_diswasher_type']
      //   },
      //   component: () => import('@/view/product/tables-product.vue')
      // },
      // {
      //   path: 'disinfection_cabinet_type',
      //   name: '消毒柜',
      //   meta: {
      //     productType: 'disinfection_cabinet_type',
      //     title: '消毒柜',
      //     access: ['super_admin', 'admin', 'product_disinfection_cabinet_type']
      //   },
      //   component: () => import('@/view/product/tables-product.vue')
      // }
    ]
  },
  {
    path: '/function',
    name: '功能管理',
    component: Main,
    meta: {
      access: [
        'super_admin',
        'admin',
        'function_electric_heater',
        'function_gas_heater_stove',
        'function_gas_stove',
        'function_water_purification',
        'function_water_drink',
        'function_rang_hood_type',
        'function_integrated_gas_combined_kitchen',
        'function_gas_combined_kitchen',
        'function_diswasher_type',
        'function_disinfection_cabinet_type'
      ],
      title: '功能管理',
      icon: 'ios-apps'
    },
    children: [
      {
        path: 'electric_heater',
        name: '功能-电热水器',
        meta: {
          productType: 'electric_heater',
          title: '电热水器',
          access: ['super_admin', 'admin', 'function_electric_heater']
        },
        component: () => import('@/view/function/tables - electric_heater.vue')
      },
      {
        path: 'gas_heater_stove',
        name: '功能-燃气热水器',
        meta: {
          productType: 'gas_heater_stove',
          title: '燃气热水器',
          access: ['super_admin', 'admin', 'function_gas_heater_stove']
        },
        component: () => import('@/view/function/tables - gas_heater_stove.vue')
      },
      // {
      //   path: 'gas_stove',
      //   name: '功能-燃气炉',
      //   meta: {
      //     productType: 'gas_stove',
      //     title: '燃气炉',
      //     access: ['super_admin', 'admin', 'function_gas_stove']
      //   },
      //   component: () => import('@/view/function/tables - gas_stove.vue')
      // },
      // {
      //   path: 'water_purification',
      //   name: '功能-净水机',
      //   meta: {
      //     productType: 'water_purification',
      //     title: '净水机',
      //     access: ['super_admin', 'admin', 'function_water_purification']
      //   },
      //   component: () => import('@/view/function/tables - water_purification.vue')
      // },
      // {
      //   path: 'water_drink',
      //   name: '功能-饮水机(含净饮机)',
      //   meta: {
      //     productType: 'water_drink',
      //     title: '饮水机(含净饮机)',
      //     access: ['super_admin', 'admin', 'function_water_drink']
      //   },
      //   component: () => import('@/view/function/tables - water_drink.vue')
      // },
      // {
      //   path: 'rang_hood_type',
      //   name: '功能-吸油烟机',
      //   meta: {
      //     productType: 'rang_hood_type',
      //     title: '吸油烟机',
      //     access: ['super_admin', 'admin', 'function_rang_hood_type']
      //   },
      //   component: () => import('@/view/function/tables - rang_hood_type.vue')
      // },
      // {
      //   path: 'integrated_gas_combined_kitchen',
      //   name: '功能-集成灶',
      //   meta: {
      //     productType: 'integrated_gas_combined_kitchen',
      //     title: '集成灶',
      //     access: ['super_admin', 'admin', 'function_integrated_gas_combined_kitchen']
      //   },
      //   component: () => import('@/view/function/tables - integrated_gas_combined_kitchen.vue')
      // },
      // {
      //   path: 'gas_combined_kitchen',
      //   name: '功能-燃气灶(含组合灶)',
      //   meta: {
      //     productType: 'gas_combined_kitchen',
      //     title: '燃气灶(含组合灶)',
      //     access: ['super_admin', 'admin', 'function_gas_combined_kitchen']
      //   },
      //   component: () => import('@/view/function/tables - gas_combined_kitchen.vue')
      // },
      // {
      //   path: 'diswasher_type',
      //   name: '功能-洗碗机',
      //   meta: {
      //     productType: 'diswasher_type',
      //     title: '洗碗机',
      //     access: ['super_admin', 'admin', 'function_diswasher_type']
      //   },
      //   component: () => import('@/view/function/tables - diswasher_type.vue')
      // },
      // {
      //   path: 'disinfection_cabinet_type',
      //   name: '功能-消毒柜',
      //   meta: {
      //     productType: 'disinfection_cabinet_type',
      //     title: '消毒柜',
      //     access: ['super_admin', 'admin', 'function_disinfection_cabinet_type']
      //   },
      //   component: () => import('@/view/function/tables - disinfection_cabinet_type.vue')
      // }
    ]
  },
  // {
  //   path: '/scenario',
  //   name: '场景管理',
  //   component: Main,
  //   meta: {
  //     access: [
  //       'super_admin',
  //       'admin',
  //       'scenario_electric_heater',
  //       'scenario_gas_heater_stove',
  //       'scenario_gas_stove',
  //       'scenario_water_purification',
  //       'scenario_water_drink',
  //       'scenario_rang_hood_type',
  //       'scenario_integrated_gas_combined_kitchen',
  //       'scenario_gas_combined_kitchen',
  //       'scenario_diswasher_type',
  //       'scenario_disinfection_cabinet_type'
  //     ],
  //     title: '场景管理',
  //     icon: 'ios-home'
  //   },
  //   children: [
  //     {
  //       path: 'electric_heater',
  //       name: '场景-电热水器',
  //       meta: {
  //         productType: 'electric_heater',
  //         title: '电热水器',
  //         access: ['super_admin', 'admin', 'scenario_electric_heater']
  //       },
  //       component: () => import('@/view/scenario/tables - electric_heater.vue')
  //     },
  //     {
  //       path: 'gas_heater_stove',
  //       name: '场景-燃气热水器',
  //       meta: {
  //         productType: 'gas_heater_stove',
  //         title: '燃气热水器',
  //         access: ['super_admin', 'admin', 'scenario_gas_heater_stove']
  //       },
  //       component: () => import('@/view/scenario/tables - gas_heater_stove.vue')
  //     },
  //     {
  //       path: 'gas_stove',
  //       name: '场景-燃气炉',
  //       meta: {
  //         productType: 'gas_stove',
  //         title: '燃气炉',
  //         access: ['super_admin', 'admin', 'scenario_gas_stove']
  //       },
  //       component: () => import('@/view/scenario/tables - gas_stove.vue')
  //     },
  //     {
  //       path: 'water_purification',
  //       name: '场景-净水机',
  //       meta: {
  //         productType: 'water_purification',
  //         title: '净水机',
  //         access: ['super_admin', 'admin', 'scenario_water_purification']
  //       },
  //       component: () => import('@/view/scenario/tables - water_purification.vue')
  //     },
  //     {
  //       path: 'water_drink',
  //       name: '场景-饮水机(含净饮机)',
  //       meta: {
  //         productType: 'water_drink',
  //         title: '饮水机(含净饮机)',
  //         access: ['super_admin', 'admin', 'scenario_water_drink']
  //       },
  //       component: () => import('@/view/scenario/tables - water_drink.vue')
  //     },
  //     {
  //       path: 'rang_hood_type',
  //       name: '场景-吸油烟机',
  //       meta: {
  //         productType: 'rang_hood_type',
  //         title: '吸油烟机',
  //         access: ['super_admin', 'admin', 'scenario_rang_hood_type']
  //       },
  //       component: () => import('@/view/scenario/tables - rang_hood_type.vue')
  //     },
  //     {
  //       path: 'integrated_gas_combined_kitchen',
  //       name: '场景-集成灶',
  //       meta: {
  //         productType: 'integrated_gas_combined_kitchen',
  //         title: '集成灶',
  //         access: ['super_admin', 'admin', 'scenario_integrated_gas_combined_kitchen']
  //       },
  //       component: () => import('@/view/scenario/tables - integrated_gas_combined_kitchen.vue')
  //     },
  //     {
  //       path: 'gas_combined_kitchen',
  //       name: '场景-燃气灶(含组合灶)',
  //       meta: {
  //         productType: 'gas_combined_kitchen',
  //         title: '燃气灶(含组合灶)',
  //         access: ['super_admin', 'admin', 'scenario_gas_combined_kitchen']
  //       },
  //       component: () => import('@/view/scenario/tables - gas_combined_kitchen.vue')
  //     },
  //     {
  //       path: 'diswasher_type',
  //       name: '场景-洗碗机',
  //       meta: {
  //         productType: 'diswasher_type',
  //         title: '洗碗机',
  //         access: ['super_admin', 'admin', 'scenario_diswasher_type']
  //       },
  //       component: () => import('@/view/scenario/tables - diswasher_type.vue')
  //     },
  //     {
  //       path: 'disinfection_cabinet_type',
  //       name: '场景-消毒柜',
  //       meta: {
  //         productType: 'disinfection_cabinet_type',
  //         title: '消毒柜',
  //         access: ['super_admin', 'admin', 'scenario_disinfection_cabinet_type']
  //       },
  //       component: () => import('@/view/scenario/tables - disinfection_cabinet_type.vue')
  //     }
  //   ]
  // },
  // {
  //   path: '/sensor',
  //   name: '传感器管理',
  //   component: Main,
  //   meta: {
  //     access: [
  //       'super_admin',
  //       'admin',
  //       'sensor_electric_heater',
  //       'sensor_gas_heater_stove',
  //       'sensor_gas_stove',
  //       'sensor_water_purification',
  //       'sensor_water_drink',
  //       'sensor_rang_hood_type',
  //       'sensor_integrated_gas_combined_kitchen',
  //       'sensor_gas_combined_kitchen',
  //       'sensor_diswasher_type',
  //       'sensor_disinfection_cabinet_type'
  //     ],
  //     title: '传感器管理',
  //     icon: 'ios-thermometer'
  //   },
  //   children: [
  //     {
  //       path: 'electric_heater',
  //       name: '传感器-电热水器',
  //       meta: {
  //         productType: 'electric_heater',
  //         title: '电热水器',
  //         access: ['super_admin', 'admin', 'sensor_electric_heater']
  //       },
  //       component: () => import('@/view/sensor/tables - electric_heater.vue')
  //     },
  //     {
  //       path: 'gas_heater_stove',
  //       name: '传感器-燃气热水器',
  //       meta: {
  //         productType: 'gas_heater_stove',
  //         title: '燃气热水器',
  //         access: ['super_admin', 'admin', 'sensor_gas_heater_stove']
  //       },
  //       component: () => import('@/view/sensor/tables - gas_heater_stove.vue')
  //     },
  //     {
  //       path: 'gas_stove',
  //       name: '传感器-燃气炉',
  //       meta: {
  //         productType: 'gas_stove',
  //         title: '燃气炉',
  //         access: ['super_admin', 'admin', 'sensor_gas_stove']
  //       },
  //       component: () => import('@/view/sensor/tables - gas_stove.vue')
  //     },
  //     {
  //       path: 'water_purification',
  //       name: '传感器-净水机',
  //       meta: {
  //         productType: 'water_purification',
  //         title: '净水机',
  //         access: ['super_admin', 'admin', 'sensor_water_purification']
  //       },
  //       component: () => import('@/view/sensor/tables - water_purification.vue')
  //     },
  //     {
  //       path: 'water_drink',
  //       name: '传感器-饮水机(含净饮机)',
  //       meta: {
  //         productType: 'water_drink',
  //         title: '饮水机(含净饮机)',
  //         access: ['super_admin', 'admin', 'sensor_water_drink']
  //       },
  //       component: () => import('@/view/sensor/tables - water_drink.vue')
  //     },
  //     {
  //       path: 'rang_hood_type',
  //       name: '传感器-吸油烟机',
  //       meta: {
  //         productType: 'rang_hood_type',
  //         title: '吸油烟机',
  //         access: ['super_admin', 'admin', 'sensor_rang_hood_type']
  //       },
  //       component: () => import('@/view/sensor/tables - rang_hood_type.vue')
  //     },
  //     {
  //       path: 'integrated_gas_combined_kitchen',
  //       name: '传感器-集成灶',
  //       meta: {
  //         productType: 'integrated_gas_combined_kitchen',
  //         title: '集成灶',
  //         access: ['super_admin', 'admin', 'sensor_integrated_gas_combined_kitchen']
  //       },
  //       component: () => import('@/view/sensor/tables - integrated_gas_combined_kitchen.vue')
  //     },
  //     {
  //       path: 'gas_combined_kitchen',
  //       name: '传感器-燃气灶(含组合灶)',
  //       meta: {
  //         productType: 'gas_combined_kitchen',
  //         title: '燃气灶(含组合灶)',
  //         access: ['super_admin', 'admin', 'sensor_gas_combined_kitchen']
  //       },
  //       component: () => import('@/view/sensor/tables - gas_combined_kitchen.vue')
  //     },
  //     {
  //       path: 'diswasher_type',
  //       name: '传感器-洗碗机',
  //       meta: {
  //         productType: 'diswasher_type',
  //         title: '洗碗机',
  //         access: ['super_admin', 'admin', 'sensor_diswasher_type']
  //       },
  //       component: () => import('@/view/sensor/tables - diswasher_type.vue')
  //     },
  //     {
  //       path: 'disinfection_cabinet_type',
  //       name: '传感器-消毒柜',
  //       meta: {
  //         productType: 'disinfection_cabinet_type',
  //         title: '消毒柜',
  //         access: ['super_admin', 'admin', 'sensor_disinfection_cabinet_type']
  //       },
  //       component: () => import('@/view/sensor/tables - disinfection_cabinet_type.vue')
  //     }
  //   ]
  // },
  // {
  //   path: '/voiceFunction',
  //   name: '语音功能管理',
  //   component: Main,
  //   meta: {
  //     title: '语音功能',
  //     icon: 'md-mic',
  //     access: ['super_admin', 'admin', 'voice_function']
  //   },
  //   children: [
  //     {
  //       path: '/',
  //       name: '语音功能',
  //       meta: {
  //         title: '语音功能',
  //         icon: 'md-mic',
  //         access: ['super_admin', 'admin', 'voice_function']
  //       },
  //       component: () => import('@/view/voice-function/tables - voice_function.vue')
  //     }
  //   ]
  // },
  // {
  //   path: '/ecologyEntrance',
  //   name: '生态入口管理',
  //   component: Main,
  //   meta: {
  //     title: '生态入口',
  //     icon: 'ios-cloud',
  //     access: ['super_admin', 'admin', 'ecology_entrance']
  //   },
  //   children: [
  //     {
  //       path: '/',
  //       name: '生态入口',
  //       meta: {
  //         title: '生态入口',
  //         icon: 'ios-cloud',
  //         access: ['super_admin', 'admin', 'ecology_entrance']
  //       },
  //       component: () => import('@/view/ecology-entrance/tables - ecology_entrance.vue')
  //     }
  //   ]
  // },
  // {
  //   path: '/branch',
  //   name: '品牌',
  //   component: Main,
  //   meta: {
  //     title: '品牌管理',
  //     icon: 'md-square-outline',
  //     access: ['super_admin', 'admin']
  //   },
  //   children: [
  //     {
  //       path: '/',
  //       name: '品牌管理',
  //       meta: {
  //         title: '品牌管理',
  //         icon: 'md-square-outline',
  //         access: ['super_admin', 'admin']
  //       },
  //       component: () => import('@/view/branch-management/tables-branch.vue')
  //     }
  //   ]
  // },
  {
    path: '/config',
    name: '配置管理',
    component: Main,
    meta: {
      access: ['super_admin', 'admin', 'user_manage'],
      title: '配置管理',
      icon: 'md-contact'
    },
    children: [
      {
        path: 'user',
        name: '用户管理',
        meta: {
          title: '用户管理',
          icon: 'md-contact',
          access: ['super_admin', 'admin', 'user_manage']
        },
        component: () => import('@/view/config-manage/user-manage.vue')
      }
    ]
  },
  {
    path: '/auto',
    name: '自动化',
    component: Main,
    meta: {
      access: ['super_admin', 'admin', 'user_manage'],
      title: '自动化',
      icon: 'md-contact'
    },
    children: [
      {
        path: 'user',
        name: '语言翻译自动化',
        meta: {
          title: '语言翻译自动化',
          icon: 'md-contact',
          access: ['super_admin', 'admin', 'user_manage']
        },
        component: () => import('@/view/auto-script/parseJs2Excel.vue')
      }
    ]
  }
]
