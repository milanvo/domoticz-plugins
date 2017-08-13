# Domoticz Python Plugin for WeMo Switch (by Belkin)

## Features
- Domoticz Switch device for WeMo

## Requirements
- Tested and developed on RPi 3 with Raspbian 8 (Jessie)
- Domoticz stable 3.8153 or latest beta
- Working Python plugin system http://www.domoticz.com/wiki/Using_Python_plugins

## Installation
- in Domoticz folder `domoticz/plugins/` create folder `wemo-switch`
- copy `plugin.py` to folder `domoticz/plugins/wemo-switch`
- restart Domoticz

## Configuration
- Check menu Setup / Settings / System if "Accept new Hardware Devices" is enabled
- In menu Setup / Hardware add new device - type: WeMo Switch (plugin), enter name of your choice (for example "wemo").
Specify IP address and port (default is 49153).
- Open Setup / Log and watch for plugin start
```
2017-08-13 14:24:23.135 (wemo) Started.
2017-08-13 14:24:23.627 (wemo) Entering work loop.
2017-08-13 14:24:23.627 (wemo) Initialized version 0.1, author 'mivo'
```
- In Setup / Devices you should see new device named like "hardware name - device name" for example:
    - wemo - Switch 1

- Add device by clicking on green right arrow and then you should see it on corresponding page - Switches
