#!/usr/bin/env python3
import os
import PIL.Image
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

print(wid)

# Parse out actual X11 Window ID
wid = int(wid.split('\n')[-2].split(" ")[-1], base=16)

# Resize window, for consistency. Assume expert difficulty. Size magic numbers.
subprocess.run(['xdotool', 'windowsize', str(wid), str(1164), str(617)])

# Navigate to expert level
subprocess.run("xdotool mousemove --window {} 400 400".format(wid).split())
subprocess.run("xdotool click 1".split())
subprocess.run("xdotool mousemove --window {} 0 0".format(wid).split())

time.sleep(3)

top_left = (45, 90)
tile_size = 30
board_dims = (30, 16)

def pixel_tuple(im):
    px = im.load()
    grid = []
    for x in range(tile_size):
        grid.append(tuple([px[x,y][:3] for y in range(tile_size)]))
    return tuple(grid)

# Create tile dictionary
tile_dict = {}
for i in range(1,9):
    with PIL.Image.open("images/{}.png".format(i)) as f:
        tile_dict[pixel_tuple(f)] = i
with PIL.Image.open("images/known.png") as f:
    tile_dict[pixel_tuple(f)] = 0
with PIL.Image.open("images/unknown.png") as f:
    tile_dict[pixel_tuple(f)] = None

# Process image
def read_board():
    # Save window as png
    board_image = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".png")
    board_image.close()
    os.system("xwd -id {} | convert - {}".format(wid, board_image.name))
    with PIL.Image.open(board_image.name) as im:
        board = []
        for x in range(board_dims[0]):
            line = []
            for y in range(board_dims[1]):
                bounds = (
                    top_left[0] + tile_size * x,
                    top_left[1] + tile_size * y,
                    top_left[0] + tile_size * (x+1),
                    top_left[1] + tile_size * (y+1),
                )
                region = im.crop(bounds)
                px_tuple = pixel_tuple(region)
                # TODO Handle game over tiles
                line.append(tile_dict[px_tuple])
            board.append(line)
    os.remove(board_image.name)
    return board

def leftclick_tile(x, y):
    x = top_left[0] + tile_size * x + (tile_size // 2)
    y = top_left[1] + tile_size * y + (tile_size // 2)
    subprocess.run("xdotool mousemove --window {} {} {}".format(wid,x,y).split())
    subprocess.run("xdotool click 1".split())
    subprocess.run("xdotool mousemove --window {} 0 0".format(wid).split())

# TODO : main loop

read_board()
leftclick_tile(5, 5)
time.sleep(1)
b = read_board()
print(b)
