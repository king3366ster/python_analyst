# -*- coding:utf-8 -*- 
import groupdata, filterdata
import os, sys, pdb

def runcmd(cmdobj, cache = None):
    ctype = cmdobj['ctype']
    result = None
    if ctype == 'group':
        result = groupdata.groupdata(cmdobj, cache)
    elif ctype == 'resample':
        result = groupdata.resampledata(cmdobj, cache)
    elif ctype == 'topnrows':
        result = groupdata.topndata(cmdobj, cache)
    elif ctype == 'filter':
        result = filterdata.filterdata(cmdobj, cache)
    elif ctype == 'sort':
        result = filterdata.sortdata(cmdobj, cache)
    elif ctype == 'opcol':
        result = filterdata.opcoldata(cmdobj, cache)
    elif ctype == 'opnull':
        result = filterdata.opnulldata(cmdobj, cache)
    elif ctype == 'replace':
        result = filterdata.replacedata(cmdobj, cache)
    elif ctype == 'parsejson':
        result = filterdata.parsejsondata(cmdobj, cache)
    return result

if __name__ == '__main__':

    pass