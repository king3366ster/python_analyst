const wsUrl = `ws://${window.location.host}/ana/`

export default function createSocketPlugin () {
  const socket = new WebSocket(wsUrl)

  return store => {
    socket.onopen = () => {
      console.info('socket opend')
    }
    socket.onerror = err => {
      console.error(`socket error: ${err}`)
    }
    socket.onmessage = ({data}) => {
      try {
        data = JSON.parse(data)
      } catch (err) {
        console.error(`message error: ${err}`)
        console.info(event.data)
      }
      if (data.code === 200 || data.code === 101) {
        let cbChannel = data.channel
        if (store.state.cbMap[cbChannel]) {
          store.state.cbMap[cbChannel](data.data)
        }
      } else {
        console.error(data)
      }
      store.dispatch('receiveData', data)
    }
    store.subscribe( mutation => {
      if (mutation.type === 'sendMsgs') {
        let channel = store.state.channel
        let msg = {channel, ...mutation.payload}
        socket.send(JSON.stringify(msg))
      }
    })
  }
}