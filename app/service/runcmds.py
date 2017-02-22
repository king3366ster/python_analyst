# -*- coding: utf-8 -*-
import copy, os, sys, re, pdb
import msg_agent
from datalib.CommandAgent import CommandAgent
from datasettings.settings import setting_config

def init_execunit_fromfile ():
    base_path = 'datasettings/execunit'
    config = {}
    for file_name in os.listdir(base_path):
        if re.search(r'\.data$', file_name):
            with open('%s/%s' % (base_path, file_name)) as f:
                content = f.read()
                try:
                    content = content.decode('utf-8', 'ignore')
                except:
                    pass
                keyname = file_name.replace('.data', '')
                config[keyname] = content
    return config
# 执行单元为全局变量
execunit_config = init_execunit_fromfile()

# 重写执行命令单元集合
def rununit (cmdobj, cmdagent, msg_channel, cache = {}, extra = {}):
    cmdkeys = cmdobj['ckeys']
    if 'src' not in cmdkeys:
        raise Exception('Command Error: execunit without src')
    if 'tar' not in cmdkeys:
        raise Exception('Command Error: execunit without tar')
    src = cmdkeys['src']
    tar = cmdkeys['tar']
    if src not in cmdagent.config['unitdata']:
        raise Exception('Runtime Error: execunit src %s has not been set' % src)
    cmds = cmdagent.config['unitdata'][src]
    param_map = {} # 配置文件内设置参数
    if 'params' in cmdkeys:
        param_map = cmdagent.parse_params(cmdkeys['params'])
    cmds = cmdagent.readcmdtext(cmds, param_map)
    output = None
    for cmd in cmds:
        cobj = cmdagent.parsecmd(cmd)
        if 'tar' in cobj['ckeys']:
            output = cobj['ckeys']['tar']
    count = 0
    total = len(cmds)
    tmp_cache = {}
    for cmd in cmds:
        msg_agent.send_msg(
            msg_channel,
            'execunit: ' + cmd.replace('\"', '\\\\\"'), # 转义""
            extra = {
                'type': 'shell',
                'channel': extra['channel']
            }
        )
        result = cmdagent.runcmd(cmd, tmp_cache)
        if result is not None:
            message = '--target columns: %r' % list(result.columns)
            msg_agent.send_msg(
                msg_channel,
                message,
                extra = {
                    'type': 'shell',
                    'channel': extra['channel']
                }
            )
        count += 1
        msg_agent.send_msg(
            msg_channel,
            '%d/%d' % (count, total),
            extra = {
                'type': 'process',
                'channel': extra['channel']
            }
        )
    cache[tar] = tmp_cache[output]

def runcmds (cmds_text, msg_channel, cache = {}, extra = {}):
    cmdagent = CommandAgent(setting_config)
    for key in execunit_config:
        cmdagent.set_execunit(key, execunit_config[key])
    errmsg = ''
    try:
        # 只有一句execunit命令
        if cmds_text.find('execunit') == 0 and cmds_text.strip().find('\n') < 0:
            cmdobj = cmdagent.parsecmd(cmds_text)
            rununit(cmdobj, cmdagent, msg_channel, cache, extra = extra)
        else:
            # 解析文本
            cmds = cmdagent.readcmdtext(cmds_text)
            count = 0
            total = len(cmds)
            for cmd in cmds:
                result = cmdagent.runcmd(cmd, cache)
                if result is not None:
                    message = '--target columns: %r' % list(result.columns)
                    msg_agent.send_msg(
                        msg_channel,
                        message,
                        extra = {
                            'type': 'shell',
                            'channel': extra['channel']
                        }
                    )
                count += 1
                msg_agent.send_msg(
                    msg_channel,
                    '%d/%d' % (count, total),
                    extra = {
                        'type': 'process',
                        'channel': extra['channel']
                    }
                )
    except Exception as what:
        errmsg = 'runcmd error: %r' % what
        msg_agent.send_msg(
            msg_channel,
            errmsg.replace('\"', '\\\\\"'),
            extra = {
                'type': 'error',
                'channel': extra['channel']
            }
        )
