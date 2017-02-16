# -*- coding: utf-8 -*-  
import format_msg
import pandas, numpy
import json

def proxy_msg(msg_channel):
    content = msg_channel['text']
    channel = -1
    msg_type = ''
    try:
        json_data = json.loads(content)
        if 'channel' in json_data:
            channel = json_data['channel']
        if 'type' in json_data:
            msg_type = json_data['type']
        extra = {
            'channel': channel
        }
    except:
        pass
    if msg_type == 'command':
        data = '"est"'
        format_msg.send(msg_channel, data, extra = extra)
    elif msg_type == 'pulldata':
        data = pandas.DataFrame(numpy.random.randn(6, 4), columns=list('ABCD')).to_json()
        format_msg.send(msg_channel, data, extra = extra)

