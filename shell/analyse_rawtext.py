# -*- coding:utf-8 -*- 
import sys, os
sys.path.append("..")
import datalib.CommandAgent as cmd
import settings

rawtext = '''
$set t_ex test.xlsx
$set t_cv test.csv
$set t_path ../datalib/testdata/
$set t

dbloadexcel --src ${t_path}${t_ex} --tar excdata
dbloadcsv --src ${t_path}${t_cv} --tar csvdata
dbloadmysql --db localdb --tar msdata --query select * from tb_new where created_at > "${start}" limit 20
# dmmerge --tar dst1 --src excdata csvdata --join left A B
dmmerge --tar dst2 --src excdata csvdata --join inner C B
dmconcat --tar dst3 --src csvdata excdata --join outer --axis 0
dsgroup --src excdata   --tar dst4  --by C --cols J|top2 HIS|first G|last C
dsresample --src excdata --tar dst5  --by HIS --cols G|sum H|mean --period 3d
'''

if __name__ == '__main__':
    cache = {}
    config = settings.config
    params = {
    	'start': '2016-11-21'
    }
    t = cmd.CommandAgent(config)
    cmds = t.readcmdraw(rawtext, params)
    print cmds
    t.runcmds(cmds, cache = cache)
    print (cache['dst4'], cache['dst5'])