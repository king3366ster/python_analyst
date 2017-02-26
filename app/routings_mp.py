# -*- coding: utf-8 -*-
from channels.handler import AsgiHandler
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
import service.msg_agent as msg_agent
import multiprocessing, threading
import json, gc, sys, time

gc.enable()
gc.set_threshold(360, 8, 8)

# 全局缓存对象
# cache = {}
lock  = multiprocessing.Lock()
usermap = dict()

def stop_process(user):
    try:
        if user in usermap:
            usermap[user]['thread_stop'] = True
            time.sleep(0.003)
            proc = usermap[user]['process']
            # if proc.is_alive():
            usermap[user]['queue'].close()
            usermap[user]['thread_queue'].close()
            proc.terminate()
            proc.join()
            time.sleep(0.002)
            del usermap[user]['queue']
            del usermap[user]['thread_queue']
            del usermap[user]['channels']
            del usermap[user]
        gc.collect() # 手动回收内存
    except Exception as what:
        print (what)

def start_process (user):
    # 消息队列
    queue = multiprocessing.Queue()
    thread_queue = multiprocessing.Queue()

    usermap[user] = {
        'queue': queue,
        'process': None, # proc,
        'thread_queue': thread_queue,
        'thread': None, # thrd,
        'thread_stop': False,
        'channels': []
    }

    # 任务开启进程，内存自动回收
    multiprocessing.freeze_support()
    proc = multiprocessing.Process(target = process_event, args = (user, queue, thread_queue))
    usermap[user]['process'] = proc
    proc.daemon = True
    proc.start()
    # 线程侦听消息
    thrd = threading.Thread(target = thread_event, args = (user, thread_queue, usermap[user]['channels']))
    usermap[user]['thread'] = thrd
    thrd.setDaemon(True)
    thrd.start()

# websocket channel
# Connected to websocket.connect
@channel_session
@channel_session_user_from_http
def ws_connect(msg_channel):
    user = unicode(msg_channel.user)
    msg_channel.channel_session['user'] = user

    stop_process(user)
    start_process(user)
    usermap[user]['channels'].append(msg_channel)
    print ('Hello %s, You have connected' % user)
    # msg_channel.reply_channel.send({
    #     'text': json.dumps({
    #         'code': 101,
    #         'data': 'user %s connected' % user,
    #         'channel': -1,
    #         'type': 'shell',
    #     })
    # })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(msg_channel):
    user = unicode(msg_channel.channel_session['user'])
    stop_process(user)
    print 'user %s disconnect' % user    

@channel_session
def ws_receive(msg_channel):
    user = unicode(msg_channel.channel_session['user'])
    # msg_agent.proxy_msg(msg_channel, cache[user])
    queue = usermap[user]['queue']
    usermap[user]['channels'].append(msg_channel)
    channel_id = len(usermap[user]['channels']) - 1
    channel_msg = msg_channel['text']
    queue.put((channel_id, channel_msg))

# 专门接收消息并处理数据的进程
def process_event (user, queue, thread_queue):
    data_cache = {}
    count = 0
    msg_agent.send_msg({
            'id': 0,
            'queue': thread_queue,
        }, 
        'Hello %s, You have connected!' % user,
        {
            'type': 'shell'
        },
    )
    while True:
        count += 1
        if not queue.empty():
            channel_info = queue.get()
            channel_id = channel_info[0]
            channel_msg = channel_info[1]
            # thread_queue.put((channel_id, channel_msg)) # 测试
            msg_agent.proxy_msg({
                'text': channel_msg,
                'id': channel_id,
                'queue': thread_queue,
            }, data_cache)
        time.sleep(0.001)

# 专门用于侦听进程消息发送的线程，用于消息回复
def thread_event (user, thread_queue, channel_list):
    count = 0
    while not usermap[user]['thread_stop']:
        count += 1
        time.sleep(0.001)
        if not thread_queue.empty():
            channel_info = thread_queue.get()
            channel_id = channel_info[0]
            channel_msg = channel_info[1]
            channel = channel_list[channel_id]
            channel.reply_channel.send(channel_msg)
    print ('thread stoped')

