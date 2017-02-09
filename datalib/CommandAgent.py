# -*- coding:utf-8 -*- 
import os, sys
import re
import databaseaccess.dbruncmd as db, datamultioperate.dmruncmd as dm, datasingleoperate.dsruncmd as ds

class CommandAgent(object):
    """docstring for CommandAgent"""
    def __init__(self, config = {}):
        super(CommandAgent, self).__init__()
        self.config = config
        
    def parsecmd (self, cmd):
        cmd = unicode(cmd).strip()
        space = re.search(r'\s+', cmd)
        if not space:
            return {
                'ctype': cmd,
                'ckeys': {},
            }
        else:
            spindex = space.start(0)
            ctype = cmd[: spindex]
            ckeys = {}
            keys = re.findall(r'\s+--[^\-\s]+', cmd)
            keyset = set()
            keypos = []
            for key in keys:
                if key in keyset:
                    raise Exception('Command Error: duplicate command options %s' % key)
                else:
                    keyset.add(key)
                keypos.append(cmd.find(key))
            keypos.append(len(cmd))
            for i in range(0, len(keypos) - 1):
                key = keys[i]
                value = cmd[keypos[i] + len(key) : keypos[i + 1]].strip()
                key = key[3:]
                ckeys[key] = value
            del keyset
            return {
                'ctype': ctype,
                'ckeys': ckeys,
            }

    def runcmd (self, cmd, cache = None):
        cmdobj = self.parsecmd(cmd)
        ctype = cmdobj['ctype']
        if ctype.find('db') == 0: # databaseaccess类
            result = db.runcmd(cmdobj, config = self.config, cache = cache)
        elif ctype.find('ds') == 0: # datasingleoperate类
            result = ds.runcmd(cmdobj)
        elif ctype.find('dm') == 0: # datasingleoperate类
            result = dm.runcmd(cmdobj, cache = cache)
        else:
            return None
        if 'tar' in cmdobj['ckeys'] and cache is not None:
            cache[cmdobj['ckeys']['tar']] = result
        return result

if __name__ == '__main__':

    cache = {}
    t_ex = 'testdata/test.xlsx'
    t_cv = 'testdata/test.csv'
    cmds = [
        'loadexcel --src %s --tar excdata' % t_ex,
        'loadcsv --src %s --tar csvdata' % t_cv,
    ]
    t = CommandAgent()
    for cmd in cmds:
        t.runcmd(cmd, cache)
    print (cache['csvdata'], cache['excdata'])
