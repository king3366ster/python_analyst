### 后端消息接口
- 返回格式：
	- {"code": %r, "data": %s, "type": "%s", "channel": %r}

### 前端消息接口
- 发送格式：
	- {	type, message, channel}
- 参数说明：
	- type
		- shell 控制台命令
		- data 获取相应数据
		- process 进度条
		- cache 内存节点
    - command 操作任务
