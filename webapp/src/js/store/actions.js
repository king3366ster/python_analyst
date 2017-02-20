export default {
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
  },
  changeCurrentNode ({ commit }, data) {
    commit('changeCurrentNode', data)
  },
  pullData ({ commit }, data) {
    commit('pullData', data)
  },
  saveFile ({ commit }, data) {
    if (data === 'excel') {
      commit('saveExcel', data)
    }
  },
}
