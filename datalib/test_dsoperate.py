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
        'dbloadcsv --src  %s --tar csvdata' % t_cv,
        'dsgroup --src excdata   --tar dst1  --by A B --cols HIS|mean G|sum C',
    ]

    t = CommandAgent(dbconfig)
    for cmd in cmds:
        t.runcmd(cmd, cache)
    print (cache['dst1'])