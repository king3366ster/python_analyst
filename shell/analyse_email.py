# -*- coding:utf-8 -*- 
import sys, os
sys.path.append("..")
import datalib.CommandAgent as cmd
import settings
from libemail import send_mail

index = 0
cmdfile = ''
for arg in sys.argv:
    if arg == '-f' and (index + 1 < len(sys.argv)):
        cmdfile = sys.argv[index + 1]
    index += 1
if cmdfile == '':
    raise Exception('CommandLine need cmd file path argument like: python analyse_file.py -f <filename>')

if __name__ == '__main__':
    cache = {}
    config = settings.config
    t = cmd.CommandAgent(config)
    cmds = t.readcmdfile(cmdfile)
    t.runcmds(cmds, cache = cache)
    data = (cache['result'].to_html())
    mailto_list = [
        'hzchensheng15@corp.netease.com',
        # 'hzliujun3@corp.netease.com',
        'hzquehangning@corp.netease.com',
        'hzhudan@corp.netease.com',
        'ddwang@corp.netease.com',
    ]
    print (send_mail(mailto_list, '数据统计', data))