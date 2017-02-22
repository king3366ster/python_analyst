import Vue from 'vue'
import VueRouter from 'vue-router'
import store from 'store'
import App from 'modules/App'
import Shell from 'modules/Shell'
import VisualCtrl from 'modules/VisualCtrl'
import Monitor from 'modules/Monitor'
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
  {
    path: '/monitor',
    component: Monitor
  }
]

const router = new VueRouter({
  routes
})
const app = new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
