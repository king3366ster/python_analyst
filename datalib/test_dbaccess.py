# -*- coding:utf-8 -*-
import os, sys, path
sys.path.append("..")
import re
from CommandAgent import CommandAgent
from testdata.settings import dbconfig

if __name__ == '__main__':
    t_ex = '../testdata/test.xlsx'
    t_cv = '../testdata/test.csv'

    cache = {}
    cmds = [
        'loadexcel --src %s --tar excdata' % t_ex,
        # 'loadcsv --src %s --tar csvdata' % t_cv,
        # 'loadmysql --db localdb --tar msdata --query select * from tb_new limit 20',
        # 'saveexcel --src csvdata --tar ../testdata/testnewdata',
        'savecsv --src excdata --tar ../testdata/testnewdata',
        # 'savemysql --db localdb --src excdata --tar tb_new --if_exists replace --unique A --need_datetime true',
    ]
    # 可设置dbconfig的loadpath/savepath属性，设置默认文件载入、存储路径
    t = CommandAgent(dbconfig)
    t.runcmds(cmds, cache, multithread = False)
    print (cache['excdata'])
