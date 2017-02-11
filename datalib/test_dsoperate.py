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
        'dbloadexcel --src  %s  --tar excdata' % t_ex,
        # 'dbloadcsv --src  %s --tar csvdata' % t_cv,
        # 'dsgroup --src excdata   --tar dst1  --by C --cols J|top2 HIS|first G|last C',
        # 'dsresample --src excdata --tar dst1  --by HIS --cols G|sum H|mean --period 3d',
        'dstopn --src excdata --tar dst1 --by C --num 2',
    ]

    t = CommandAgent(dbconfig)
    t.runcmds(cmds, cache)
    print (cache['dst1'])