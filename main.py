#!/usr/bin/env python3
import time
import subprocess

from subprocess import Popen

# Open a copy of Gnome-Mines
p = Popen(['gnome-mines'])

# Find relevant IDs
pid = p.pid
wid = None
while (wid == None):
    time.sleep(1)

    wid_obj = subprocess.run(["./wid_from_pid.sh", str(pid)], stdout=subprocess.PIPE)
    wid = wid_obj.stdout.decode("utf-8")

# Parse out actual X11 Window ID
wid = int(wid.split('\n')[1].split(" ")[-1], base=16)
