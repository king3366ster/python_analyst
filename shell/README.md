## 命令行方式操作步骤
### 输入文件的执行方式
- 编辑 settings.py文件，填写对应的db配置、输入命令行所在文件夹路径、输入excel/csv文件所在文件夹（如果有）
- 编辑命令行脚本，如 test.data
- 操作命令行: python analyse_file.py -f <filename>
	- example: python analyse_file.py -f test.data

### 输入文本的执行方式
- 编辑 settings.py文件，填写对应的db配置、输入命令行所在文件夹路径、输入excel/csv文件所在文件夹（如果有）
- 参考 analyse_rawtext.py
	- 设置输入输出所在的缓存对象：
		- cache = {}
    - 设置数据库等相关配置文件：
    	- config = settings.config
    	- 也可以在py文件中独立设置 config = {}
    - 生成命令代理对象：
    	- t = cmd.CommandAgent(config)
    - 执行命令：
    	- cmds = t.readcmdraw(rawtext, config)
    - 从内存中查看对应数据
    	- print (cache['dst1'])