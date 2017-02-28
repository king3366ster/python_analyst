<template>
  <div class="m-mainbox">
    <h3>Shell操作及脚本配置常用命令行</h3>
    <h4>获取数据源类</h4>
    <ol>
      <li>
        <h5>获取预置数据(execunit)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>execunit --src 缓存节点 --tar 生成节点 --params 参数1=a, 参数2=b ...</li>
              <li>execunit --src 内存表名 --tar 新表名</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 在内存中的对象键值，可通过后台配置或前台自定义配置</li>
              <li>--tar: 处理完成后的数据输出表名</li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>获取Mysql数据(loadmysql)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>loadmysql --db localdb --tar msdata --query select * from tb_new limit 20</li>
              <li>loadmysql --db testdb --tar 分析 --query select id, count(corp) as "企业数", sum(cost) as "消耗" from tb_new group by id</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--db: 后台已配置的数据库配置信息</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--query: SQL命令行</li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>获取Excel数据(loadexcel)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>loadexcel --tar dataframe --src source --sheet Sheet1</li>
              <li>loadexcel --tar 生成表名 --src source</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 上传的excel文件名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--sheet: excel表名，默认为Sheet1</li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>获取CSV数据(loadcsv)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>loadcsv --tar dataframe --src source --sheet Sheet1</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 上传的excel文件名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
            </ul>
          </li>
        </ul>
      </li>
    </ol>
    <h4>多数据合并类</h4>
    <ol>
      <li>
        <h5>按列做匹配合并(merge)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>merge --tar dest --src src1 src2 --join left cid aid</li>
              <li>merge --tar dest --src src1 src2 --join inner aid</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--join: 连接方式，第一个字段为连接方面，后面为连接列名，空格分隔</li>
              <li>--join: 连接方式包括left/right/inner/outer</li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>非匹配合并(concat)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>concat --tar dest --src src1 src2 --join inner --axis 0</li>
              <li>concat --tar dest --src src1 src2 --join outer --axis 1</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--join: 连接方式，inner/outer，会自动去重</li>
              <li>--axis: 合并方向：0 纵向合并 1 横向合并</li>
            </ul>
          </li>
        </ul>
      </li>
    </ol>
    <h4>数据筛选操作类</h4>
    <ol>
      <li>
        <h5>数据按行筛选(filter)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>filter --src excdata --tar dst1 --cond (HIS&lt;"2017-12-12") &amp; (G!=4) &amp; (C~="^pc")</li>
              <li>filter --src excdata --tar dst1 --sort A asc, G desc --limit 3,4</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--cond 比较操作命令，列名放在操作符前，程序会自动解析
                <ul>
                  <b>- 运算操作符 &lt; &lt;= == >= > != ~=</b>
                  <li>- ~= 操作符表示正则匹配 如 A ~= "^P+"</li>
                  <li>- 字符类型的比较务必加上引号 如 A == ""</li>
                </ul>
                <ul>
                  <b>- 比较操作符 &amp; |</b>
                  <li>- &amp; 与操作 | 或操作</li>
                </ul>
                <ul>
                  <b>- 优先操作符 ( )</b>
                </ul>
              </li>
              <li>--sort 排序，执行顺序晚于cond
                <ul>
                  <b>方法使用： <列名><排序方式> 以逗号(,)分隔</b>
                  <li>排序方式：asc|desc 不填默认升序</li>
                  <li>排序优先级依命令顺序</li>
                </ul>
              </li>
              <li>--cols 选取特定的列</li>
              <li>--limit 获取特定行 以逗号(,)分隔
                <ul>
                  <li>一个参数时(--limit num)等同于 offset 0 limit num</li>
                  <li>两个参数时(--limit num1, num2)等同于 offset num1 limit num2</li>
                  <li>超过两个参数，只取前两个参数</li>
                </ul>
              </li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>数据按列操作(opcol)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>opcol --src excdata --tar dst2 --setcol M1=A+B, HI = HIS, T3 = HIS-T2, T3->time</li>
              <li>opcol --src excdata --tar dst2 --setcol HI = HIS --dropcol HIS --leftcol A B C G --rename B -> 测试, C-> 公平</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--setcol 设置列 如 A=B-C, B=1, D->int/time/str/float
                <ul>
                  <b>=为运算操作符</b>
                  <li>A = B+1 表示A列为B列的值加一</li>
                  <li>D -> time 表示将D列转化为时间类型</li>
                </ul>
              </li>
              <li>--dropcol 删除列</li>
              <li>--leftcol 剩余列</li>
              <li>--rename 重命名列 逗号分隔</li>
              <li>--cols 选取特定的列</li>
              <li>任何一条opcol命令执行顺序为 setcol -> dropcol -> leftcol -> rename 可多选少选（!请注意顺序）</li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>空值操作(opnull)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>opnull --src excdata --tar dst2 --setval 3.2</li>
              <li>opnull --src excdata --tar dst2 --setval </li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--setval 对空值的填充内容</li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>JSON字段解析(parsejson)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>parsejson --tar dest --src src1 --cols col1.key1.subkey1 col2.key2</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--cols 需要解析json字段的列及属性 如col1.key1，第一个为列名，第二个值为对应列第一个要解析的json key，第三个值为第二个要解析的json key,依次类推</li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>数据全局替换(replace)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>replace --tar dest --src src1 --setval 0->null 3->"as"</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--setval 将特定数值进行替换</li>
            </ul>
          </li>
        </ul>
      </li>
    </ol>
    <h4>数据聚合分析类</h4>
    <ol>
      <li>
        <h5>按组聚合(group)--类似于mysql的group by</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>group --tar dest --src src1 --by cola --cols col1|sum col2|mean</li>
              <li>group --tar dest --src src1 --by col1 col2 --cols col3 col4|top3</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--by 进行groupby的键值，可多选</li>
              <li>--cols (列名)|(聚合方法)
                <ul>
                  <b>目前支持方法</b>
                  <li>sum/mean/count/std/var/min/max/top/last/topN</li>
                  <li>top(N): top2 top3 ... ；top1等同于top</li>
                  <li>新生成列自动加下划线+方法命名，如A|sum 生成列名为A_sum</li>
                  <li>可使用opcol --rename进行重命名</li>
                </ul>
              </li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>时间序列重采样(resample)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>resample --src excdata --tar dst1  --by HIS --cols G|sum H|mean --period 3d</li>
              <li>resample --src excdata --tar dst1  --by HIS --cols G|sum H|mean --period 2M</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--by 进行重采样的键值，必须为时间类型</li>
              <li>--cols (列名)|(聚合方法)
                <ul>
                  <b>目前支持方法</b>
                  <li>sum/mean/count/std/var/min/max/top/last/topN</li>
                  <li>top(N): top2 top3 ... ；top1等同于top</li>
                  <li>新生成列自动加下划线+方法命名，如A|sum 生成列名为A_sum</li>
                  <li>可使用opcol --rename进行重命名</li>
                </ul>
              </li>
              <li>--period 采样周期 M 月、 D 天、 H 小时、 T 分钟、 S 秒，3D即表示以3天为周期</li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        <h5>获取特定标签顶部的N行(topnrows)</h5>
        <ul>
          <li>
            <strong>示例：</strong>
            <ul>
              <li>topnrows --src excdata --tar dst1 --by C --num 3</li>
            </ul>
          </li>
          <li>
            <strong>参数： </strong>
            <ul>
              <li>--src: 已执行完成的内存表名</li>
              <li>--tar: 处理完成后的数据输出表名</li>
              <li>--by 作为聚合基准的键值</li>
              <li>--num 获取顶部的行数</li>
            </ul>
          </li>
        </ul>
      </li>
    </ol>
  </div>
</template>

<script>
export default {
  data () {
    return {
      msg: 'Info'
    }
  }
}
</script>
