# -*- coding: utf-8 -*-
from channels.handler import AsgiHandler
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
import service.msg_agent_sp as msg_agent
import json, gc, sys

gc.enable()
gc.set_threshold(360, 8, 8)

# 全局缓存对象
cache = {}

# websocket channel
# Connected to websocket.connect
@channel_session
@channel_session_user_from_http
def ws_connect(msg_channel):
    user = unicode(msg_channel.user)
    msg_channel.channel_session['user'] = user
    if user in cache:
        del cache[user]
    cache[user] = {}

    print ('user %s connected' % user)
    msg_channel.reply_channel.send({
        'text': json.dumps({
            'code': 101,
            'data': 'user %s connected' % user,
            'channel': -1,
            'type': 'shell',
        })
    })
    gc.collect()

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(msg_channel):
    user = unicode(msg_channel.channel_session['user'])
    if user in cache:
    	if cache[user] is not None:
    		nodelist = [node for node in cache[user]]
    		for node in nodelist:
    			del cache[user][node]
        del cache[user]
    gc.collect() # 手动回收内存
    print 'user %s disconnect' % user

@channel_session
def ws_receive(msg_channel):
    user = unicode(msg_channel.channel_session['user'])
    msg_agent.proxy_msg({
        'text': msg_channel['text'],
        'channel': msg_channel
    }, cache[user])
