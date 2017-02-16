# -*- coding: utf-8 -*-  
from channels.handler import AsgiHandler
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
import service.format_msg as fmg
import json

# websocket channel
# Connected to websocket.connect
@channel_session
@channel_session_user_from_http
def ws_connect(msg_channel):
    user = unicode(msg_channel.user) 
    msg_channel.channel_session['user'] = user
    fmg.send(msg_channel, {'code': '101'})

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(msg_channel):
    print 'disconnect'
    print msg_channel

@channel_session
def ws_receive(msg_channel):
    content = msg_channel['text']
    fmg.send(msg_channel, json.dumps({'hello': content}))
