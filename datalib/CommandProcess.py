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
        # self.manager = multiprocessing.Manager()
        # self.msg_queue = self.manager.Queue()

    def run (self, params = [], cache = None, comm = False):
        if len(params) == 0:
            return None
        else:
            # self.pool = multiprocessing.Pool()
            for param in params:
                # proc = self.pool.apply_async(self.func_name, args = (param, self.msg_queue))
                proc = multiprocessing.Process(target = self.func_name, args = (param, cache, self.msg_queue))
                self.proc_list.append(proc)
                proc.daemon = comm
                proc.start()
            # self.pool.close()
            # self.pool.join()

            if comm: # 是否需要通信
                for proc in self.proc_list:
                    proc.join()
                cache = dict()
                self.msg_queue.put('STOP')
                msg_cache = None
                while msg_cache != 'STOP':
                    if not self.msg_queue.empty():
                        msg_cache = self.msg_queue.get()
                        if 'error' in msg_cache:
                            raise Exception(unicode(msg_cache['error']))
                        if isinstance(msg_cache, dict) == True:
                            cache = dict(cache, **msg_cache)
                return cache
            else:
                sys.stdout.flush()

    def stop(self):
        for proc in self.proc_list:
            if proc.is_alive():
                proc.terminate()
                print ('pid %d stoped' % proc.pid)
                proc.join()
        print ('process terminated')
        # self.pool.terminate()
        # print ('process pool terminated')

def testruncmd (cmd, cache = None, msg_queue = None):
    try:
        cmd = unicode(cmd)
        # print ('multiprocess start: %s' % cmd)
        time.sleep(1 + 2 * random.random())
        if cmd == 'groupe':
            raise Exception('test error')
        msg_queue.put({
            cmd: pd.DataFrame(np.random.randn(6, 4), columns=list('ABCD'))
        })
        print ('multiprocess end: %s' % cmd)
    except Exception as what:
        msg_queue.put({'error': what})

if __name__ == '__main__':

    t = CommandProcess(testruncmd)
    print (t.run([1, 'unit', 'group'], comm = True))