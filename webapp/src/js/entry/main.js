import Vue from 'vue'
import VueRouter from 'vue-router'
import App from 'modules/App'
import Shell from 'modules/Shell'
import VisualCtrl from 'modules/VisualCtrl'
Vue.use(VueRouter)

const routes = [
  {
    name: 'datactrl',
    path: '/shell',
    component: Shell
  },
  {
    path: '/visual',
    component: VisualCtrl
  }
]

const router = new VueRouter({
  routes
})
const app = new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
