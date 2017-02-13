# -*- coding:utf-8 -*- 
import mergedata
import os, sys, pdb

def runcmd(cmdobj, cache = None):
    ctype = cmdobj['ctype']
    result = None
    if ctype == 'merge':
        result = mergedata.mergedata(cmdobj, cache)
    elif ctype == 'concat':
        result = mergedata.concatdata(cmdobj, cache)
    return result

if __name__ == '__main__':

    pass