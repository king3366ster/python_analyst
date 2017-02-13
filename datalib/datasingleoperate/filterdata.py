# -*- coding:utf-8 -*- 
import re, json, pdb
import numpy as np
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

def parse_setcol_command (command, data):
    # 先对列名、符号进行分词，生成列表
    tmp_char = ''
    tmp_char_type = 0 # 0 \s; 1 +-*/; 2 ()[]{} ;3 char
    tmp_char_type_pre = 0
    tmp_char_list = []
    for i in range(0, len(command)):
        i_char = command[i]
        if re.match('\s', i_char):
            continue
        if re.match('[\+\-\*\/]', i_char):
            tmp_char_type = 1
        elif re.match('[\(\)\[\]]', i_char):
            tmp_char_type = 2
        else:
            tmp_char_type = 3
        if tmp_char_type != tmp_char_type_pre:
            tmp_char_list.append(tmp_char)
            tmp_char = i_char
        else:
            tmp_char = tmp_char + i_char
        tmp_char_type_pre = tmp_char_type
    tmp_char_list.append(tmp_char)
    if tmp_char_list[0] == '':
        del tmp_char_list[0]

    operation = 'colnew = '
    tmp_char_type_pre = -1 # 优先级 3:() 2:*/ 1:+-
    for tmp_char in tmp_char_list:
        if re.match('[\[\]\(\)]', tmp_char):
            tmp_char_type = 3
        elif re.match('[\*\/]', tmp_char):
            tmp_char_type = 2
        elif re.match('[\+\-]', tmp_char):
            tmp_char_type = 1
        else:
            tmp_char_type = 0
        if tmp_char_type == 0: # keyname
            if re.match('^\d*(\.\d+)*$',tmp_char):
                operation = operation + tmp_char
            elif tmp_char.find('"') >= 0:
                operation = operation + tmp_char
            else:
                keyname = tmp_char.strip()
                if keyname not in data:
                    raise Exception('Command Error: opcoldata setcol %s not in data' % keyname)
                if data[keyname].dtype == 'timedelta64[ns]':
                    operation = operation + 'data[u\'%s\'] / np.timedelta64(1, \'s\')' % keyname
                else:
                    operation = operation + 'data[u\'%s\']' % keyname   
        else:
            operation = operation + tmp_char
    return operation

def parse_setcol_single (command, data = {}):
    errmsg = 'Command Error: opcoldata setcol '
    cmd = command
    if cmd.find('=') > 0:
        cmd_list = cmd.split('=')
        if len(cmd_list) != 2:
            raise Exception('%s assin val need like <dst> = <opfunc>' % errmsg)
        dst = cmd_list[0].strip()
        cmd = cmd_list[1].strip()
        exec(parse_setcol_command(cmd, data))
        if colnew.dtype == 'timedelta64[ns]':
            colnew = colnew / np.timedelta64(1, 's')
        if dst in data:
            data[dst] = colnew
        else:
            data.insert(len(data.columns), dst, colnew)
    elif cmd.find('->') > 0:
        cmd_list = cmd.split('->')
        if len(cmd_list) != 2:
            raise Exception('%s assin val need like <dst> -> <datatype>' % errmsg)
        dst = cmd_list[0].strip()
        cmd = cmd_list[1].strip()
        if dst not in data:
            raise Exception('Command Error: opcoldata setcol %s not in data' % dst)
        if cmd == 'int':
            data[dst] = data[dst].astype(int)
        elif cmd == 'str':
            data[dst] = data[dst].astype(unicode)
        elif cmd == 'float':
            data[dst] = data[dst].astype(float)
        elif cmd == 'time':
            data[dst] = pd.to_datetime(data[dst])
    return data

def parse_setcol (command, data = {}):
    cmds = command.split(',')
    for cmd in cmds:
        data = parse_setcol_single(cmd, data)
    return data

@checkparams
def filterdata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    data = cache[cmdkeys['src']].copy(deep = True)
    if 'cond' in cmdkeys:
        cond = cmdkeys['cond']
        command = parse_condition(cond, data)
        exec(command)
    if 'limit' in cmdkeys:
        limit = cmdkeys['limit'].strip()
        if not re.match(r'^\d+(\s+\d+)*$', limit):
            raise Exception('Command Error: filterdata limit command invalid')
        limits = re.split(r'\s+', limit)
        if len(limits) == 1:
            offset = 0
            limit = int(limits[0])
        else:
            offset = int(limits[0])
            limit = int(limits[1])
        data = data.iloc[offset : offset + limit]
    if 'cols' in cmdkeys:
        cols = cmdkeys['cols'].strip()
        cols = re.split(r'\s+', cols)
        for col in cols:
            if col not in data:
                raise Exception('Runtime Error: filter cols %s not in data' % col)
        data = data[cols]
    return data
   
@checkparams
def opcoldata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    data = cache[cmdkeys['src']].copy(deep = True)
    if 'setcol' in cmdkeys:
        command = cmdkeys['setcol']
        data = parse_setcol(command, data)
    if 'dropcol' in cmdkeys:
        command = cmdkeys['dropcol']
        columns = re.split(r'\s+', command)
        data.drop(columns, axis = 1, inplace = True)
    if 'leftcol' in cmdkeys:
        command = cmdkeys['leftcol']
        columns = re.split(r'\s+', command)
        data = data[columns]
    if 'rename' in cmdkeys:
        command = cmdkeys['rename']
        command = re.sub(r'\s*\->\s*', '->', command)
        cmds = re.split('\s+', command)
        for cmd in cmds:
            names = re.split('\s*->\s*', cmd)
            if len(names) == 2:
                nameA = names[1]
                nameB = names[0]
                data.rename(columns = {nameB: nameA}, inplace = True)
    return data

@checkparams
def opnulldata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    data = cache[cmdkeys['src']].copy(deep = True)
    if 'fill' in cmdkeys:
        fillword = cmdkeys['fill'].strip()
        if re.match(r'^[\'\"][^\'\"]*[\'\"]$', fillword):
            data.fillna(fillword[1:-1], inplace = True)
        elif re.match(r'^\d+$', fillword):
            data.fillna(int(fillword), inplace = True)
        elif re.match(r'^\d+\.\d+$', fillword):
            data.fillna(float(fillword), inplace = True)
        else:
            data.fillna(fillword, inplace = True)
    return data

@checkparams
def sortdata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    data = cache[cmdkeys['src']].copy(deep = True)
    if 'order' in cmdkeys:
        orderby = cmdkeys['order']
        orderbys = orderby.split(',')
        columns = []
        orders = []
        for order in orderbys:
            order = re.split(r'\s+', order.strip())
            if len(order) == 1:
                keyname = order[0]
                order = 1
            elif len(order) >1:
                keyname = order[0]
                if order[1] == 1 or order[1].lower() == 'desc':
                    order = 0
                else:
                    order = 1
            else:
                raise Exception('Command Error: sortdata without order keys')
            if keyname not in data:
                raise Exception('Runtime Error: sortdata %s not in data' % keyname)
            columns.append(keyname)
            orders.append(order)
        if len(columns) > 0:
            data.sort_values(by = columns, ascending = orders, inplace = True)
    return data

@checkparams
def replacedata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    data = cache[cmdkeys['src']].copy(deep = True)
    if 'setval' in cmdkeys:
        setval = cmdkeys['setval']
        setval = re.sub(r'\s*\->\s*', '->', setval)
        setvals = re.split(r'\s+', setval)
        for setcmd in setvals:
            if setcmd.find('->') > 0:
                setcmd = setcmd.split('->')
                if len(setcmd) == 2:
                    val1 = setcmd[0]
                    val2 = setcmd[1]
                    if val1 == 'null':
                        val1 = 'np.nan'
                    if val2 == 'null':
                        val2 = 'np.nan'
                    command = 'data = data.replace(%s,%s)' % (val1, val2)
                    exec(command)
                else:
                    raise Exception('Command Error: replacedata setval need like <val1> = <val2>')
    return data

@checkparams
def parsejsondata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    data = cache[cmdkeys['src']].copy(deep = True)
    if 'cols' in cmdkeys:
        cols = cmdkeys['cols']
        jsoncmds = re.split(r'\s+', cols)
        jsoncmds = map(lambda x: x.split('.'), jsoncmds)
        new_series = {}
        for jsoncmd in jsoncmds:
            column = jsoncmd[0]
            if column not in data:
                raise Exception('Runtime Error: parsejson %s not in data' % column)
            jsoncmd.insert(0, '_'.join(jsoncmd))
            new_series[jsoncmd[0]] = []

        for item in data.iterrows():
            item = item[1].to_dict()
            for jsoncmd in jsoncmds:
                keyname = jsoncmd[0]
                column = jsoncmd[1]
                try:
                    json_dict = json.loads(item[column])
                    for tmpkey in jsoncmd[2:]:
                        if json_dict is None:
                            break
                        if tmpkey in json_dict:
                            json_dict = json_dict[tmpkey]
                        else:
                            json_dict = None
                    if isinstance(json_dict, dict):
                        new_series[keyname].append(unicode(json_dict))
                    else:
                        new_series[keyname].append(json_dict)
                except:
                    new_series[keyname].append(None)
        new_data = pd.DataFrame(new_series, index = data.index)
        data = pd.concat([data, new_data], axis = 1)
    return data
                