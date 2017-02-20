### 后端消息接口
- 返回格式：
	- {"code": %r, "data": %s, "type": "%s", "channel": %r}
- 参数说明：
  - code
    - 200 消息正常返回
    - 101 Socket连接成功
  - type
    - shell 控制台命令
    - data 获取相应数据
    - process 进度条
    - cache 内存节点
    - filend 文档生成成功

### 前端消息接口
- 发送格式：
	- {	type, message, channel}
- 参数说明：
	- type
		- shell 控制台命令
		- data 获取相应数据
    - command 操作任务
