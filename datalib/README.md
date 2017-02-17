### 配置选项
- 初始化CommandAgent 命令代理对象时，可传入配置选项，如：
    - t = CommandAgent(dbconfig)
- dbconfig 中可通过设置数据库键值、载入文件路径、存储文件路径等
    - 设置数据库键值:
        - 如：'localdb': { 'host': '127.0.0.1', 'user': 'root', ...}
        - 则可直接使用键名做数据库选择 如 loadmysql --db localdb --tar ...
    - 设置文件输入路径
        - 必须匹配全名，即： 'loadpath': ...
        - 可在config文件中不填，文件路径默认为''
        - 如配置loadpath为'/home/test/' 则命令loadcsv --src file.csv则会读取/home/test/file.csv
    - 设置文件输出路径
        - 必须匹配全名，即： 'savepath': ...
        - 可在config文件中不填，文件路径默认为''
- 初始化执行单元(execunit)
    - 必须通过CommandAgent对象方法set_execunit将命令行文本载入内存如：
        - t.set_execunit('tu1', testunit1)
        - t.set_execunit('tu2', testunit2)
    - 随后可通过命令如：execunit --src tu1 --tar dst1 执行命令集合
    - execunit单元内部指令，默认经过优化，采用多线程执行

### 测试单元
- test_dbaccess.py
    - 用于测试数据获取、存储相关的命令
- test_execunit.py
    - 用于测试命令执行单元（如文件、Mysql中存储的命令集合文本）
- test_singleoperate.py
    - 用于测试单节点数据操作
- test_multioperate.py
    - 用于测试多节点数据合并操作

### 技术重点
- 执行单元嵌套(递归)相互阴影造成无限循环
	- 例如 B {execunit A ... {execunit B ...}}
	- 解决方式： 命令解析及预检查 checkloop 检查最大迭代深度

- 命令优化(多进程)
	- 解析命令节点，生成列表，生成命令树
	- load* 相关及 execunit单元始终是在树顶部，可以多线程优化(IO密集型)
	- multipledata 如merge concat 操作类涉及多节点汇集，有相互依赖关系，不可多线程

- 异常传递
	- 进程优化涉及进程内套进程，异常需要逐层传递
	- 进程消息传递
