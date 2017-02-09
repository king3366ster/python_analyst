# -*- coding:utf-8 -*- 
import os, path
import re
from CommandAgent import CommandAgent
from testdata.testdb import dbconfig

if __name__ == '__main__':
    t_ex = 'testdata/test.xlsx'
    t_cv = 'testdata/test.csv'

    cache = {}
    cmds = [
        'loadexcel --src %s --tar excdata' % t_ex,
        'loadcsv --src %s --tar csvdata' % t_cv,
        'loadmysql --db localdb --tar msdata --query select * from supporter_tech limit 20',
        # 'saveexcel --src msdata --tar testdata/testnewdata',
        # 'savecsv --src msdata',
        'savemysql --db localdb --src csvdata --tar tb_new --if_exist append --unique channel'
    ]

    t = CommandAgent(dbconfig)
    for cmd in cmds:
        t.runcmd(cmd, cache)
    print (cache['csvdata'], cache['msdata'])