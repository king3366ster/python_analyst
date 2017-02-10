# -*- coding:utf-8 -*- 
import mergedata
import os, sys, pdb

def runcmd(cmdobj, cache = None):
    ctype = cmdobj['ctype']
    result = None
    if ctype == 'dmmerge':
        result = mergedata.mergedata(cmdobj, cache)
    elif ctype == 'dmconcat':
        result = mergedata.concatdata(cmdobj, cache)
    return result

if __name__ == '__main__':

    pass