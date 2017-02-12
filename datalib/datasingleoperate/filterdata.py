# -*- coding:utf-8 -*- 
import re, pdb
import pandas as pd

def checkparams (func):
    def _checkparams (cmdobj, cache = None):
        ctype = cmdobj['ctype']
        if cache is None or (not isinstance(cache, dict)):
            raise Exception('Runtime Error: %s without cache' % ctype)
        if 'src' not in cmdobj['ckeys']:
            raise Exception('Command Error: %s without src' % ctype)
        src = cmdobj['ckeys']['src']
        if src not in cache:
            raise Exception('Runtime Error: %s not in cache' % src)
        return func(cmdobj, cache)
    return _checkparams

def parse_condition (condition, data = {}):
    tmp_char = ''
    tmp_char_pre = ''
    key_state = 'start' # 标记是否是列名
    quot_start = False # 标记引号开头
    for i in range(0, len(condition)):
        i_char = condition[i]
        if i_char == '\"' or i_char == '\'': # 是否被引号包围
            if quot_start == False:
                quot_start = True
                i_char = 'u' + i_char
            else:
                quot_start = False
        if quot_start == False:
            if re.match('[\)\|&]', i_char):
                key_state = 'start'
            elif re.match('[~!<=>]', i_char):
                key_state = 'end'
            if key_state == 'end':
                if tmp_char != '':
                    tmp_char = tmp_char.strip()
                    if tmp_char not in data:
                        raise Exception('Runtime Error: dsfilter %s not in cache' % tmp_char)
                    tmp_char = 'data[u\'%s\']' % tmp_char
                    tmp_char_pre += tmp_char
                    tmp_char = ''
                tmp_char_pre += i_char
            elif key_state == 'start':
                if re.match('[\(\)\s&\|]', i_char):
                    tmp_char_pre += i_char
                else:
                    tmp_char += i_char
        else:
            tmp_char_pre += i_char

    if tmp_char != '':
        tmp_char = 'data[u\'%s\']' % tmp_char
        tmp_char_pre += tmp_char
    if tmp_char_pre.find(']~=u') > 0:
        tmp_char_pre = tmp_char_pre.replace('~=u', '.str.contains(u') + ')'
    return 'data=data[%s]' % tmp_char_pre

@checkparams
def filterdata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    if 'cond' not in cmdkeys:
        raise Exception('Command Error: filterdata without cond')
    cond = cmdkeys['cond']
    data = cache[cmdkeys['src']].copy(deep = True)
    command = parse_condition(cond, data)
    exec(command)
    return data
