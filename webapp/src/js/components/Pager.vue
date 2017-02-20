<template>
  <ul class="my-pagination" >
    <li v-show="current != 1" @click="current-- && goto(current)" ><span>上一页</span></li>
    <li v-for="index in pages" @click="goto(index)" :class="{'active':current == index}" :key="index">
      <span>{{index}}</span>
    </li>
    <li v-show="pageTotal != current && pageTotal != 0 " @click="current++ && goto(current++)"><span>下一页</span></li>
    <li>
      <input type="number" name="" v-model="tempCurrent">
    </li>
    <li>
      <span @click="goto(tempCurrent)">Go!</span>
    </li>
    <li> 共 {{total}} 条数据，第 {{current}} 页，共 {{pageTotal }} 页</li>
  </ul>
</template>

<style>
  .my-pagination {
    position: relative;
    margin: 10px auto;
    text-align: center;
    li {
      display: inline-block;
      margin: 0 5px;
      vertical-align: middle;
      span {
        cursor: pointer;
      }
      span, input {
        padding: .5rem 1rem;
        display: inline-block;
        max-width: 100px;
        border: 1px solid #ddd;
        background: #fff;
        color: #0E90D2;
      }
      span:hover {
        background: #E6F9FF;
      }
      &.active {
        span {
          background: #DBFFDB;
        }
      }
    }
  }
</style>

<script>

export default {
  name: 'pager',
  props: ['pageLimit', 'total', 'pageAction'],
  data: function(){
    return{
      current: 1,
      tempCurrent: 1
    }
  },
  computed:{
    pageTotal () {
      return Math.ceil(this.total / this.pageLimit)
    },
    pages () {
      var pag = [];
      if ( this.current < this.pageLimit ) { //如果当前的激活的项 小于要显示的条数
        //总页数和要显示的条数那个大就显示多少条
        let i = Math.min(this.pageLimit, this.pageTotal)
        while (i) {
          pag.unshift(i--);
        }
      } else { //当前页数大于显示页数了
        let middle = this.current - Math.floor(this.pageLimit / 2 ) // 从哪里开始
        let i = this.pageLimit;
        if ( middle > (this.pageTotal - this.pageLimit)) {
          middle = (this.pageTotal - this.pageLimit) + 1
        }
        while(i--){
          pag.push( middle++ );
        }
      }
      return pag
    }
  },
  methods:{
    goto (index) {
      index = parseInt(index)
      if (index == this.current) return
      this.current = index;
      // let offset = Math.max(index - 1, 0) * this.pageLimit
      this.$emit('goto', index)
    }
  }
}
</script>
