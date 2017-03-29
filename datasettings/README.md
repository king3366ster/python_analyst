## 配置文件说明
### settings.py
* 数据库文件配置、载入文件路径、保持文件路径配置地点
* 载入文件路径目标地需以loadpath为键值如：
	- 'loadpath': 'datasettings/loadpath/',
* 保持文件路径目标地需以savepath为键值如：
	- 'savepath': 'datasettings/savepath/',
* 数据库配置参考数据库命令说明
  - 设置数据库键值:
    - 以mysql为例：
      - 如：'localdb': { 'host': '127.0.0.1', 'user': 'root', 'pwd': '**', 'db': 'test', 'port': 3306,}
      - 则可直接使用键名做数据库选择 如 loadmysql --db localdb --tar ... --query ...

### presets.py
* 界面选项配置： datasettings/presets.py
  - 配置文件为json形式，参数如下：
    - name: 选择数据的名称
    - desc：数据描述
    - file：用于数据分析的数据脚本名称，固定目录在datasettings/execunit
    - perm: 该数据可供应的权限，不填则为全部拥有权限
    - params: 选择数据的可选参数，与*.data文件配套使用
      - 格式为数组，第一项为参数名，第二项为参数类型，用于前端的input[type]，第三项为补充参数类型，如select框的选择，至少填一项
      - 第二项参数类型可选：text/number/date/email/select...

### *.data文件
* 预置执行单元配置
  - 数据执行脚本文件：datasettings/execunit/**.data
    - 自定义参数语法：
      - 文件头设置 $set key val
      - 命令行中使用 ${key}，解析器会自动用val替换${key}
      - 替换方式如C语言中的 #define key val 的用法