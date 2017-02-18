import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import createSocketPlugin from 'store/socketPlugin'
const SocketPlugin = createSocketPlugin()

const store = new Vuex.Store({
  state: {
    channel: 0, // 计数消息通道
    cbMap: Object.create(null), // 注册socket消息回调
    shellMsgs: [], // 控制台显示
    cacheCommands: [], // 需要缓存的命令行列表
    cacheNodes: [] // 节点缓存
  },
  mutations: {
    sendMsgs () {
      // 注册事件，调用插件
    },
    receiveData (state, msg) {
      if (msg.type == 'shell') {
        store.commit('pushShellMsgs', msg)
      } else if (msg.type == 'error') {
        store.commit('pushShellMsgs', msg)
      } else if (msg.type == 'cache') {
        store.commit('pushCacheNodes', msg)
      }
    },
    pushCacheCommands (state, msg) {
      state.cacheCommands.push(msg)
    },
    pushShellMsgs (state, msg) {
      if (msg.type == 'shell') {
        state.shellMsgs.push({
          from: 'server',
          msg: msg.data
        })
      } else if (msg.type == 'error') {
        state.shellMsgs.push({
          from: 'error',
          msg: msg.data
        })
      } else if (msg.type == 'user') {
        state.shellMsgs.push({
          from: 'user',
          msg: msg.data
        })
      }
    },
    pushCacheNodes (state, msg) {
      state.cacheNodes = msg.data
    }
  },
  actions: {
    sendMsgs ({ commit, state }, message) {
      state.channel ++
      commit('sendMsgs', message)
      return new Promise ((resolve, reject) => {
        let channel = state.channel
        state.cbMap[channel] = data => {
          resolve(data)
        }
      })
    },
    receiveData ({ commit }, data) {
      commit('receiveData', data)
    },
    pushCacheCommands ({ commit }, data) {
      commit('pushCacheCommands', data)
    },
    pushShellMsgs ({ commit }, data) {
      commit('pushShellMsgs', data)
    }
  },
  getters: {
    // doneTodos: state => {
    //   return state.count
    // }
  },
  plugins: [SocketPlugin]
})

export default store