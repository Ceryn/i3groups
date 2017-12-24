#!/usr/bin/env python
import os, socket, json, i3ipc as i3

SOCKET_PATH = '/dev/shm/i3groups-watchfocus'

def group_name(wsname):
    return wsname.split('::')[-1] if '::' in wsname else ''

def workspace_handler(_, data):
    if data['change'] == 'focus':
        output = data['current']['output']
        name = data['current']['name']
        group = group_name(name)

        if not focus.has_key(group):
            focus[group] = dict()
        focus[group][output] = name

focus = dict()
if not i3.subscribe(['workspace'], workspace_handler):
    raise

if os.path.exists(SOCKET_PATH):
    os.unlink(SOCKET_PATH)
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.bind(SOCKET_PATH)
s.listen(1)
while True:
    c, _ = s.accept()
    c.send(json.dumps(focus))
    c.close()
