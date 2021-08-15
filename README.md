# Tools for correcting for un-even surfaces on a CNC machine

## Overview

The goal of this library is to probe a surface that will be cut using gcode, then adjust the gcode to account for unevenness of the surface.

This library was written for the Genmitsu 3018 Pro, however it could be easily be adapted to any machine that supports GCode over serial.

This code is not very clean. You can open an issue if you want me to clean it up.

Warning: this code has not been tested thoroughly. It may break your machine.

https://deepvlad.wordpress.com/making-pcb-circuit-boards-on-desktop-cnc-genmitsu-3018/

## Probing

Probing is done in probe.py.

For it to work, put in the right serial port at the top. I would start with the moveRoutine to make sure everythnig works.

Look at probe.py line 106. You have two main functions you could run.

1) moveRoutine(): this will allow you to move the machine with simple commands.
2) scanRoutine(x,w,y,h): probe a rectangle of points starting at x,y and ending at x+w,y+h. The number of points to probe is specified in the function itself.

Watch out! It will move the machine to a bunch of coordinates in between x,y and x+w,y+h. The origin is wherever the machine is when you run the python file. It will only lift up by 1mm before scanning, so make sure the machine can clear everything when z=1mm within that whole rectangle!

The output is a 2-d array of points of where it scanned.

## Warping gcode files

Copy the array from the probing part into height_warp.py.

Change the file names at the top of height_warp.py.

Run height_warp.py, and it will output the warped file.

I would do a diff with the unwarped file to make sure nothing crazy happened.
