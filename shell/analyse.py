# -*- coding:utf-8 -*- 
import sys, os
sys.path.append("..")
import datalib.CommandAgent as cmd
import settings

index = 0
cmdfile = ''
for arg in sys.argv:
    if arg == '-f' and (index + 1 < len(sys.argv)):
        cmdfile = sys.argv[index + 1]
    index += 1
if cmdfile == '':
    raise Exception('CommandLine need cmd file path argument like: python analyse.py -f <filename>')

if __name__ == '__main__':
    cache = {}
    config = settings.config
    t = cmd.CommandAgent(config)
    cmds = t.readcmdlines(cmdfile)
    for cmd in cmds:
        t.runcmd(cmd, cache)
    print (cache['dst1'])