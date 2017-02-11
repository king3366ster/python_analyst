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

@checkparams
def filterdata (cmdobj, cache = None):
	cmdkeys = cmdobj['ckeys']
	if 'cond' not in cmdkeys:
		raise Exception('Command Error: filterdata without cond')
	cond = cmdkeys['cond']
	print cond
	print 'test'