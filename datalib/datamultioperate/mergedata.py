# -*- coding:utf-8 -*- 
import re, pdb
import pandas as pd

joinway_set = set(['right', 'left', 'outer', 'inner'])

def get_src (cmdobj):
    cmdkeys = cmdobj['ckeys']
    srcs = cmdkeys['src']
    srcs = re.split(r'\s+', srcs)
    return set(srcs)

def get_joinway (cmdobj, cache):
    ctype = cmdobj['ctype']
    cmdkeys = cmdobj['ckeys']
    if 'join' not in cmdkeys:
        raise Exception('Command Error: %s without join' % ctype)
    joinways = re.split(r'\s+', cmdkeys['join'])
    if len(joinways) < 2 and ctype == 'mergedata':
        raise Exception('Command Error: %s join cmd need 2 more words' % ctype)
    elif len(joinways) < 1:
        raise Exception('Command Error: %s join cmd need 1 more words' % ctype)
    joinway = joinways[0]
    joinkeys = joinways[1:]
    return {
        'how': joinway,
        'on': joinkeys,
    }

def checkparams (func):
    def _checkparams (cmdobj, cache = None):
        ctype = cmdobj['ctype']
        if cache is None or (not isinstance(cache, dict)):
            raise Exception('Runtime Error: %s without cache' % ctype)
        if 'src' not in cmdobj['ckeys']:
            raise Exception('Command Error: %s without src' % ctype)
        srcs = get_src(cmdobj)
        for src in srcs:
            if src not in cache:
                raise Exception('Runtime Error: %s not in cache' % src)
        return func(cmdobj, cache)
    return _checkparams

@checkparams
def mergedata (cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    srcs = get_src(cmdobj)
    joinway = get_joinway(cmdobj, cache)
    for jkey in joinway['on']:
        for skey in srcs:
            if jkey not in cache[skey]:
                raise Exception('Runtime Error: mergedata %s not in node %s' % (jkey, skey))
    data = None
    for src in srcs:
        if data is None:
            data = cache[src].copy(deep = True)
        else:
            data = pd.merge(data, cache[src], how = joinway['how'], on = joinway['on'])
    return data

@checkparams
def concatdata(cmdobj, cache = None):
    cmdkeys = cmdobj['ckeys']
    srcs = get_src(cmdobj)
    joinway = get_joinway(cmdobj, cache)
    if 'axis' in cmdkeys:
        axis = int(cmdkeys['axis'])
    else:
        axis = 0
    srcs = map(lambda x: cache[x], srcs)
    return pd.concat(srcs, join = joinway['how'], axis = axis, ignore_index = True)