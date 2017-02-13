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
	- load* 相关及 execunit单元始终是在树顶部，可以多进程
	- multipledata 如merge concat 操作类涉及多节点汇集，有相互依赖关系

- 异常传递
	- 进程优化涉及进程内套进程，异常需要逐层传递
	- 进程消息传递

