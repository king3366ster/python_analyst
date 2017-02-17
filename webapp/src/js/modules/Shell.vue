<template>
  <div class="m-shell">
    <div class="m-blackboard">
      <li v-for="msg in shellMsgs" :class="{user: msg.from=='user', server: msg.from=='server', error: msg.from=='error'}">{{ msg.msg }}</li>
    </div>
    <div class="m-inputbar">
      <h4>命令控制台</h4>
      <textarea name="name" rows="8" cols="100" @keyup.ctrl.enter="sendCommands" v-model="commands"></textarea>
      <p>
        <button @click.stop="sendCommands" class="btn btn-success">发送消息</button>
        <button class="btn btn-warning">清空消息</button>
        <span class="info">按Ctrl+Enter发送消息</span>
      </p>
    </div>
  </div>
</template>

<script>
import createSocket from 'api/socketUtil'

export default {
  mounted () {
    this.socket = createSocket(this.msgReceived)
  },
  data () {
    return {
      commands: '',
      shellMsgs: [],
    }
  },
  methods: {
    async sendCommands () {
      let sentMsgs = this.commands.split('\n').map(item => {
        return {
          from: 'user',
          msg: item
        }
      })
      this.shellMsgs = this.shellMsgs.concat(sentMsgs)
      this.socket.send(this.commands)
      // let res = await this.socket.sendOnce(this.commands)

      // console.log(res)
    },
    msgReceived (msg) {
      if (msg.type == 'shell') {
        this.shellMsgs.push({
          from: 'server',
          msg: msg.data
        })
      } else if (msg.type == 'error') {
        this.shellMsgs.push({
          from: 'error',
          msg: msg.data
        })
      }
    }
  }
}
</script>
