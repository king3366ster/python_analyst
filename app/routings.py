# -*- coding: utf-8 -*-
from channels.handler import AsgiHandler
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
# import service.format_msg as format_msg
import service.msg_agent as msg_agent
import json

# 全局缓存对象
cache = {}

# websocket channel
# Connected to websocket.connect
@channel_session
@channel_session_user_from_http
def ws_connect(msg_channel):
    user = unicode(msg_channel.user)
    msg_channel.channel_session['user'] = user
    msg_agent.send_msg(msg_channel, 'user %s connected' % user, {'code': 101})
    cache[user] = {}

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
    print 'user %s disconnect' % user

@channel_session
def ws_receive(msg_channel):
    user = unicode(msg_channel.channel_session['user'])
    msg_agent.proxy_msg(msg_channel, cache[user])
