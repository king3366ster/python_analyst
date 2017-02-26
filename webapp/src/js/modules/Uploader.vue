<template>
  <div class="visual-ctrl-opcol">
    <h3>上传文件分析</h3>
    <p class="u-text">
      <span class="u-label btn">上传分析文件</span>
      <form enctype="multipart/form-data">
        <input class="btn btn-default nav-inline" type="file" name="uploader">
        <input class="btn btn-success nav-inline" type="button" value="提交">
      </form>
    </p>
  </div>
</template>

<script>

export default {
  data () {
    return {
      selectData: '',
    }
  },
  computed: {
    cacheNodes () {
      return this.$store.state.cacheNodes
    },
  },
  methods: {
    
  }
}
</script>
