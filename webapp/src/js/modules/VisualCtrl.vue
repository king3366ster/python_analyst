<template>
  <div class="visual-ctrl">
    <div class="m-nav">
      <button class="btn btn-sm" :class="{'btn-success': ctrlType=='merge'}" @click="changeCtrlType('merge')">数据表合并</button>
      <button class="btn btn-sm" :class="{'btn-success': ctrlType=='filter'}" @click="changeCtrlType('filter')">数据行筛选</button>
      <button class="btn btn-sm" :class="{'btn-success': ctrlType=='opcol'}" @click="changeCtrlType('opcol')">数据列运算</button>
      <button class="btn btn-sm" :class="{'btn-success': ctrlType=='group'}" @click="changeCtrlType('group')">数据聚合(group by)</button>
      <button class="btn btn-sm" :class="{'btn-success': ctrlType=='resample'}" @click="changeCtrlType('resample')">时间维度采样分析</button>
    </div>
    <div class="m-view">
      <ctrl-merge v-if="ctrlType=='merge'"></ctrl-merge>
      <ctrl-filter v-if="ctrlType=='filter'"></ctrl-filter>
      <ctrl-opcol v-if="ctrlType=='opcol'"></ctrl-opcol>
      <ctrl-resample v-if="ctrlType=='resample'"></ctrl-resample>
      <ctrl-group v-if="ctrlType=='group'"></ctrl-group>
    </div>
  </div>
</template>

<script>
import VisualCtrlFilter from 'modules/VisualCtrlFilter'
import VisualCtrlMerge from 'modules/VisualCtrlMerge'
import VisualCtrlOpcol from 'modules/VisualCtrlOpcol'
import VisualCtrlGroup from 'modules/VisualCtrlGroup'
import VisualCtrlResample from 'modules/VisualCtrlResample'

export default {
  data () {
    return {
      ctrlType: 'merge', // merge/group/resample/filter
    }
  },
  methods: {
    changeCtrlType (ctrlType) {
      this.ctrlType = ctrlType
    }
  },
  components: {
    'ctrlFilter': VisualCtrlFilter,
    'ctrlMerge': VisualCtrlMerge,
    'ctrlOpcol': VisualCtrlOpcol,
    'ctrlGroup': VisualCtrlGroup,
    'ctrlResample': VisualCtrlResample,
  }
}
</script>
