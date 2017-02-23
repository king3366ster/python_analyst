export default {
  sendMsgs ({ commit, state }, message) {
    message.split('\n').forEach(item => {
      commit('pushShellMsgs', {
        type: 'user',
        data: item
      })
    })
    commit('pushCacheCommands', message)
    state.channel ++
    commit('sendMsgs', {
      message,
      type: 'shell'
    })
    return new Promise ((resolve, reject) => {
      let channel = state.channel
      state.cbMap[channel] = data => {
        resolve(data)
      }
    })
  },
  cleanMsgs ({ commit }) {
    commit('cleanMsgs')
  },
  receiveData ({ commit }, data) {
    commit('receiveData', data)
  },
  changeCurrentNode ({ commit }, data) {
    commit('changeCurrentNode', data)
  },
  pullData ({ commit }, data) {
    commit('pullData', data)
  },
  saveFile ({ commit }, data) {
    commit('saveFile', data)
  },
}
