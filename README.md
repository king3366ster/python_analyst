### 数据源操作类
- params
    - src 需要载入数据的源配置对象的key(mysql/mongo需要/redis)或文件地址
    - tar 生成数据结果的内存引用名，可继续进行后续操作
    - query mysql语句
    - sheet excel表格/redis hset名

#### dbloadmysql
- examples
    - dbloadmysql --db localdb --tar msdata --query select * from tb_new limit 20

#### dbsavemysql
- examples
    - dbsavemysql --db localdb --src csvdata --tar tb_new --if_exists append --unique channel 

#### dbloadredis
- examples
    - dbloadredis --db testdb --tar dataframe --sheet hsetname 

#### dbsaveredis

#### dbloadmongo
- examples
    -dbloadmongo --db testdb --tar dataframe --query db.query.find()

#### dbsavemongo

#### dbloadexcel
- examples
    - dbloadexcel --tar dataframe --src source--sheet Sheet1

#### dbsaveexcel
- examples
    - dbsaveexcel --tar dest --src source

#### dbloadcsv
- examples
    - dbloadcsv --tar dataframe --src source

#### dbsavecsv
- examples
    - dbsavecsv --tar dest --src source

### 多数据聚合类
- params
    - tar 目标节点名
    - src 源节点名，可以多个节点（merge/concat至少2个），空格分隔

#### dmmerge
- params
    - join 连接方式，merge/concat分别为left/right/inner/outer，及连接的键
- examples
    - dmmerge --tar dest --src src1 src2 --join left cid aid

#### dmconcat
- params
    - join 连接方式，merge/concat分别为left/right/inner/outer，及连接的键
- examples
    - dmconcat --tar dest --src src1 src2 --join inner cid aid

### 单数据筛选类
- params
    - tar 目标节点名
    - src 源节点名，可以多个节点（merge/concat至少2个），空格分隔

#### dsoperate
- params
    - order 对列进行排序，以空格分割字段，以空格分隔列名与排序规则
    - topn 获取top N 行
    - lastn 获取 last N 行
    - cond 获取条件筛选结果 ~(正则匹配) > < =
    - rename 重命名列名
    - trans 切换列类型/重计算
    - setval 对某个单元设置具体数值
- examples
    - dsoperate --tar dest --src src1 --cond (`A`~"^sa*")|(`B`=12)&(`C`>=2016-01-21 02:11:21) 
    - dsoperate --tar dest --src src1 --rename `A`->`B` `D`->`C`
    - dsoperate --tar dest --src src1 --trans `A`=`B`-`C` `D`->int `B`=21
    - dsoperate --tar dest --src src1 --setval `A`.`12` = 123

#### dsparsejson(需要迭代器)
* 对数据某一字段进行json解析，提取对应的keyname，生成新的column
- params
    - by 进行json解析的字段
    - cols 需要解析json字段的属性

- examples
    - dsparsejson --tar dest --src src1 --by col1 --cols key1.subkey1 key2

#### dsgroup
* 对数据进行编组统计，类似于数据库的groupby(目前支持select count(*))
- params
    - by 进行groupby的键值，可多选
    - cols <column>|<method>
        - sum/mean/count/std/min/max/top/last
        - top(N): top2 top3 top1等同于top
- examples
    - dsgroup --tar dest --src src1 --by col1 --cols 商机id --cols col1|sum col2|mean 
    - dsgroup --tar dest --src src1 --by col1 col2 --cols col3 col4

#### dsresample
* 时间序列重采样
- params
    - by 进行重采样的列
    - cols <column>|<method>
        - sum/mean/count/std/min/max/top/last
        - top(N): top2 top3 top1等同于top
    - period 采样周期
- examples
    - dsresample --src excdata --tar dst1  --by HIS --cols G|sum H|mean --period 3d
