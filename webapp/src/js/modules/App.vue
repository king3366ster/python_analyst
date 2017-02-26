<template>
  <div class="app">
    <div class="m-nav-l">
      <left-nav></left-nav>
    </div><div class="m-ctrl">
      <nav class="m-nav nav nav-inline">
        <router-link to="/shell">
          <button role="presentation" class="nav-link btn btn-default">命令行操作</button>
        </router-link>
        <router-link to="/visual">
          <button role="presentation" class="nav-link btn btn-default">可视化操作</button>
        </router-link>
        <router-link to="/monitor">
          <button role="presentation" class="nav-link btn btn-default">数据监控</button>
        </router-link>
        <router-link to="/operator">
          <button role="presentation" class="nav-link btn btn-default">自动化脚本</button>
        </router-link>
        <router-link to="/uploader">
          <button role="presentation" class="nav-link btn btn-default">上传文件分析</button>
        </router-link>
      </nav>
      <div class="m-view">
        <router-view></router-view>
      </div>
    </div><div class="m-nodes">
      <cache-nodes></cache-nodes>
    </div><div class="m-chartview">
      <chart-view></chart-view>
    </div>
  </div>
</template>

<script>

import LeftNav from 'modules/LeftNav'
import CacheNodes from 'modules/CacheNodes'
import ChartView from 'modules/ChartView'

export default {
  data () {
    return {
      msg: 'Info'
    }
  },
  components: {
    'left-nav': LeftNav,
    'cache-nodes': CacheNodes,
    'chart-view': ChartView
  }
}
</script>
