# -*- coding:utf-8 -*- 
import loaddata, savedata
import os, sys, pdb

def runcmd(cmdobj, config = None, cache = None):
    ctype = cmdobj['ctype']
    result = None
    if ctype == 'dbloadexcel':
        result = loaddata.loadexcel(cmdobj)
    elif ctype == 'dbloadcsv':
        result = loaddata.loadcsv(cmdobj)
    elif ctype == 'dbloadmysql':
        result = loaddata.loadmysql(cmdobj, config)
    elif ctype == 'dbsaveexcel':
        result = savedata.saveexcel(cmdobj, cache = cache)
    elif ctype == 'dbsavecsv':
        result = savedata.savecsv(cmdobj, cache = cache)
    elif ctype == 'dbsavemysql':
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