# -*- coding:utf-8 -*- 
import pdb, re
import pandas as pd
import openpyxl
from openpyxl.utils import get_column_letter
import sqlalchemy

def checkparams(func):
    def _checkparams(cmdobj, config = None, cache = None):
        ctype = cmdobj['ctype']
        if cache is None or (not isinstance(cache, dict)):
            raise Exception('Runtime Error: %s without cache' % ctype)
        if 'src' not in cmdobj['ckeys']:
            raise Exception('Command Error: %s without src' % ctype)
        src = cmdobj['ckeys']['src']
        if src not in cache:
            raise Exception('Runtime Error: %s %s not in cache' % (ctype, src))
        if 'tar' not in cmdobj['ckeys']:
            cmdobj['ckeys']['tar'] = cmdobj['ckeys']['src']
        return func(cmdobj, config = config, cache = cache)
    return _checkparams

def checkdb(func):
    def _checkdb(cmdobj, config = None, cache = None):
        ctype = cmdobj['ctype']
        if config is None:
            raise Exception('Config Error: %s without configs' % ctype)
        if 'db' not in cmdobj['ckeys']:
            raise Exception('Command Error: %s without db' % ctype)
        db = cmdobj['ckeys']['db']
        if db not in config:
            raise Exception('Command Error: %s without correct db' % ctype)
        return func(cmdobj, config = config, cache = cache)
    return _checkdb

@checkparams
def saveexcel (cmdobj, config = None, cache = None):
    ckeys = cmdobj['ckeys']
    src = ckeys['src']
    tar = ckeys['tar']
    if not re.search(r'\.xlsx$', tar):
        filename = tar + '.xlsx'
    else:
        filename = tar

    if 'if_exists' in ckeys:
        if_exists = ckeys['if_exists']
    else:
        if_exists = 'replace'
    if 'sheet' in ckeys:
        sheet_name = ckeys['sheet']
    else:
        sheet_name = 'Sheet1'
    data = cache[src]

    if if_exists == 'append':
        try:
            wb = openpyxl.load_workbook(filename)
            ws = wb.get_sheet_by_name(sheet_name)
        except Exception as what:
            wb = openpyxl.workbook.Workbook()
            ws = wb.create_sheet(sheet_name, 0)
    else:
        wb = openpyxl.workbook.Workbook()
        ws = wb.create_sheet(sheet_name, 0)

    dfIndexs = data.index
    dfColumns = data.columns
    dfValues = data.values

    for i in range(0, len(dfColumns)):
        index_col = i + 1
        index_row = 1
        col = get_column_letter(index_col + 1)
        ws['%s%s' %(col, index_row)] = dfColumns[i]

    for i in range(0, len(dfIndexs)):
        index_row = dfIndexs[i] + 2
        ws['A%d' % index_row] = dfIndexs[i]
        for j in range(0, len(dfColumns)):
            index_col = j + 1
            col = get_column_letter(index_col + 1)
            tmpValue = dfValues[i][j]
            try:
                ws['%s%s' %(col, index_row)] = tmpValue
            except Exception as what:
                print what
    wb.save(filename = filename)


@checkparams
def savecsv (cmdobj, config = None, cache = None):
    ckeys = cmdobj['ckeys']
    src = ckeys['src']
    tar = ckeys['tar']
    if not re.search(r'\.csv', tar):
        filename = tar + '.csv'
    else:
        filename = tar
    cache[src].to_csv(filename, index = False, encoding = 'gbk')
    return cache[src]

def gen_engine_mysql (config):
    if 'host' in config:
        _host = config['host']
    else:
        _host = '127.0.0.1'
    if 'user' in config:
        _user = config['user']
    else:
        _user = 'root'
    if 'pwd' in config:
        _pwd = config['pwd']
    else:
        _pwd = '123456'
    if 'db' in config:
        _db = config['db']
    else:
        _db = 'mysql'
    if 'port' in config:
        _port = config['port']
    else:
        _port = 3306
    mysql_engine = 'mysql://%s:%s@%s:%s/%s?charset=utf8' % (_user, _pwd, _host, _port, _db)
    # print (mysql_engine)
    return sqlalchemy.create_engine(mysql_engine)

@checkparams
@checkdb
def savemysql (cmdobj, config = None, cache = None):
    cmdkeys = cmdobj['ckeys']
    src = cmdkeys['src']
    tar = cmdkeys['tar']
    db = cmdkeys['db']
    mysql_engine = gen_engine_mysql(config[db])
    print (mysql_engine)





    