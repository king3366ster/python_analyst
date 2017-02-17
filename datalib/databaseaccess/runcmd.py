# -*- coding:utf-8 -*-
import loaddata, savedata
import os, sys, pdb

def runcmd(cmdobj, config = None, cache = None):
    ctype = cmdobj['ctype']
    result = None
    if ctype == 'loadexcel':
        result = loaddata.loadexcel(cmdobj, config)
    elif ctype == 'loadcsv':
        result = loaddata.loadcsv(cmdobj, config)
    elif ctype == 'loadmysql':
        result = loaddata.loadmysql(cmdobj, config)
    elif ctype == 'saveexcel':
        result = savedata.saveexcel(cmdobj, cache = cache)
    elif ctype == 'savecsv':
        result = savedata.savecsv(cmdobj, cache = cache)
    elif ctype == 'savemysql':
        result = savedata.savemysql(cmdobj, config = config, cache = cache)
    return result

if __name__ == '__main__':

    test_csv = os.path.join(os.getcwd(), 'testdata/test.csv')
    print (
        runcmd({
            'ctype': 'loadcsv',
            'ckeys': {
                'src': test_csv
            }
        })
    )
