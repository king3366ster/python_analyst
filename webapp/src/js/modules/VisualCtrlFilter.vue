<template>
  <div class="visual-ctrl-filter">
    <p class="">
      <span class="u-label btn">选择需要筛选的表格:</span>
      <select v-model="selectData">
        <option :value="node.name" v-for="node in cacheNodes">{{node.name}}</option>
      </select>
    </p>
    <p class="u-text">
      <span class="u-label btn">填写筛选条件: (筛选条件格式为 &lt;列名>&lt;比较>&lt;数值>)</span>
      <p class="u-line"><strong>比较操作符：</strong> >、>=、==、&gt;=、&gt;、!=、~= 。&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>条件操作符：</strong>&amp; 代表与; | 代表或。 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>优先级操作符：</strong>(、)</p>
      <p class="u-line">比较操作符中 ~= 表示正则匹配，比如： ColA ~= "[A-Za-z]+"。 字符类型比较需要加双引号" </p>
      <p class="u-line">例子：(HIS&lt;"2017-12-12") &amp; ((cid!=4) | (C~="^pc"))</p>
    </p>
    <p class="u-text">
      <span class="u-label btn">点击需要筛选的表格列:</span>
      <span class="btn btn-info" v-for="column in nodeColumns" @click="addCondition(column)">{{column}}</span>
      <textarea name="name" rows="8" cols="80" v-model="condData"></textarea>
    </p>
    <p class="u-text">
      <span class="u-label btn">对表格进行排序</span>
      <select v-model="orderData">
        <option :value="column" v-for="column in nodeColumns">{{column}}</option>
      </select>
      <select v-model="orderType">
        <option value="">不排序</option>
        <option value="asc">升序</option>
        <option value="asc">降序</option>
      </select>
    </p>
    <p class="u-text">
      <span class="u-label btn">输出表格名称:</span>
      <input class="target-tb-name" type="text" v-model="target" placeholder="请输入生成表格名称(重名则覆盖)">
      <button class="btn btn-success" @click="runCommand">开始筛选</button>
    </p>
  </div>
</template>

<script>
export default {
  data () {
    return {
      selectData: '',
      condData: '',
      orderData: '',
      orderType: '',
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
    }
  },
  methods: {
    addCondition (column) {
      this.condData = `${this.condData} ${column} `
      this.$forceUpdate()
    },
    runCommand () {
      if (/^\s*$/.test(this.condData) && (this.orderType === '')) {
        alert ('请输入筛选条件或排序规则')
        return
      }
      if (/^\s*$/.test(this.target)) {
        alert('请输入生成表格名称')
        return
      }
      let condition = ''
      if (!(/^\s*$/.test(this.condData))) {
        condition = `--cond ${this.condData}`
      }
      let order = ''
      if (this.orderType && this.orderData) {
        order = `--sort ${this.orderData} ${this.orderType}`
      }
      let command = `filter --src ${this.selectData} --tar ${this.target} ${condition} ${order}`
      this.$store.dispatch('sendMsgs', command)
    }
  }
}
</script>
