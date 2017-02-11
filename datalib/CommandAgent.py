# -*- coding:utf-8 -*- 
import os, sys, pdb
import re, copy
import databaseaccess.runcmd as db, datamultioperate.runcmd as dm, datasingleoperate.runcmd as ds

class CommandAgent(object):
    """docstring for CommandAgent"""
    def __init__(self, config = {}):
        super(CommandAgent, self).__init__()
        self.config = config
        if 'execpath' not in self.config:
            self.config['execpath'] = ''
        if 'unitdata' not in self.config:
            self.config['unitdata'] = {}

    def set_unitcmds (self, key, value):
        self.config['unitdata'][key] = value

    def readcmdfile (self, filename, params = {}):
        filepath = self.config['execpath'] + filename
        param_map = copy.deepcopy(params)
        commands = []
        with open(filepath) as f:
            for cmdline in f.readlines():
                cmdline = self.parsetext(cmdline, param_map = param_map)
                if cmdline != '':
                    commands.append(cmdline)
        return commands

    def readcmdtext (self, rawtext = '', params = {}):
        param_map = copy.deepcopy(params)
        commands = []
        cmdlines = rawtext.split('\n')
        for cmdline in cmdlines:
            cmdline = self.parsetext(cmdline, param_map = param_map)
            if cmdline != '':
                commands.append(cmdline)
        return commands

    def parsetext (self, cmdline, param_map = {}):
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
            return ''
        elif cmdline.find('#') == 0:
            return ''
        elif cmdline != '':
            if re.search(r'\$\{[^\}\s]+\}', cmdline):
                params = re.findall(r'\$\{[^\}\s]+\}', cmdline)
                for param in params:
                    param = re.sub(r'^\$\{', '', param)
                    param = re.sub(r'\}$', '', param)
                    if param in param_map:
                        cmdline = cmdline.replace('${%s}' % param, param_map[param])
        return cmdline

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

    # 执行命令单元集合
    def rununit (self, cmdobj):
        cmdkeys = cmdobj['ckeys']
        if 'src' not in cmdkeys:
            raise Exception('Command Error: duexec without src')
        if 'tar' not in cmdkeys:
            raise Exception('Command Error: duexec without tar')
        src = cmdkeys['src']
        tar = cmdkeys['tar']
        if src not in self.config['unitdata']:
            raise Exception('Runtime Error: duexec src %s has not been set' % src)
        cmds = self.config['unitdata'][src]
        cmds = self.readcmdtext(cmds)
        output = None
        for cmd in cmds:
            cobj = self.parsecmd(cmd)
            if 'tar' in cobj['ckeys']:
                output = cobj['ckeys']['tar']
        cache = {}
        self.runcmds(cmds, cache)
        result = cache[output]
        return result

    def runcmd (self, cmd, cache = None):
        cmdobj = self.parsecmd(cmd)
        ctype = cmdobj['ctype']
        if ctype.find('db') == 0: # databaseaccess类
            result = db.runcmd(cmdobj, config = self.config, cache = cache)
        elif ctype.find('ds') == 0: # datasingleoperate类
            result = ds.runcmd(cmdobj, cache = cache)
        elif ctype.find('dm') == 0: # datasingleoperate类
            result = dm.runcmd(cmdobj, cache = cache)
        elif ctype == 'duexec': # dataunitexecute类
            result = self.rununit(cmdobj)
        else:
            return None
        if 'tar' in cmdobj['ckeys'] and cache is not None:
            cache[cmdobj['ckeys']['tar']] = result

    def runcmds (self, cmds = [], cache = None):
        if cache is None:
            raise Exception('Runtime Error: cache should not be none')
        [self.runcmd(cmd, cache) for cmd in cmds]

if __name__ == '__main__':

    cache = {}
    t_ex = 'testdata/test.xlsx'
    t_cv = 'testdata/test.csv'
    cmds = [
        'dbloadexcel --src %s --tar excdata' % t_ex,
        'dbloadcsv --src %s --tar csvdata' % t_cv,
        'dmmerge --tar dst1 --src excdata csvdata --join inner A C B',
        'dsgroup --tar dst2 --src dst1 --by A --cols B|count'
    ]
    t = CommandAgent()
    t.runcmds(cmds, cache)
    print (cache['dst1'], cache['dst2'])
