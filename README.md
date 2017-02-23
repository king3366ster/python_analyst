## 安装部署
### 环境安装
- 数据处理库环境安装
    - pip install numpy pandas openpyxl mysql-python sqlalchemy
- web后台环境安装
    - pip install django channels redis asgi_redis django_redis_sessions
- web前端环境安装
    - npm install

### 初始化命令
- 本地部署方式
    - 将main文件夹中的settings_test.py文件重命名为settings.py
    - 测试环境初始化部署：
        - 开启redis服务 可在main文件的settings.py中做相应配置
        - python manage.py makemigrations app
        - python manage.py migrate
        - python manage.py createsuperuser / test / tt111111
    - 测试环境运行
        - python manage.py runserver 0.0.0.0:8000
        - 访问localhost:8000  帐号：test tt111111

### 目录结构
- 数据分析引擎
    - datalib  核心数据处理引擎
        - databaseaccess  数据获取及输出层
        - datamultioperate  多数据合并层
        - datasingleoperate  单数据筛选及操作层
        - test_*.py  测试文件
- 独立执行脚本
    - shell  可直接脚本执行数据分析示例
    - testdata  直接进行脚本执行的测试数据与配置
- 可视化web工程
    - main  后端工程主入口及环境配置
    - app  后端服务主目录
    - webapp  前端工程主目录

## 命令接口
### 数据源操作类
- params
    - src 需要载入数据的源配置对象的key(mysql/mongo需要/redis)或文件地址
    - tar 生成数据结果的内存引用名，可继续进行后续操作
    - query mysql语句
    - sheet excel表格/redis hset名

#### loadmysql
- examples
    - loadmysql --db localdb --tar msdata --query select * from tb_new limit 20

#### savemysql
- examples
    - savemysql --db localdb --src csvdata --tar tb_new --if_exists append --unique channel

#### loadredis
- examples
    - loadredis --db testdb --tar dataframe --sheet hsetname

#### saveredis

#### loadmongo
- examples
    -dbloadmongo --db testdb --tar dataframe --query db.query.find()

#### savemongo

#### loadexcel
- examples
    - loadexcel --tar dataframe --src source--sheet Sheet1

#### saveexcel
- examples
    - saveexcel --tar dest --src source

#### loadcsv
- examples
    - loadcsv --tar dataframe --src source

#### savecsv
- examples
    - savecsv --tar dest --src source

### 多数据聚合类
- params
    - tar 目标节点名
    - src 源节点名，可以多个节点（merge/concat至少2个），空格分隔

#### merge
- params
    - join 连接方式，merge/concat分别为left/right/inner/outer，及连接的键
- examples
    - merge --tar dest --src src1 src2 --join left cid aid

#### concat
- params
    - join 连接方式，merge/concat分别为left/right/inner/outer，及连接的键
- examples
    - concat --tar dest --src src1 src2 --join inner cid aid

### 单数据筛选类
- params
    - tar 目标节点名
    - src 源节点名，可以多个节点（merge/concat至少2个），空格分隔

#### filter
* 数据比较筛选过滤器
- params
    - cond 比较操作命令，列名放在操作符前，程序会自动解析
        - 运算操作符 < <= == >= > != ~=
            - ~= 操作符表示正则匹配 如 A ~= "^P+"
            - 字符类型的比较务必加上引号 如 A == ""
        - 比较操作符 & |
            - & 与操作 | 或操作
        - 优先操作符 ( )
    - sort 排序，执行顺序晚于cond
        - 方法使用： <列名><排序方式> 以逗号(,)分隔
        - 排序方式：asc|desc 不填默认升序
        - 排序优先级依命令顺序
    - cols
        - 选取特定的列 (可选)
    - limit 获取特定行 以逗号(,)分隔
        - 一个参数时(--limit num)等同于 offset 0 limit num
        - 两个参数时(--limit num1, num2)等同于 offset num1 limit num2
        - 超过两个参数，只取前两个参数
- examples
    - filter --src excdata --tar dst1 --cond (HIS<"2017-12-12") & (G!=4) & (C~="^pc")
    - filter --src excdata --tar dst1 --cond (HIS<"2017-12-12") --limit 2 4
    - filter --src excdata --tar dst1 --sort A asc, G desc

#### opcol
* 列操作
- params
    - setcol 设置列 如 A=B-C, B=1, D->int/time/str/float
    - dropcol 删除列
    - leftcol 剩余列
    - rename 重命名列 逗号分隔
    - 任何一条opcol命令执行顺序为 setcol -> dropcol -> leftcol -> rename 可多选少选
- examples
    - opcol --src excdata --tar dst2 --setcol M1=A+B, HI = HIS, T3 = HIS-T2, T3->str
    - opcol --src excdata --tar dst2 --setcol HI = HIS --dropcol HIS
    - opcol --src excdata --tar dst2 --setcol HI = HIS --leftcol A HI
    - opcol --src excdata --tar dst2 --setcol HI = HIS --dropcol HIS --leftcol A B C G --rename B -> 测试, C-> 公平

#### opnull
* 空值操作
- params
    - setval 对空值的填充内容
- examples
    - opnull --src excdata --tar dst2 --setval 3.2

#### parsejson(需要迭代器)
* 对数据某一字段进行json解析，提取对应的keyname，生成新的column
- params
    - cols 需要解析json字段的列及属性 如col1.key1
    - json内部属性嵌套可以使用.操作符级联

- examples
    - parsejson --tar dest --src src1 --cols col1.key1.subkey1 col2.key2

#### replace
* 全局替换
- params
    - setval 将特定数值进行替换
- examples
    - replace --tar dest --src src1 --setval 0->null 3->"as"

### 聚合分析类
#### group
* 对数据进行编组统计，类似于数据库的groupby(目前支持select count(*))
- params
    - by 进行groupby的键值，可多选
    - cols <column>|<method>
        - sum/mean/count/std/var/min/max/top/last
        - top(N): top2 top3 top1等同于top
- examples
    - group --tar dest --src src1 --by cola --cols col1|sum col2|mean
    - group --tar dest --src src1 --by col1 col2 --cols col3 col4

#### resample
* 时间序列重采样
- params
    - by 进行重采样的列
    - cols <column>|<method>
        - sum/mean/count/std/min/max/top/last
        - top(N): top2 top3 top1等同于top
    - period 采样周期
- examples
    - resample --src excdata --tar dst1  --by HIS --cols G|sum H|mean --period 3d

#### topnrows
* 获取特定标签顶部的N行
- params
    - by 对比维度
    - num 获取每一对比维度的行数
- examples
    - topnrows --src excdata --tar dst1 --by C --num 3

### 执行单元类
#### execunit
* 执行特点配置好的命令数据
- params
    - src 在内存中的命令行key，可以通过CommandAgent.set_execunit函数写到CommandAgent对象的config['unitdata']中
    - tar 处理完成后的数据输出
- examples
    - execunit --src src1 --tar dst1

### 独立命令
#### cleancache
* 清理下载文件及缓存
