import _ from 'lodash'

class SocketUnit {
  constructor (url, hook) {
    url = url || `ws://${window.location.host}/ssh/`
    this.cbMap = Object.create(null)
    this.connection = new WebSocket(url)
    this.channel = 1
    this.init(hook)
  }
  init (hook) {
    const conn = this.connection
    conn.onopen = () => {
      console.info('socket opend')
    }
    conn.onerror = err => {
      console.error(`socket error: ${err}`)
    }
    conn.onmessage = event => {
      // console.log(event.data)
      let data = JSON.parse(event.data)
      if (data.code === 200) {
        if (data.json) {
          console.log(data.json)
        } else if (data.text) {
          console.log(data.text)
        }
      } else {
        console.info(data)
      }
      if (hook instanceof Function) {
        hook(data)
      }
    }
  }
  sendOnce (message) {
    this.channel ++
    let msg = {
      msg: message,
      channel: this.channel
    }
    this.connection.send(JSON.stringify(msg))
    return new Promise ((resolve, reject) => {
      this.cbMap[msg.channel] = data => {
        console.log(data)
        resolve(data)
      }
    })
  }
  send (message, channel) {
    this.channel ++
    channel = channel || this.channel
    let msg = {
      msg: message,
      channel
    }
    this.connection.send(JSON.stringify(msg))
  }
}

// hook为回调钩子
function createSocket (url, hook = null) {
  return new SocketUnit(url, hook)
}
export default createSocket
