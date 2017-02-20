import store from 'store'
export default {
  sendMsgs () {
    // 注册事件，调用插件
    // 消息格式：
    // {	type, message, channel}
  },
  receiveData (state, msg) {
    if (msg.type === 'shell') {
      store.commit('pushShellMsgs', msg)
    } else if (msg.type === 'error') {
      store.commit('pushShellMsgs', msg)
    } else if (msg.type === 'cache') {
      store.commit('pushCacheNodes', msg)
    } else if (msg.type === 'data') {
      store.commit('updateData', msg.data)
    } else if (msg.type == 'filend') {
      let target = msg.data.target
      state.fileLinks.forEach(item => {
        if (item.name === target) {
          item.status = 'succeed'
        }
      })
    }
  },
  // 缓存命令行
  pushCacheCommands (state, msg) {
    state.cacheCommands.push(msg)
  },
  // 控制台显示
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
  },
  changeCurrentNode (state, msg) {
    state.currentNode = msg
  },
  pullData (state, {offset=0, limit=0, order=''}) {
    if (limit === 0) {
      limit = state.pageLimit
    }
    let cacheNode = state.currentNode
    if (cacheNode) {
      store.commit('sendMsgs', {
        type: 'data',
        message: `pulldata --src ${cacheNode} --limit ${offset}, ${limit} ${order}`
      })
    }
  },
  updateData (state, msg) {
    state.currentData = msg.data
    state.currentDataTotal = msg.total
  },
  saveExcel (state, msg) {
    let source = state.currentNode
    if (source) {
      let randnum = Math.round(Date.parse(new Date()) % 10000000000 / 100)
      let target = `${source}_${randnum}`
      store.commit('sendMsgs', {
        type: 'command',
        message: `saveexcel --src ${source} --tar ${target}`
      })
      state.fileLinks.push({
        name: target,
        time: new Date(),
        status: 'pending'
      })
    }
  }
}
