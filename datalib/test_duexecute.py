# -*- coding:utf-8 -*- 
import os, sys, path
sys.path.append("..")
import re
from CommandAgent import CommandAgent
from testdata.settings import dbconfig

if __name__ == '__main__':
    with open('../testdata/testunit1.data') as f:
        testunit1 = f.read()
    with open('../testdata/testunit2.data') as f:
        testunit2 = f.read()

    t = CommandAgent(dbconfig)
    t.set_execunit('tu1', testunit1)
    t.set_execunit('tu2', testunit2)

    cache = {}
    cmds = [
        'duexec --src tu1 --tar dst1',
        'duexec --src tu2 --tar dst2',
        'dsfilter --src dst2 --tar dst3 --cond A',
    ]
    t.runcmds(cmds, cache, multiprocess = True)
    print (cache['dst1'],cache['dst2'])