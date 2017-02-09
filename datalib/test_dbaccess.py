# -*- coding:utf-8 -*- 
import os, path
import re
from CommandAgent import CommandAgent
from testdata.testdb import dbconfig

if __name__ == '__main__':
    t_ex = 'testdata/test1.xlsx'
    t_cv = 'testdata/test.csv'

    cache = {}
    cmds = [
        'dbloadexcel --src %s --tar excdata' % t_ex,
        'dbloadcsv --src %s --tar csvdata' % t_cv,
        # 'dbloadmysql --db localdb --tar msdata --query select * from supporter_tech limit 20',
        # 'dbsaveexcel --src csvdata --tar testdata/testnewdata',
        # 'dbsavecsv --src msdata',
        'dbsavemysql --db localdb --src csvdata --tar tb_new --if_exists append --unique channel --need_datetime true'
    ]

    t = CommandAgent(dbconfig)
    for cmd in cmds:
        t.runcmd(cmd, cache)
    # print (cache['csvdata'], cache['excdata'])