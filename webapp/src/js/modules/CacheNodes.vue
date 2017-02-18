<template>
  <div>
    <span class="cache" v-for="node in cacheNodes">{{ node.name }}</span>
  </div>
</template>

<script>
export default {
  computed: {
    cacheNodes () {
      return this.$store.state.cacheNodes
    }
  }
}
</script>
