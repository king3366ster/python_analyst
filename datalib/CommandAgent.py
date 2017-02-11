# -*- coding:utf-8 -*- 
import os, sys
import re
import databaseaccess.runcmd as db, datamultioperate.runcmd as dm, datasingleoperate.runcmd as ds

class CommandAgent(object):
    """docstring for CommandAgent"""
    def __init__(self, config = {}):
        super(CommandAgent, self).__init__()
        self.config = config

    def readcmdlines (self, filename):
        filepath = self.config['cmdpath'] + filename
        param_map = dict()
        commands = []
        with open(filepath) as f:
            for cmdline in f.readlines():
                cmdline = cmdline.strip()
                if cmdline.find('$set') >= 0:
                    cmdline = re.sub('^\s*\$set\s+', '', cmdline)
                    reg = re.search(r'\s+', cmdline)
                    if reg:
                        pos = reg.start(0)
                        key = cmdline[:pos].strip()
                        val = cmdline[pos:].strip()
                    else:
                        key = cmdline
                        val = ''
                    if key != '':
                        param_map[key] = val
                elif cmdline.find('#') == 0:
                    continue
                elif cmdline != '':
                    if re.search(r'\$\{[^\}\s]+\}', cmdline):
                        params = re.findall(r'\$\{[^\}\s]+\}', cmdline)
                        for param in params:
                            param = re.sub(r'^\$\{', '', param)
                            param = re.sub(r'\}$', '', param)
                            if param in param_map:
                                cmdline = cmdline.replace('${%s}' % param, param_map[param])
                    commands.append(cmdline)
        return commands
        
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
            keys = map(lambda x: x.strip(), keys)
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
                key = key[2:]
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
            result = ds.runcmd(cmdobj, cache = cache)
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
