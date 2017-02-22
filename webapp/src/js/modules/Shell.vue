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

export default {
  data () {
    return {
      shellMsg: [],
      commands: ''
    }
  },
  computed: {
    shellMsgs () {
      return this.$store.state.shellMsgs
    }
  },
  methods: {
    sendCommands () {
      this.$store.dispatch('sendMsgs', this.commands)
    }
  }
}
</script>
