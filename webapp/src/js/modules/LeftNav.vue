<template>
  <div>
    <div class="m-presets">
      <h4>系统预置数据</h4>
      <!--li :class="[u-command, {active: item.active}]" v-for="{item, index} in presets" -->
      <li class="u-command" :class="{active: item.active}" v-for="(item, index) in presets" @click="selectCommand(index)">
        <div class="tag">{{item.target}}</div>
        <div class="detail">
          <span class="param" v-for="(param, param_index) in item.params">
            <label :for="param.name">{{param.name}}</label>
            <input :type="param.type" :name="param.name" :data-index="index" :data-param-index="param_index" @change="getParams">
          </span>
          <button class="btn btn-success btn-sm" @click="execCommand(index)">执行</button>
        </div>
      </li>
    </div>
  </div>

</template>

<script>
import axios from 'axios'

export default {
  async mounted () {
    let result = await axios.post('/get_presets', {test: 1})
    if (result.status === 200) {
      let data = result.data
      // 预制数据脚本
      if (data.presets) {
        data.presets.forEach( content => {
          let target = content.name
          let source = content.file.replace(/\.data$/, '')
          let params = content.params
          params = params.map(item => {
            if (typeof item === 'string') {
              return {
                name: item,
                type: 'text',
                value: ''
              }
            } else if (Array.isArray(item)) {
              return {
                name: item[0],
                type: item[1],
                value: ''
              }
            }
          })
          this.presets.push({
            source,
            target,
            params,
            active: false
          })
        })
      }
    }
  },
  data () {
    return {
      current: 0,
      presets: []
    }
  },
  methods: {
    selectCommand (index = 0) {
      this.presets.forEach(item => {
        item.active = false
      })
      this.presets[index].active = true
    },
    execCommand (index = 0, type = 'presets') {
      let setItem = null
      index = parseInt(index)
      if (type === 'presets') {
        setItem = this.presets[index]
      }
      let source = setItem.source
      let target = setItem.target
      let params = ''
      let paramsList = []
      setItem.params.forEach(item => {
        if (item.value != '') {
          paramsList.push(`${item.name}=${item.value}`)
        }
      })
      if (paramsList.length > 0) {
        params = paramsList.join(', ')
        params = `--params ${params}`
      }
      let message = `execunit --src ${source} --tar ${target} ${params}`
      this.$store.dispatch('sendMsgs', message)
    },
    getParams (event) {
      let target = event.target
      let index = parseInt(target.dataset.index)
      let paramIndex = parseInt(target.dataset.paramIndex)
      let value = target.value
      this.presets[index].params[paramIndex].value = value
    }
  }
}
</script>
