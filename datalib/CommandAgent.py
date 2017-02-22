# -*- coding:utf-8 -*-
import os, sys, signal, pdb
import multiprocessing
import re, copy
import databaseaccess.runcmd as db, datamultioperate.runcmd as dm, datasingleoperate.runcmd as ds
from CommandProcess import CommandProcess
from CommandThread import CommandThread
from CommandMap import CommandMap

class CommandAgent(object):
    """docstring for CommandAgent"""
    def __init__(self, config = {}):
        super(CommandAgent, self).__init__()
        self.config = config
        if 'execpath' not in self.config:
            self.config['execpath'] = ''
        if 'unitdata' not in self.config:
            self.config['unitdata'] = {}

    def set_execunit (self, key, value):
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
        try:
            if not isinstance(cmdline, unicode):
                cmdline = cmdline.decode('utf-8', 'ignore')
        except:
            cmdline = cmdline
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
                if key not in param_map: # 不覆盖策略
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
        try:
            if not isinstance(cmd, unicode):
                cmd = cmd.decode('utf-8', 'ignore')
        except:
            cmd = cmd
        cmd = cmd.strip()
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

    # 解析 --params 参数
    def parse_params (self, params):
        params = re.split(r'\s*,\s*', params)
        param_map = {}
        for param in params:
            param = param.strip()
            if param.find('=') > 0:
                tmp = re.split(r'\s*=\s*', param)
                param_map[tmp[0]] = tmp[1]
            else:
                param_map[param] = ''
        return param_map

    # 执行命令单元集合
    def rununit (self, cmdobj, multithread = True):
        cmdkeys = cmdobj['ckeys']
        if 'src' not in cmdkeys:
            raise Exception('Command Error: execunit without src')
        if 'tar' not in cmdkeys:
            raise Exception('Command Error: execunit without tar')
        src = cmdkeys['src']
        tar = cmdkeys['tar']
        if src not in self.config['unitdata']:
            raise Exception('Runtime Error: execunit src %s has not been set' % src)
        cmds = self.config['unitdata'][src]
        param_map = {} # 配置文件内设置参数
        if 'params' in cmdkeys:
            param_map = self.parse_params(cmdkeys['params'])
        cmds = self.readcmdtext(cmds, param_map)
        output = None
        for cmd in cmds:
            cobj = self.parsecmd(cmd)
            if 'tar' in cobj['ckeys']:
                output = cobj['ckeys']['tar']
        cache = {}
        self.runcmds(cmds, cache, multithread = multithread)
        result = cache[output]
        return result

    # hook 为执行完命令的回调
    def runcmd (self, cmd, cache = None, hook = None):
        print ('%r' % cmd)
        if cache is None:
            raise Exception('Runtime Error: cache should not be none')
        cmdobj = self.parsecmd(cmd)
        ctype = cmdobj['ctype']
        if ctype in CommandMap['execunit']:
            result = self.rununit(cmdobj)
        elif ctype in CommandMap['loaddata']:
            result = db.runcmd(cmdobj, config = self.config, cache = cache)
        elif ctype in CommandMap['savedata']:
            result = db.runcmd(cmdobj, config = self.config, cache = cache)
        elif ctype in CommandMap['singledata']:
            result = ds.runcmd(cmdobj, cache = cache)
        elif ctype in CommandMap['multipledata']:
            result = dm.runcmd(cmdobj, cache = cache)
        else:
            result = None

        if 'tar' in cmdobj['ckeys'] and cache is not None:
            if result is not None:
                target = cmdobj['ckeys']['tar']
                cache[target] = result
                print ('--tar: %r colums: %r' % (target, list(result.columns)))
        if hook is not None:
            hook(result)
        return result

    # hook 回调仅在非开启multithread有效
    def runcmds (self, cmds = [], cache = None, multithread = False, multiprocess = False, hook = None):
        self.checkloop (cmds) # 检查递归深度
        # print ('itercount %d' % self.checkloop (cmds))
        if cache is None:
            raise Exception('Runtime Error: cache should not be none')
        if multithread or multiprocess:
            cmdmap = self.sortcmds(cmds)
            mthreadcmds = cmdmap['mthread']
            serialcmds = cmdmap['serial']
            mprocesscmds = cmdmap['mprocess']

            # 多线程执行
            multithread = CommandThread(self.runthreadcmd)
            # 多进程执行
            multiproc = CommandProcess(self.runprocesscmd)

            cache_new = multithread.run(mthreadcmds) # 用于load源数据
            cache.update(cache_new) # 内存引用更新
            # 单进程/线程串行
            [self.runcmd(cmd, cache) for cmd in serialcmds]
            multiproc.run(mprocesscmds, cache, comm = False) # 用于save结果数据，不需要数据通信
        else:
            [self.runcmd(cmd, cache, hook) for cmd in cmds]

    # 多进程命令函数
    def runprocesscmd (self, cmd, cache = None, msg_queue = None):
        try:
            # print ('multiprocess start: %s' % cmd)
            if cache is None:
                cache = {}
            self.runcmd(cmd, cache)
            msg_queue.put(cache)
            print ('multiprocess end: %s' % cmd)
        except Exception as what:
            try:
                print ('multiprocess error: %s' % unicode(what))
                msg_queue.put({'error': what})
            except:
                print ('multiprocess error: unknown error')
        # curr_proc = multiprocessing.current_process()
        # if curr_proc.is_alive():
        #     pid = curr_proc.pid
        #     print ('kill pid %d' % pid)
        #     os.kill(pid, 9)

    # 多线程命令函数
    def runthreadcmd (self, cmd, msg_queue, lock):
        try:
            # print ('thread start: %s' % cmd)
            cache = {}
            self.runcmd(cmd, cache)
            with lock:
                msg_queue.append(cache)
            print ('thread end: %s' % cmd)
        except Exception as what:
            try:
                print ('multithread error: %s' % unicode(what))
                msg_queue.append({'error': what})
            except:
                print ('multithread error: unknown error')

    # 整理命令行，提取多进程函数
    def sortcmds (self, cmds = []):
        headlist = []
        bodylist = []
        footlist = []
        for cmd in cmds:
            cmdobj = self.parsecmd(cmd)
            ctype = cmdobj['ctype']
            if ctype.find('load') == 0:
                headlist.append(cmd)
            elif ctype == 'execunit':
                headlist.append(cmd)
            elif ctype.find('save') == 0:
                footlist.append(cmd)
            else:
                bodylist.append(cmd)
        return {
            'mthread': headlist,
            'serial': bodylist,
            'mprocess': footlist,
        }

    # 简单处理，命令行全展开，看最大调用次数
    def checkloop (self, cmds = []):
        itercount = 0
        def checkrecursion (cmds = [], itercount = 0):
            itercount += 1
            if itercount > 100: # 最大递归深度
                raise Exception('Runtime Error: checkloop overflow max iter loops')
            for cmd in cmds:
                cmdobj = self.parsecmd(cmd)
                cmdkeys = cmdobj['ckeys']
                ctype = cmdobj['ctype']
                if ctype == 'execunit':
                    src = cmdkeys['src']
                    if src not in self.config['unitdata']:
                        raise Exception('Runtime Error: execunit src %s has not been set' % src)
                    cmds = self.config['unitdata'][src]
                    cmds = self.readcmdtext(cmds)
                    itercount = checkrecursion (cmds, itercount)
            return itercount
        itercount = checkrecursion(cmds, itercount)
        return itercount

if __name__ == '__main__':

    cache = {}
    t_ex = '../testdata/test.xlsx'
    t_cv = '../testdata/test.csv'
    cmds = [
        'loadexcel --src %s --tar excdata' % t_ex,
        'loadcsv --src %s --tar csvdata' % t_cv,
        'merge --tar dst1 --src excdata csvdata --join inner A C B',
        'group --tar dst2 --src dst1 --by A --cols B|count'
    ]
    t = CommandAgent()
    t.runcmds(cmds, cache, multithread = True)
    print (cache['dst1'], cache['dst2'])
