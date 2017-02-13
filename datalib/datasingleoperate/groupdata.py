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

def getbykey (cmdobj, cache = None):
    ctype = cmdobj['ctype']
    cmdkeys = cmdobj['ckeys']
    if 'by' not in cmdkeys:
        raise Exception('Command Error: %s without by' % ctype)
    src = cmdkeys['src']
    bykeys = re.split(r'\s+', cmdkeys['by'])
    for bkey in bykeys:
        if bkey not in cache[src]:
            raise Exception('Runtime Error: %s %s not in %s' % (ctype, bkey, src))
    return bykeys

def getcols (cmdobj, data = None):
    ctype = cmdobj['ctype']
    cmdkeys = cmdobj['ckeys']
    src = cmdkeys['src']
    if 'cols' not in cmdkeys:
        raise Exception('Command Error: %s without cols' % ctype)
    cols = cmdkeys['cols']
    cols = re.sub(r'\s*\|\s*', '|', cols)
    cols = re.split(r'\s+', cols)

    colfunc_list = []
    for col in cols:
        rindex = col.rfind('|')
        if rindex > 0:
            method = col[rindex + 1:]
            column = col[:rindex]
        else:
            method = 'count'
            column = col
        if column not in data:
            raise Exception('Runtime Error: %s %s not in %s' % (ctype, column, src))
        colfunc_list.append({
            'column': column,
            'method': method,
        })
    return colfunc_list

def generate_group (method, column, grouped = None, data = None):
    data_new = None
    if method == 'count':
        data_new = grouped[column].count()
    elif method == 'sum':
        data_new = grouped[column].sum()
    elif method == 'mean':
        data_new = grouped[column].mean()
    elif method == 'median':
        data_new = grouped[column].median()
    elif method == 'min':
        data_new = grouped[column].min()
    elif method == 'max':
        data_new = grouped[column].max()
    elif method == 'top':
        data_new = grouped[column].first()
    elif method == 'last':
        data_new = grouped[column].last()
    elif method == 'std':
        data_new = grouped[column].std()
    elif method == 'var':
        data_new = grouped[column].var()
    elif re.search(r'^top\d+$', method):
        num = int(re.findall(r'\d+', method)[0])
        num = max(num - 1, 1)
        data_new = grouped[column].nth(num)
    return data_new

@checkparams
def groupdata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    src = cmdkeys['src']
    data = cache[src].copy(deep = True)
    bykeys = getbykey(cmdobj, cache)

    colfunc_list = getcols(cmdobj, data)
    grouped = data.groupby(bykeys)
    col_data = dict()
    for item in colfunc_list:
        column = item['column']
        method = item['method']
        try:
            series = generate_group(method, column, grouped = grouped, data = data)
        except Exception as what:
            raise Exception('Runtime Error: dsgroup column %s cannot apply %s' % (column, method))
        if series is not None:
            col_data['%s_%s' % (column, method)] = series
    data_new = pd.DataFrame(col_data).reset_index()
    return data_new

@checkparams
def resampledata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    src = cmdkeys['src']
    data = cache[src].copy(deep = True)
    key_index = getbykey(cmdobj, cache)[0]
    data[key_index] = pd.to_datetime(data[key_index])
    data = data.set_index(key_index)

    if 'period' in cmdkeys:
        period = cmdkeys['period']
    else:
        period = 'M' # 1d 2d 

    colfunc_list = getcols(cmdobj, data)
    grouped = data.resample(period)
    col_data = dict()
    for item in colfunc_list:
        column = item['column']
        method = item['method']
        try:
            series = generate_group(method, column, grouped = grouped, data = data)
        except Exception as what:
            raise Exception('Runtime Error: %s column %s cannot apply %s' % (ctype, column, method))
        if series is not None:
            col_data['%s_%s' % (column, method)] = series
    data_new = pd.DataFrame(col_data).reset_index()
    return data_new

@checkparams
def topndata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    src = cmdkeys['src']
    data = cache[src].copy(deep = True)
    bykeys = getbykey(cmdobj, cache)
    if 'num' in cmdkeys:
        num = cmdkeys['num']
        if not re.search(r'^\s*\d+\s*$', num):
            raise Exception('Command Exception: topn num should be int type')
        else:
            num = int(num)
    else:
        raise Exception('Command Error: topn without num')
    grouped = data.groupby(bykeys)
    data_new = grouped.head(num)
    data_new.reset_index(inplace = True)
    return data_new