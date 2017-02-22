<template>
  <div class="visual-ctrl-opcol">
    <p class="">
      <span class="u-label btn">选择需要筛选的表格:</span>
      <select v-model="selectData">
        <option :value="node.name" v-for="node in cacheNodes">{{node.name}}</option>
      </select>
    </p>
    <p class="u-text">
      <span class="u-label btn">设置需要计算的列:</span>
      <span>可对列进行加减乘除等基本运算</span>
      <span class="f-add" @click="addSetColList">+</span>
      <div class="u-setcol" v-for="(item, index) in setcolList">
        <p>
          <span class="btn btn-info" v-for="column in nodeColumns" @click="addDstSetColList(column, index)">{{column}}</span>
        </p>
        <input class="dst-col" type="text" :data-index="index" @change="dstSetColList" placeholder="生成列名" v-model="item.dstCol">
        <span> = </span>
        <input class="src-col" type="text" :data-index="index" @change="srcSetColList" placeholder="列运算规则" v-model="item.srcCol">
        <span class="f-del" @click="delSetColList(index)">-</span>
      </div>
    </p>
    <p class="u-text">
      <span class="u-label btn">选择需要输出的表格列:</span>
      <span class="btn btn-default" :class="{active: showColMap[column]}" v-for="column in lastNodeColumn" @click="addShowColMap(column)">{{column}}</span>
    </p>
    <p class="u-text">
      <span class="u-label btn">设置需要重命名的列:</span>
      <span class="f-add" @click="addRenameList">+</span>
      <div class="u-setcol" v-for="(item, index) in renameList">
        <select v-model="item.srcCol" :data-index="index" @change="srcRenameList">
          <option :value="col" v-for="col in leftcolList">{{col}}</option>
        </select>
        <span>重命名为</span>
        <input type="text" :data-index="index" v-model="item.dstCol" @change="dstRenameList">
        <span class="f-del" @click="delRenameList(index)">-</span>
      </div>
    </p>
    <p class="u-text">
      <span class="u-label btn">输出表格名称:</span>
      <input class="target-tb-name" type="text" v-model="target" placeholder="请输入生成表格名称(重名则覆盖)">
      <button class="btn btn-success" @click="runCommand">开始运算</button>
    </p>
  </div>
</template>

<script>
export default {
  data () {
    return {
      selectData: '',
      setcolList: [],
      leftcolList: [],
      renameList: [],
      showColMap: {},
      target: '',
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
    },
    lastNodeColumn () {
      if (this.selectData) {
        let dst = new Set(this.nodeColumns)
        this.setcolList.forEach(item => {
          dst.add(item.dstCol)
        })
        return Array.from(dst)
      }
      return []
    }
  },
  methods: {
    addSetColList () {
      let tmpObj = {
        dstCol: '',
        srcCol: ''
      }
      this.setcolList.push(tmpObj)
      this.$forceUpdate()
    },
    delSetColList (index) {
      this.setcolList.splice(index, 1)
      this.$forceUpdate()
    },
    // setcol 命令目标列
    dstSetColList (event) {
      let target = event.target
      let index = parseInt(target.dataset.index)
      this.setcolList[index].dstCol = target.value
    },
    // setcol 命令操作列
    srcSetColList (event) {
      let target = event.target
      let index = parseInt(target.dataset.index)
      this.setcolList[index].srcCol = target.value
    },
    // 将列添加到输入框中
    addDstSetColList (column, index) {
      this.setcolList[index].srcCol += (' ' + column + ' ')
    },
    addShowColMap (column) {
      if (!this.showColMap[column]) {
        this.showColMap[column] = true
      } else {
        this.showColMap[column] = false
      }
      let leftcolList = []
      for (let col in this.showColMap) {
        if (this.showColMap[col]) {
          leftcolList.push(col)
        }
      }
      this.leftcolList = leftcolList
      this.$forceUpdate()
    },
    addRenameList () {
      let tmpObj = {
        dstCol: '',
        srcCol: ''
      }
      this.renameList.push(tmpObj)
      this.$forceUpdate()
    },
    delRenameList (index) {
      this.renameList.splice(index, 1)
      this.$forceUpdate()
    },
    // rename 命令目标列
    dstRenameList (event) {
      let target = event.target
      let index = parseInt(target.dataset.index)
      this.renameList[index].dstCol = target.value
    },
    // rename 命令操作列
    srcRenameList (event) {
      let target = event.target
      let index = parseInt(target.dataset.index)
      this.renameList[index].srcCol = target.value
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
      let setcolCmds = []
      for (let i = 0; i < this.setcolList.length; i++) {
        let item = this.setcolList[i]
        if (/^\s*$/.test(item.srcCol)) {
          alert('请正确填写处理方法')
          return
        }
        if (/^\s*$/.test(item.dstCol)) {
          alert('输出列名不能为空')
          return
        }
        setcolCmds.push(`${item.dstCol}=${item.srcCol}`)
      }
      let setcol = setcolCmds.join(',')
      if (this.leftcolList.length < 1) {
        alert('请至少选择一个输出列')
        return
      }
      let leftcol = this.leftcolList.join(' ')

      let renameCmds = []
      for (let i = 0; i < this.renameList.length; i++) {
        let item = this.renameList[i]
        if (item.srcCol==='') {
          alert('请输入待重命名的列')
          return
        }
        if (/^\s*$/.test(item.dstCol)) {
          alert('输出列名不能为空')
          return
        }
        renameCmds.push(`${item.srcCol}->${item.dstCol}`)
      }
      let rename = renameCmds.join(',')

      let command = `opcol --src ${this.selectData} --tar ${this.target} --setcol ${setcol} --leftcol ${leftcol} --rename ${rename}`
      this.$store.dispatch('sendMsgs', command)
    }
  }
}
</script>
