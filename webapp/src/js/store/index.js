import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import mutations from 'store/mutations'
import actions from 'store/actions'
import createSocketPlugin from 'store/socketPlugin'
const SocketPlugin = createSocketPlugin()

const store = new Vuex.Store({
  state: {
    channel: 0, // 计数消息通道 socket
    cbMap: Object.create(null), // 注册socket消息回调
    shellMsgs: [], // 控制台显示消息
    processStatus: 0, // 进度控制状态
    cacheCommands: [], // 需要缓存的命令行列表
    cacheNodes: [], // 节点缓存
    fileLinks: [], // 可供下载的文件列表
    currentNode: null, // 当前数据处理节点
    currentData: null,  // 当前展示数据流
    currentDataTotal: 0, // 当前数据总数
    pageLimit: 10, // 每页展示数量
  },
  mutations,
  actions,
  getters: {
    // doneTodos: state => {
    //   return state.count
    // }
  },
  plugins: [SocketPlugin]
})

export default store
