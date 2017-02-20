<template>
  <div class="m-chart-view">
    <div class="m-nav">
      <button class="btn" :class="{'btn-info': chartType=='table'}" @click="changeChartType('table')">表格展示</button>
      <button class="btn" :class="{'btn-info': chartType=='chart'}" @click="changeChartType('chart')">图形展示</button>
      <button class="btn btn-success" @click="saveExcel()">生成EXCEL</button>
    </div>
    <div class="m-view">
      <data-table v-show="chartType=='table'"></data-table>
      <data-chart v-show="chartType=='chart'"></data-chart>
    </div>
    <div class="m-file">
      <h4>下载文件列表</h4>
      <div class="" v-for="file in fileLinks">
        <a v-if="file.status=='succeed'" :href="'/static/' + file.name + '.xlsx'" target="_blank">
          <span class="btn btn-success btn-sm">{{file.name}}</span>
        </a>
        <span v-else="file.status=='pending'" class="btn btn-warning btn-sm">文件生成中...</span>
        </span>
        <!-- <span>{{file.time}}</span> -->
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'modules/Chart'
import Table from 'modules/Table'

export default {
  data () {
    return {
      chartType: 'table'
    }
  },
  computed: {
    fileLinks () {
      return this.$store.state.fileLinks
    }
  },
  methods: {
    changeChartType (chartType) {
      this.chartType = chartType
    },
    saveExcel () {
      this.$store.dispatch('saveFile', 'excel')
    }
  },
  components: {
    'data-chart': Chart,
    'data-table': Table
  }
}
</script>
