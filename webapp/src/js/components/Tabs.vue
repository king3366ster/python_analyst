<template>
  <div>
    <div class="m-nav">
      <button type="button" name="button">表格</button>
      <button type="button" name="button">图形</button>
    </div>
    <div class="m-view">
      
    </div>
  </div>
</template>

<script>
import Chart from 'modules/Chart'
import Table from 'modules/Table'

export default {
  props: []
  data () {
    return {
      msg: 'Info'
    }
  },
  components: {
    'data-chart': Chart,
    'data-table': Table
  }
}
</script>
