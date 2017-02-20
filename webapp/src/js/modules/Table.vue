<template>
  <div class="m-table">
    <h3>表格数据展示 {{title}}</h3>
    <div class="u-table" v-if="tableData">
      <table>
        <thead>
          <tr>
            <td></td>
            <td v-for="column in tableData.columns">{{column}}</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in tableData.rows">
            <td>{{tableData.indexs[index]}}</td>
            <td v-for="column in tableData.columns">{{item[column]}}</td>
          </tr>
        </tbody>
      </table>
      <pager
        :total="dataTotal"
        :page-limit="pageLimit"
        v-on:goto="pullData"
      ></pager>
    </div>
    <div v-else>
      <h4>暂无数据</h4>
    </div>
  </div>
</template>

<script>
import pager from 'components/Pager'
export default {
  data () {
    return {
    }
  },
  computed: {
    pageLimit () {
      return this.$store.state.pageLimit
    },
    title () {
      return this.$store.state.currentNode
    },
    tableData () {
      let data = this.$store.state.currentData
      if (data) {
        let columns = Object.keys(data)
        let indexMap = Object.create(null)
        columns.forEach(column => {
          let dataCol = data[column]
          for (let index in dataCol) {
            if (!indexMap[index]) {
              indexMap[index] = {}
            }
            indexMap[index][column] = dataCol[index]
          }
        })
        let rows = []
        for (let index in indexMap) {
          rows.push(indexMap[index])
        }
        let indexs = Object.keys(indexMap)
        indexs = indexs.map(item => parseInt(item))
        indexs.sort((a, b) => {
          return parseInt(a) - parseInt(b)
        })
        return {
          columns,
          indexs,
          rows
        }
      } else {
        return null
      }
    },
    dataTotal () {
      return this.$store.state.currentDataTotal
    }
  },
  components: {
    'pager': pager
  },
  methods: {
    pullData (pageId) {
      let offset = Math.max(pageId - 1, 0) * this.pageLimit
      this.$store.dispatch('pullData', {
        offset,
        limit: this.pageLimit
      })
    }
  }
}
</script>
