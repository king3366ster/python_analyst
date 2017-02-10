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

@checkparams
def groupdata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    src = cmdkeys['src']
    data = cache[src].copy(deep = True)
    bykeys = getbykey(cmdobj, cache)
    if 'cols' not in cmdkeys:
        raise Exception('Command Error: dsgroup without cols')
    cols = cmdkeys['cols']
    cols = re.sub(r'\s*\|\s*', '|', cols)
    cols = re.split(r'\s+', cols)

    colfunc_dict = dict()
    for col in cols:
        rindex = col.rfind('|')
        if rindex > 0:
            method = col[rindex + 1:]
            column = col[:rindex]
        else:
            method = 'count'
            column = col
        if column not in data:
            raise Exception('Runtime Error: %s not in %s' % (column, src))
        colfunc_dict[column] = method
    print data
    grouped = data.groupby(bykeys)
    print grouped['C'].sum().reindex()
    print colfunc_dict