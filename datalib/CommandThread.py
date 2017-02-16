# -*- coding:utf-8 -*- 
import os, sys, time, pdb
import random
import numpy as np
import pandas as pd
import threading

class CommandThread:
    def __init__ (self, func_name):
        self.func_name = func_name
        self.threads = []
        self.lock = threading.Lock()
        self.msg_queue = []

    def run (self, params = []):
        if len(params) == 0:
            return None
        else:
            for param in params:
                proc = threading.Thread(target = self.func_name, args = (param, self.msg_queue, self.lock))
                self.threads.append(proc)
                proc.setDaemon(True)
                proc.start()
            for proc in self.threads:
                proc.join()

            cache = dict()
            while len(self.msg_queue) > 0:
                msg_cache = self.msg_queue.pop()
                if 'error' in msg_cache:
                    raise Exception(unicode(msg_cache['error']))
                if isinstance(msg_cache, dict) == True:
                    cache = dict(cache, **msg_cache)
            return cache

    def stop(self):
        for proc in self.threads:
            if proc.is_alive():
                proc.stop()
        print ('process terminated')

def testruncmd (cmd, msg_queue, lock = None):
    try:
        cmd = unicode(cmd)
        time.sleep(1 + 2 * random.random())
        if cmd == 'group':
            raise Exception('test error')
        if lock is None:
            msg_queue.append({
                cmd: pd.DataFrame(np.random.randn(6, 4), columns=list('ABCD'))
            })
        else:
            with lock:
                msg_queue.append({
                    cmd: pd.DataFrame(np.random.randn(6, 4), columns=list('ABCD'))
                })
            
        print ('multiprocess end: %s' % cmd)
    except Exception as what:
        msg_queue.append({'error': what})

if __name__ == '__main__':

    t = CommandThread(testruncmd)
    print (t.run([1, 'unit', 'group']))