#!/usr/bin/env python
import sys, socket, json, i3msg as i3
from subprocess import Popen, PIPE

def print_help():
    print 'Usage: i3groups command [argument]'
    print 'Available commands are:'
    print '\n'.join(['    ' + k for k in cmds.keys()])

def get_input(prompt='', options=[]):
    p = Popen(['dmenu', '-p', prompt], stdout=PIPE, stdin=PIPE)
    res = p.communicate('\n'.join(sorted(set(options + ['']))))[0].strip()
    if p.returncode != 0:
        exit()
    return res

def group_name(wsname):
    return wsname.split('::')[-1] if '::' in wsname else ''

def assign_group(group=None):
    if group is None:
        groups = [group_name(x['name']) for x in wss]
        group = get_input('Assign ws to group:', groups)
    else:
        groups = filter(lambda x: group_name(x['name']).startswith(group), wss)
        ws = sorted(groups)[0] if groups else ''
        if ws:
            group = group_name(ws['name'])

    cmd = 'rename workspace to "%s%s"' % (focused_ws['name'].split('::')[0], '::' + group if group else '')
    i3.send(i3.RUN_COMMAND, cmd)

def next_workspace():
    nextprev_workspace(1)
def prev_workspace():
    nextprev_workspace(-1)
def nextprev_workspace(offset):
    group = group_name(focused_ws['name'])
    ingroup = filter(lambda x: group_name(x['name']) == group and x['output'] == focused_ws['output'], wss)
    wsnames = [x['name'] for x in ingroup]
    idx = (wsnames.index(focused_ws['name']) + offset) % len(wsnames)
    i3.send(i3.RUN_COMMAND, 'workspace "%s"' % wsnames[idx])

def get_last_focused(group):
    outputs = dict()
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect('/dev/shm/i3groups-watchfocus')
        data = s.recv(1024**2)
        s.close()
        outputs = json.loads(data)[group]
    except:
        pass

    members = filter(lambda x: group_name(x['name']).startswith(group), wss)
    for o in outputs.keys():
        if outputs[o] not in members:
            del outputs[o]
    for w in members:
        if not outputs.has_key(w['output']):
            outputs[w['output']] = w['name']
    return outputs

def focus_group(group=None):
    if group is None:
        groups = [group_name(x['name']) for x in wss]
        group = get_input('Focus group named:', groups)
    else:
        groups = filter(lambda x: group_name(x['name']).startswith(group), wss)
        ws = sorted(groups)[0] if groups else ''
        group = group_name(ws['name'])

    outputs = get_last_focused(group)
    focus = outputs.values()
    if outputs.has_key(focused_ws['output']):
        focus.append(outputs[focused_ws['output']])

    cmd = ''
    for w in focus:
        cmd += '; ' if cmd else ''
        cmd += 'workspace "%s"' % w
    i3.send(i3.RUN_COMMAND, cmd)

def rename_group():
    groups = [group_name(x['name']) for x in wss]
    newgroup = get_input('Rename group to:', groups)
    oldgroup = group_name(focused_ws['name'])
    members = filter(lambda x: group_name(x['name']) == oldgroup, wss)
    cmd = ''
    for m in members:
        cmd += '; ' if cmd else ''
        cmd += 'rename workspace "%s" to "%s"' % (m['name'], m['name'].split('::')[0] + ('::' + newgroup if newgroup else ''))
    i3.send(i3.RUN_COMMAND, cmd)

def rename_workspace():
    group = group_name(focused_ws['name'])
    newname = get_input('Rename workspace to:', [focused_ws['name'].split('::')[0]])
    if group and '::' not in newname:
        newname += '::%s' % group
    i3.send(i3.RUN_COMMAND, 'rename workspace to "%s"' % newname)

arg2 = sys.argv[2] if len(sys.argv) > 2 else None
cmds = dict()
cmds['focus_group'     ] = [focus_group,      arg2]
cmds['assign_group'    ] = [assign_group,     arg2]
cmds['next_workspace'  ] = [next_workspace,   None]
cmds['prev_workspace'  ] = [prev_workspace,   None]
cmds['rename_group'    ] = [rename_group,     None]
cmds['rename_workspace'] = [rename_workspace, None]

try:
    function, arg = cmds[sys.argv[1]]
except:
    print_help()
    exit()

wss = i3.send(i3.GET_WORKSPACES)
focused_ws = filter(lambda x: x['focused'], wss)[0]
function() if arg is None else function(arg)
