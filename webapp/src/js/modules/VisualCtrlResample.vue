<template>
  <div class="visual-ctrl-opcol">
    <p class="">
      <span class="u-label btn">选择需要筛选的表格:</span>
      <select v-model="selectData">
        <option :value="node.name" v-for="node in cacheNodes">{{node.name}}</option>
      </select>
    </p>
    <p class="u-text">
      <span class="u-label btn">设置维度聚合的基准列:</span>
      <span class="btn btn-default" :class="{active: groupMap[column]}" v-for="column in nodeColumns" @click="addGroupMap(column)">{{column}}</span>
    </p>
    <p class="u-text">
      <span class="u-label btn">设置需要聚合运算的列:</span>
      <span class="f-add" @click="addGroupList">+</span>
      <div class="u-setcol" v-for="(item, index) in methodList">
        <select v-model="item.column" :data-index="index" @change="changeGroupColumn">
          <option :value="column" v-for="column in nodeColumns">{{column}}</option>
        </select>
        <span> 聚合类型:</span>
        <select v-model="item.method" :data-index="index" @change="changeGroupMethod">
          <option :value="method.method" v-for="method in groupMethod">{{method.name}}</option>
        </select>
        <span class="f-del" @click="delRenameList(index)">-</span>
      </div>
    </p>
    <p class="u-text">
      <span class="u-label btn">重采样时间维度:</span>
      <input type="number" v-model="periodNum">
      <select v-model="periodType">
        <option value="M">月</option>
        <option value="D">天</option>
        <option value="H">小时</option>
        <option value="T">分钟</option>
        <option value="S">秒</option>
      </select>
    </p>
    <p class="u-text">
      <span class="u-label btn">输出表格名称:</span>
      <input class="target-tb-name" type="text" v-model="target" placeholder="请输入生成表格名称(重名则覆盖)">
      <button class="btn btn-success" @click="runCommand">开始运算</button>
    </p>
  </div>
</template>

<script>
import groupMethod from 'api/groupMethod'

export default {
  data () {
    return {
      selectData: '',
      groupMethod,
      groupList: [],
      groupMap: {},
      methodList: [],
      target: '',
      periodNum: 1,
      periodType: 'M',
    }
  },
  computed: {
    cacheNodes () {
      return this.$store.state.cacheNodes
    },
    nodeColumns () {
      if (this.selectData) {
        for (let i = 0; i < this.cacheNodes.length; i ++) {
          if (this.cacheNodes[i].name === this.selectData) {
            return this.cacheNodes[i].columns
          }
        }
      }
      return []
    }
  },
  methods: {
    addGroupList () {
      let tmpObj = {
        column: '',
        method: '',
      }
      this.methodList.push(tmpObj)
      this.$forceUpdate()
    },
    delGroupList (index) {
      this.methodList.splice(index, 1)
      this.$forceUpdate()
    },
    addGroupMap (column) {
      if (!this.groupMap[column]) {
        this.groupMap[column] = true
      } else {
        this.groupMap[column] = false
      }
      let groupList = []
      for (let col in this.groupMap) {
        if (this.groupMap[col]) {
          groupList.push(col)
        }
      }
      this.groupList = groupList
      this.$forceUpdate()
    },
    changeGroupColumn () {
      let target = event.target
      let index = parseInt(target.dataset.index)
      this.methodList[index].column = target.value
    },
    changeGroupMethod () {
      let target = event.target
      let index = parseInt(target.dataset.index)
      this.methodList[index].method = target.value
    },
    runCommand () {
      if (/^\s*$/.test(this.selectData)) {
        alert ('请输入操作表格')
        return
      }
      if (/^\s*$/.test(this.target)) {
        alert('请输入生成表格名称')
        return
      }
      let groups = this.groupList.join(' ')
      let methods = []
      for (let i = 0; i < this.methodList.length; i++) {
        let item = this.methodList[i]
        if (/^\s*$/.test(item.column)) {
          alert('请选择需要运算的列名')
          return
        }
        if (/^\s*$/.test(item.method)) {
          alert('请选择需要运算的方法')
          return
        }
        methods.push(`${item.column}|${item.method}`)
      }
      methods = methods.join(' ')

      let command = `resample --src ${this.selectData} --tar ${this.target} --by ${groups} --cols ${methods} --period ${this.periodNum}${this.periodType}`
      this.$store.dispatch('sendMsgs', command)
    }
  }
}
</script>
