# -*- coding:utf-8 -*- 

CommandMap = {
    'execunit': set([
        'execunit',
    ]),
    'loaddata': set([
        'loadexcel',
        'loadcsv',
        'loadmysql',
    ]),
    'savedata': set([
        'saveexcel',
        'savecsv',
        'savemysql',
    ]),
    'multipledata': set([
        'merge',
        'concat',
    ]),
    'singledata': set([
        'filter', # 行数据筛选
        'sort', # 排序操作
        'opcol', # 列操作
        'opnull', # 处理null值
        'parsejson', # 解析json字段
        'group',
        'resample',
        'topnrows',
    ]),
}