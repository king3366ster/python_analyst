# -*- coding: utf-8 -*-  
import json
from channels.handler import AsgiHandler
import pdb
from channels import Channel, Group

def format(message, extra = {}):
    channel_num = -1
    channel_type = 'text'
    channel_code = 200
    if 'channel' in extra:
        channel_num = extra['channel']
    if 'type' in extra:
        channel_type = extra['type']
    if 'code' in extra:
        channel_code = extra['code']
    if isinstance(message, dict) or isinstance(message, list):
        message = json.dumps(message)

    result = '{"code": %r, "data": %s, "type": "%s", "channel": %r}' % (channel_code, message, channel_type, channel_num)
    result = result.decode('unicode_escape')
    return {
        'text': result
    }

def send(channel, message, extra = {}):
    message_sent = format(message, extra)
    channel.reply_channel.send(message_sent)