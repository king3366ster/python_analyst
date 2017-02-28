# -*- coding:utf-8 -*-

presets = [
	{
        'name': '测试脚本',
        'desc': '用于测试的脚本',
		'file': 'test.data',
		'params': [
			['start_at', 'date'],
			['end_at', 'date'],
            ['选择框', 'select', [['选项1', 1], ['选项2', 2], ['选项3', 3
            ]]],
		]
	},
	{
        'name': '测试脚本2',
        'desc': '用于测试',
		'file': 'testcsv.data',
		'params': [
			'数字大于',
			'数字小于',
		]
	}
]
