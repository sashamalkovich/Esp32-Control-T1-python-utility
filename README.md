# Esp32 Control T1 Desktop python utility

Desktop Utility for Esp32 WiFi MIDI controller

Python 3.7, PyQt 5.13.0, Pyserial 3.4

https://github.com/sashamalkovich/esp32-MIDI-Control

Device parameters can be changed using the desktop utility written in Python. The utility also allows you to enter the WiFi login and password. Once connected, displays the IP address and port required for Apple MIDI in the appropriate fields.


Created using PyCharm Comunity. Recommended to compile using pyinstaller.

Tested on mac os 10.14, 10.13, 10.11, Windows 10


For use in Windows, inside file checkPorts.py 'CP2102' must be replaced with 'Silicon'

