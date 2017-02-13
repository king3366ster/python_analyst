# -*- coding:utf-8 -*- 
import os, sys, time, pdb
import random
import numpy as np
import pandas as pd
import multiprocessing

class CommandProcess:
    def __init__ (self, func_name):
        self.func_name = func_name
        self.proc_list = []
        self.msg_queue = multiprocessing.Queue()

    def run (self, params = []):
        if len(params) == 0:
            return None
        else:
            proc_num = len(params)
            for param in params:
                proc = multiprocessing.Process(target = self.func_name, args = (param, self.msg_queue))
                self.proc_list.append(proc)
                proc.daemon = False
                proc.start()
            for proc in self.proc_list:
                proc.join()

            cache = dict()
            while proc_num > 0:
                if not self.msg_queue.empty():
                    msg_cache = self.msg_queue.get()
                    if 'error' in msg_cache:
                        raise Exception(unicode(msg_cache['error']))
                    cache = dict(cache, **msg_cache)
                    proc_num -= 1
            return cache

    def stop(self):
        for proc in self.proc_list:
            if proc.is_alive():
                proc.terminate()
                print ('pid %d stoped' % proc.pid)
                proc.join()
        print ('process stoped')

def testruncmd (cmd, msg_queue):
    try:
        cmd = unicode(cmd)
        # print ('multiprocess start: %s' % cmd)
        time.sleep(1 + 2 * random.random())
        if cmd == 'group':
            raise Exception('test error')
        msg_queue.put({
            cmd: pd.DataFrame(np.random.randn(6, 4), columns=list('ABCD'))
        })
        print ('multiprocess end: %s' % cmd)
    except Exception as what:
        msg_queue.put({'error': what})

if __name__ == '__main__':

    t = CommandProcess(testruncmd)
    print (t.run([1, 'group', 'unit']))