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
        'dbloadexcel --src %s --tar excdata' % t_ex,
        'dbloadcsv --src %s --tar csvdata' % t_cv,
        # 'dbloadmysql --db localdb --tar msdata --query select * from tb_new limit 20',
        # 'dmmerge --tar dst1 --src excdata csvdata --join left A B',
        'dmmerge --tar dst2 --src excdata csvdata --join inner C B',
        'dmconcat --tar dst1 --src csvdata excdata --join outer --axis 0',
    ]

    t = CommandAgent(dbconfig)
    t.runcmds(cmds, cache)
    print (cache['dst1'])