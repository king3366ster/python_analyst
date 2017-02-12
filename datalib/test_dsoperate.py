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
        'dbloadexcel --src  %s  --tar excdata' % t_ex,
        # 'dbloadcsv --src  %s --tar csvdata' % t_cv,
        'dsgroup --src excdata   --tar dst1  --by C --cols J|top2 HIS|top G|last C',
        # 'dsresample --src excdata --tar dst1  --by HIS --cols G|sum H|mean --period 3d',
        # 'dstopnrows --src excdata --tar dst1 --by C --num 3',
        'dsfilter --src excdata --tar dst1 --cond (HIS<"2017-12-12") & (G!=4) & (C~="^pc")',
    ]

    t = CommandAgent(dbconfig)
    t.runcmds(cmds, cache)
    print (cache['dst1'])