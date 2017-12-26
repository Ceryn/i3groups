i3groups
===
A project based workflow for [i3wm](https://i3wm.org/).

About
---
[i3wm](https://i3wm.org/) comes with workspaces. i3groups lets you assign these workspaces to groups for a more structured workflow while still letting you use all workspaces and other i3 features like you're used to.

i3groups lets you:
* assign workspaces to named groups
* focus groups by name or number, brining its last focused workspace into view for all outputs
* focus individual workspaces like you're used to<sup>\*</sup>
* rename groups and workspaces
* cycle through workspaces in active group and output
* cycle through outputs<sup>\*</sup>
* spawn new workspaces with the next available number<sup>\*\*</sup>
* save/restore the i3 tree like you're used to<sup>\*</sup>

i3groups consists of a ~120 and a ~30 line Python script for managing groups, a ~90 line patch to the i3bar C source to handle grouped workspaces correctly and ~30 i3 keybindings.

<sub>\* Some of these features are enabled by native i3, but have been incorporated in the i3groups workflow as they work particularly well with other features.</sub>  
<sup>\*\* Thanks to nervengift for making a cleaner solution to figuring out the next workspace number.</sup>

Demo
---
TODO. VIDEO DEMONSTRATION PENDING.

Dependencies
---
i3groups depends on [i3msg-python](https://github.com/Ceryn/i3msg-python).  
If you don't want to set up i3msg-python on your system you can just wget the relevant file as demonstrated in the installation section.

Installation
---
Get source files:
```Bash
cd ~/
git clone https://github.com/Ceryn/i3groups.git
```

[Set up i3msg-python](https://github.com/Ceryn/i3msg-python) (`pip install i3msg --user`) or just wget the script:
```Bash
wget https://raw.githubusercontent.com/Ceryn/i3msg-python/master/i3msg.py
touch __init__.py
```

Make a link to `i3groups.py` somewhere in your `PATH`:
```Bash
sudo ln -s ~/i3groups/i3groups.py /usr/local/bin/i3groups
```

Add i3groups keybindings to your i3 config:
```Bash
cat keybindings.conf >> ~/.config/i3/config
i3-msg reload
```

i3groups is now active and running, but i3bar will need some love, since group names are appended to workspace names and i3bar needs to handle that.  
Re-compile i3bar with the i3groups patch to make it great again (Debian assumed, your mileage may vary):
```Bash
sudo apt build-dep i3
wget https://github.com/i3/i3/archive/4.14.1.tar.gz
tar -xzvf 4.14.1.tar.gz
patch -p0 -i i3groups.patch
cd i3-4.14.1
autoreconf -fi
mkdir build
cd build
../configure
make -j8
sudo make install
i3-msg restart
```

Finally, and optionally, if you want i3groups to remember which workspaces last had focus for each group on each monitor you will need to run `i3groups-watchfocus.py` somewhere in the background. You can omit this step, but then i3groups will just pick the first workspace in the group for each monitor when you focus a group:
```Bash
echo '~/i3groups/i3groups-watchfocus.py &' >> ~/.profile
~/i3groups/i3groups-watchfocus.py &
```

And that's it. At this point everything should be working as expected.

Usage
---
i3groups will issue a `dmenu` prompt whenever input is needed except if `name` is provided.  
Command line interface:
```Bash
i3groups assign_group [name]
i3groups focus_group [name]
i3groups rename_group
i3groups rename_workspace
i3groups prev_workspace
i3groups next_workspace
```

Default keybinding modifiers:
```i3
### MODIFIERS ##################################################
set $mod   Mod1
set $ctrl  Control
set $shift Shift
```

Default keybindings (pasted from `keybindings.conf`):
```i3
### OUTPUTS ####################################################
bindsym $mod+$ctrl+j                focus output left
bindsym $mod+$ctrl+semicolon        focus output right
bindsym $mod+$ctrl+$shift+j         move workspace to output left
bindsym $mod+$ctrl+$shift+semicolon move workspace to output right

### GROUPS #####################################################
bindsym $mod+$ctrl+k        exec i3groups prev_workspace
bindsym $mod+$ctrl+l        exec i3groups next_workspace
bindsym $mod+$ctrl+r        exec i3groups rename_workspace
bindsym $mod+$ctrl+$shift+r exec i3groups rename_group
bindsym $mod+$ctrl+a        exec i3groups assign_group
bindsym $mod+$ctrl+f        exec i3groups focus_group

bindsym $mod+$ctrl+1  exec i3groups focus_group  1
bindsym $mod+$ctrl+2  exec i3groups focus_group  2
bindsym $mod+$ctrl+3  exec i3groups focus_group  3
bindsym $mod+$ctrl+4  exec i3groups focus_group  4
bindsym $mod+$ctrl+5  exec i3groups focus_group  5
bindsym $mod+$ctrl+6  exec i3groups focus_group  6
bindsym $mod+$ctrl+7  exec i3groups focus_group  7
bindsym $mod+$ctrl+8  exec i3groups focus_group  8
bindsym $mod+$ctrl+9  exec i3groups focus_group  9
bindsym $mod+$ctrl+10 exec i3groups focus_group 10

bindsym $mod+$ctrl+$shift+1  exec i3groups assign_group  1
bindsym $mod+$ctrl+$shift+2  exec i3groups assign_group  2
bindsym $mod+$ctrl+$shift+3  exec i3groups assign_group  3
bindsym $mod+$ctrl+$shift+4  exec i3groups assign_group  4
bindsym $mod+$ctrl+$shift+5  exec i3groups assign_group  5
bindsym $mod+$ctrl+$shift+6  exec i3groups assign_group  6
bindsym $mod+$ctrl+$shift+7  exec i3groups assign_group  7
bindsym $mod+$ctrl+$shift+8  exec i3groups assign_group  8
bindsym $mod+$ctrl+$shift+9  exec i3groups assign_group  9
bindsym $mod+$ctrl+$shift+10 exec i3groups assign_group 10

### WORKSPACES #################################################
# Create new workspace with the next available number. Thanks to nervengift.
bindsym $mod+$ctrl+Return exec "i3-msg workspace $(i3-msg -t get_workspaces | jq 'map(.num) | . + [0] | sort | . - [-1] | map(.+1) - . | .[0]')"
```

Additional keybindings for 12 more easy-access workspaces are recommended:
```i3
bindsym $mod+F1       workspace number 11
bindsym $mod+F2       workspace number 12
#[...]

bindsym $mod+Shift+F1 move container to workspace number 11
bindsym $mod+Shift+F2 move container to workspace number 12
#[...]
```

Contributing
---
Contributions are very welcome.  
You can reach out with your ideas/requests/improvements on Freenode IRC (Ceryn, #i3) or here.
