<template>
  <div>
    <hr class="process-bar" :style="{width:processStatus+'%'}">
    <span class="btn">已生成表格：</span>
    <span class="cache" :class="{active: currentNode==node.name}" v-for="node in cacheNodes" @click="changeCurrentNode(node.name)">{{ node.name }}</span>
    <hr>
  </div>
</template>

<script>
export default {
  data () {
    return {
    }
  },
  computed: {
    cacheNodes () {
      return this.$store.state.cacheNodes
    },
    currentNode () {
      return this.$store.state.currentNode
    },
    processStatus () {
      let status = Math.max(this.$store.state.processStatus, 0.01)
      return status * 100
    }
  },
  methods: {
    changeCurrentNode (nodeName) {
      this.$store.dispatch('changeCurrentNode', nodeName)
      this.$store.dispatch('pullData', {})
    }
  }
}
</script>
