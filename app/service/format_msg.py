# -*- coding: utf-8 -*-  
import json
from channels.handler import AsgiHandler
import pdb
from channels import Channel, Group

def format(message, extra = {}):
    channel_num = -1
    code = 200
    if 'channel' in extra:
        channel_num = extra['channel']

    if isinstance(message, unicode) or isinstance(message, str):
        return {
            'text': json.dumps({
                'text': message,
                'channel': channel_num,
                'code': 206
            })
        }
    else:
        if 'code' in message:
            code = message['code']
            del message['code']
        else:
            code = 200
        result = json.dumps({
                'json': message,
                'channel': channel_num,
                'code': code
            }).decode('unicode_escape')
        return {
            'text': result
        }

def send(channel, message):
    message_sent = format(message)
    channel.reply_channel.send(message_sent)