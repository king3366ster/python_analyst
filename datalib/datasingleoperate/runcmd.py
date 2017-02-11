# -*- coding:utf-8 -*- 
import groupdata, filterdata
import os, sys, pdb

def runcmd(cmdobj, cache = None):
    ctype = cmdobj['ctype']
    result = None
    if ctype == 'dsgroup':
        result = groupdata.groupdata(cmdobj, cache)
    elif ctype == 'dsresample':
        result = groupdata.resampledata(cmdobj, cache)
    elif ctype == 'dstopn':
        result = groupdata.topndata(cmdobj, cache)
    # elif ctype == 'dmconcat':
    #     result = groupdata.concatdata(cmdobj, cache)
    return result

if __name__ == '__main__':

    pass