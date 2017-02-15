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
        'loadcsv --src %s --tar csvdata' % t_cv,
        # 'loadmysql --db localdb --tar msdata --query select * from tb_new limit 20',
        # 'merge --tar dst1 --src excdata csvdata --join left A B',
        'concat --tar dst1 --src csvdata excdata --join outer --axis 0',
        'merge --tar dst2 --src excdata csvdata dst1 --join left C B',
    ]

    t = CommandAgent(dbconfig)
    t.runcmds(cmds, cache)
    print (cache['dst1'], cache['dst2'])