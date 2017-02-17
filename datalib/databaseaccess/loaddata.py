# -*- coding:utf-8 -*-
import pdb, re
import pandas as pd
import sqlalchemy

def checkparams (func):
    def _checkparams (cmdobj, config = {}):
        ctype = cmdobj['ctype']
        if 'src' not in cmdobj['ckeys']:
            raise Exception('Command Error: %s without src' % ctype)
        return func(cmdobj, config)
    return _checkparams

@checkparams
def loadexcel (cmdobj, config = {}):
    cmdkeys = cmdobj['ckeys']
    src = cmdkeys['src']
    if 'loadpath' in config:
        src = config['loadpath'] + src
    if not re.search(r'\.xlsx$', src):
        src = src + '.xlsx'
    if 'sheet' in cmdkeys:
        sheet = cmdkeys['sheet']
    else:
        sheet = 'Sheet1'
    return pd.read_excel(src, sheetname = sheet)

@checkparams
def loadcsv (cmdobj, config = None):
    cmdkeys = cmdobj['ckeys']
    src = cmdkeys['src']
    if 'loadpath' in config:
        src = config['loadpath'] + src
    if not re.search(r'\.csv$', src):
        src = src + '.csv'
    return pd.read_csv(src, encoding = 'gbk')

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

def loadmysql (cmdobj, config = None):
    cmdkeys = cmdobj['ckeys']
    db = cmdkeys['db']
    if config is None:
        raise Exception('Config Error: loadmysql without configs')
    elif db not in config:
        raise Exception('Command Error: loadmysql without correct db')
    elif 'query' not in cmdkeys:
        raise Exception('Command Error: loadmysql without query')
    mysql_engine = gen_engine_mysql(config[db])
    query = cmdkeys['query']
    return pd.read_sql(query, mysql_engine)
