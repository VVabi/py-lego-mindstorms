# py-lego-mindstorms

I wanted to use the Lego 51515 Mindstorms brick without the Lego app and use it to talk to a Raspberry Pi while running: The brick for controlling the motors and for IMU data, the Pi for eg a camera. This repository is the result of quite a bit of googling and experimenting. I was unable to find a concise source explaining how to do what I wanted, so even when you don't want to use the actual code, the basic ideas might still be useful.

# File system and IDE

The brick uses micropython and has a full-fledged file system. Unfortunately it is not automatically mounted when connecting to a PC; I used upide https://github.com/harbaum/upide instead to access the file system via serial. Inside the IDE you can easily navigate the files. Note that by default files are only stored on the brick; manual backup support is actually integrated into the ide (right-click on the top-level directory -> backup).

# REPL (read-eval-print-loop) 

See eg http://docs.micropython.org/en/latest/reference/repl.html for an implementation on a different board; it is basically the same on the Lego brick.    
In the above-mentioned upide , you can go to interactive mode (the play button in the bottom-right corner) and tinker around on the command line. By default, the brick spams out its sensor data, so you probably want to interrupt the running python routine with strg-c to get a clean terminal. Then you can play around with the python shell; all python commands documented in the Lego app should work here as well.

Note that the brick powers down automatically fairly quickly when nothing is happening; I haven't found out yet how to disable this power-down.

Accessing the REPL also works via direct serial access (putty/screen/...); baud is 115200.

# main.py

The REPL is nice and all, but we want to write our own code running standalone on the board!

The most important file for our purposes is main.py. It is executed automatically upon boot; modifying it gives you control over the brick.
Note that with great power comes great responsibility; it is in principle possible to lock yourself out by doing something stupid in main.py. Should this happen, turn off the brick, hold the left arrow button and then turn it back on to boot to safe mode. Here main.py is not executed and you should get back access via the IDE, or you can connect to the LEGO app for a full factory reset - the App will always ask you to "update" the device when it recognizes the default main.py script is not running - the programs you write yourself in the App are actually called inside hub_runtime from main.py. 

You very likely want to get rid of hub_runtime.start() in main.py; this is responsible for the measurement data spam and also intercepts incoming traffic via USB/bluetooth. However, you still need a call to hub_runtime.init(0) - found by experimentation: Many things work without this, but eg Motor.run_to_position doesn't. The hub_runtime module is unfortunately only available in compiled format, and I haven't been able yet to decompile it, so I don't fully know what is going on. But so far, the call to hub_runtime.init seems to do the trick.

I also had some weird issues with python import paths; rebooting the brick both fixed some errors and helped to find new ones since eg import statements done on the cmd line are available until the next reboot.

As mentioned above, the Lego app will always ask you to update the brick when hub_runtime is not running; you will lose all data if you do so!

# Talking to the outside world

As a virtual comm port, via USB - bluetooth should also be possible:

import hub  
vcp = hub.USB_VCP()  
if USB_VCP.isconnected()  
x = vcp.read(1)  
&nbsp;&nbsp;&nbsp;&nbsp;if x is not None:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vcp.write(x)  

mirroring back all written characters.

See https://lego.github.io/MINDSTORMS-Robot-Inventor-hub-API/class_usb_vcp.html  From here, you can implement your own custom protocol to talk to another device.

# Go ahead and create!

You can find documentation on how to use sensors and motors in the official Lego App python docs. It should also be possible to upload custom sounds, or maybe a "video" file to play on the display, or a file with preprogrammed motor movements, or whatever else you can think of. 