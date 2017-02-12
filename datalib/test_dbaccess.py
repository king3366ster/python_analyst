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
        'dbloadexcel --src %s --tar excdata' % t_ex,
        'dbloadcsv --src %s --tar csvdata' % t_cv,
        # 'dbloadmysql --db localdb --tar msdata --query select * from tb_new limit 20',
        'dbsaveexcel --src csvdata --tar ../testdata/testnewdata',
        # 'dbsavecsv --src msdata',
        # 'dbsavemysql --db localdb --src csvdata --tar tb_new --unique channel --if_exists replace',
        # 'dbsavemysql --db localdb --src excdata --tar tb_new --if_exists append --unique channel --need_datetime true',
    ]

    t = CommandAgent(dbconfig)
    t.runcmds(cmds, cache, multiprocess = True)
    print (cache['csvdata'])