import Vue from 'vue'
import VueRouter from 'vue-router'
import store from 'store'
import App from 'modules/App'
import Shell from 'modules/Shell'
import VisualCtrl from 'modules/VisualCtrl'
import Monitor from 'modules/Monitor'
import Operator from 'modules/Operator'
import Uploader from 'modules/Uploader'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Shell
  },
  {
    path: '/shell',
    component: Shell
  },
  {
    path: '/visual',
    component: VisualCtrl
  },
  { // 数据监控
    path: '/monitor',
    component: Monitor
  },
  { // 执行单元自动化脚本配置项
    path: '/operator',
    component: Operator
  },
  { // 上传文件分析
    path: '/uploader',
    component: Uploader
  },
]

const router = new VueRouter({
  routes
})
const app = new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
