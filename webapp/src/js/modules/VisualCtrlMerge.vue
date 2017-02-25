<template>
  <div class="visual-ctrl-merge">
    <p class="">
      <span class="u-label btn">选择需要合并的表格:</span>
      <select v-model="select1" @change="updateSelect">
        <option :value="node.name" v-for="node in cacheNodes">{{node.name}}</option>
      </select>
      <select v-model="joinType">
        <option value="inner">内联结</option>
        <option value="outer">外联结</option>
        <option value="left">左联结</option>
        <option value="right">右联结</option>
      </select>
      <select v-model="select2" @change="updateSelect">
        <option :value="node.name" v-for="node in cacheNodes">{{node.name}}</option>
      </select>
    </p>
    <p class="">
      <span class="u-label btn">选择需要合并的表格列:</span>
      <span class="btn btn-default" :class="{active: joinMap[column]}" v-for="column in joinColumns" @click="addJoinSet(column)">{{column}}</span>
    </p>
    <p class="">
      <span class="u-label btn">输出表格名称:</span>
      <input class="target-tb-name" type="text" v-model="target" placeholder="请输入生成表格名称(重名则覆盖)">
      <button class="btn btn-success" @click="runCommand">开始合并</button>
    </p>
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  data () {
    return {
      select1: '',
      select2: '',
      columnList: [],
      joinMap: Object.create(null),
      joinType: 'inner',
      target: '',
    }
  },
  computed: {
    cacheNodes () {
      return this.$store.state.cacheNodes
    },
    joinColumns () { // 数据重合的列
      let cacheNodes = this.$store.state.cacheNodes
      let setList = []
      if (cacheNodes.length < 2) {
        return []
      }
      let colSet1 = []
      let colSet2 = []
      cacheNodes.forEach(item => {
        if (item.name === this.select1) {
          item.columns.forEach(column => {
            colSet1.push(column)
          })
        }
        if (item.name === this.select2) {
          item.columns.forEach(column => {
            colSet2.push(column)
          })
        }
      })
      // let interSet = [...colSet1].filter(v => colSet2.has(v))
      // return interSet
      //
      return _.intersection(colSet1, colSet2)
    },
  },
  methods: {
    runCommand () {
      if (this.select1 === '' || this.select2 === '') {
        alert('请选择待合并表格')
        return
      } else if (this.select1 === this.select2) {
        alert('两张合并的表格不能相同')
        return
      } else if (/^\s*$/.test(this.target)) {
        alert('请输入生成表格名称')
        return
      }
      let columns = []
      for (let column in this.joinMap) {
        columns.push(column)
      }
      columns = columns.join(' ')
      let command = `merge --src ${this.select1} ${this.select2} --tar ${this.target} --join ${this.joinType} ${columns}`
      this.$store.dispatch('sendMsgs', command)
    },
    addJoinSet (column) {
      if (!this.joinMap[column]) {
        this.joinMap[column] = true
      } else {
        this.joinMap[column] = false
      }
      this.$forceUpdate()
    },
    updateSelect () {
      this.joinMap = {}
      this.joinColumns.forEach(item => {
        this.joinMap[item] = true
      })
      this.$forceUpdate()
    }
  }
}
</script>
