<template>
  <div class="m-shell">
    <div class="m-blackboard">

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
    this.socket = createSocket()
  },
  data () {
    return {
      commands: ''
    }
  },
  methods: {
    sendCommands () {
      this.socket.send(this.commands)
      console.log(this.commands)
    }
  }
}
</script>
