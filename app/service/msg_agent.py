# -*- coding: utf-8 -*-
import pandas, numpy
import json
import runcmds

def format_msg(message, extra = {}):
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
    # 此处因为原始pd.DataFrame.to_json方法做改造
    elif 'type' != 'data':
        message = '"%s"' % message

    result = '{"code": %d, "data": %s, "type": "%s", "channel": %d}' % (channel_code, message, channel_type, channel_num)
    result = result.decode('unicode_escape')
    return {
        'text': result
    }

def send_msg(channel, message, extra = {}):
    message_sent = format_msg(message, extra)
    channel.reply_channel.send(message_sent)

def proxy_msg(msg_channel, cache = {}):
    content = msg_channel['text']
    channel = -1
    msg_type = 'text'
    message = ''
    try:
        json_data = json.loads(content)
        if 'channel' in json_data:
            channel = json_data['channel']
        if 'type' in json_data:
            msg_type = json_data['type']
        if 'message' in json_data:
            message = json_data['message']
        extra = {
            'channel': channel,
            'type': msg_type,
        }
        if msg_type == 'shell':
            runcmds.runcmds(message, msg_channel, cache, extra)

        elif msg_type == 'data':
            data = pandas.DataFrame(numpy.random.randn(6, 4), columns=list('ABCD')).to_json()
            send_msg(msg_channel, data, extra = extra)

        elif msg_type == 'command':
            data = 'command'
            send_msg(msg_channel, data, extra = extra)

        # send cache nodes
        cache_keys = list(cache.keys())
        send_msg(
            msg_channel, 
            cache_keys, 
            extra = {
                'channels': channel,
                'type': 'cache',
            }
        )
    except Exception as what:
        print 'error: %r' % what
