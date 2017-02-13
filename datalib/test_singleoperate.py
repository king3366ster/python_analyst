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
        'loadexcel --src  %s  --tar excdata' % t_ex,
        # 'loadcsv --src  %s --tar csvdata' % t_cv,
        'group --src excdata   --tar dst3  --by C --cols J|top2 HIS|top G|last G|top1 G|mean C',
        'resample --src excdata --tar dst1  --by HIS --cols G|sum G|mean H|mean --period 3d',
        # 'topnrows --src excdata --tar dst1 --by C --num 3',
        # 'filter --src excdata --tar dst2 --cond (HIS<"2017-12-12") & (G!=4) & (C~="^pc")',
        # 'filter --src excdata --tar dst2 --cond (HIS<"2017-12-12") --limit 4 2',
        # 'opcol --src excdata --tar dst2 --setcol M1=A+B, HI = HIS, T3 = HIS-T2, T3->str',
        # 'opcol --src excdata --tar dst2 --setcol HI = HIS --dropcol HIS --leftcol A B C G',
        # 'opcol --src excdata --tar dst2 --setcol HI = HIS --dropcol HIS --leftcol A B C G --rename B -> 测试 C-> 公平',
        # 'sort --src excdata --tar dst2 --order A asc, G desc, J',
        # 'opnull --src excdata --tar dst2 --fill 3.2',
        'parsejson --src excdata --tar dst2 --cols jsd.d2 jsd.dv jsd.dv.fd'
        # 'saveexcel --src dst2 --tar ../testdata/t.xlsx',
    ]

    t = CommandAgent(dbconfig)
    t.runcmds(cmds, cache)
    # print (cache['excdata'])
    print (cache['dst3'], cache['dst1'])