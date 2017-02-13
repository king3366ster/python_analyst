# -*- coding:utf-8 -*- 
import sys, os
sys.path.append("..")
import datalib.CommandAgent as cmd
import settings

rawtext = '''
$set t_ex test.xlsx
$set t_cv test.csv
$set t_path ../testdata/
$set t

loadexcel --src ${t_path}${t_ex} --tar excdata
loadcsv --src ${t_path}${t_cv} --tar csvdata
# loadmysql --db localdb --tar msdata --query select * from tb_new where created_at > "${start}" limit 20
# merge --tar dst1 --src excdata csvdata --join left A B
merge --tar dst2 --src excdata csvdata --join inner C B
concat --tar dst3 --src csvdata excdata --join outer --axis 0
group --src excdata   --tar dst4  --by C --cols J|top2 HIS|first G|last C
resample --src excdata --tar dst5  --by HIS --cols G|sum H|mean --period 3d
'''

if __name__ == '__main__':
    cache = {}
    config = settings.config
    params = {
    	'start': '2016-11-21'
    }
    t = cmd.CommandAgent(config)
    cmds = t.readcmdtext(rawtext, params)
    t.runcmds(cmds, cache = cache)
    print (cache['dst4'], cache['dst5'])