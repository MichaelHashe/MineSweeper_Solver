#!/usr/bin/env python3
import os
import subprocess
import tempfile
import time

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
wid = int(wid.split('\n')[-2].split(" ")[-1], base=16)

# Resize window, for consistency. Assume expert difficulty. Size magic numbers.
subprocess.run(['xdotool', 'windowsize', str(wid), str(1164), str(617)])

# TODO : main loop
# Save window as png
board_image = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".png")
os.system(f"xwd -id {wid} | convert - {board_image.name}")

