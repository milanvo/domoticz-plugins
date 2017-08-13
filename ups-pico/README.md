# Domoticz Python Plugin for UPS PIco HV3.0A (by Pimodules)
Plugin for monitoring and control of Pimodules UPS PIco HV3.0A http://pimodules.com/

## Features
- Monitoring BAT Voltage
- Monitoring RPi Voltage
- Monitoring NTC1 Temperature
- Monitoring Powering Mode
- Control User LEDs - Orange, Green, Blue
- Enable / Disable LEDs (LED_OFF register - 0x6B, 0x15)

## Requirements
- Tested and developed on RPi 3 with Raspbian 8 (Jessie)
- Domoticz stable 3.8153 or latest beta
- installed Python 3 smbus module: `sudo apt-get install python3-smbus`
- Working Python plugin system http://www.domoticz.com/wiki/Using_Python_plugins

## Installation
- in Domoticz folder `domoticz/plugins/` create folder `ups-pico`
- copy `plugin.py` to folder `domoticz/plugins/ups-pico`
- restart Domoticz

## Configuration
- Check menu Setup / Settings / System if "Accept new Hardware Devices" is enabled
- In menu Setup / Hardware add new device - type: UPS PIco HV3.0A (plugin), enter name of your choice (for example "UPS PIco")
- Open Setup / Log and watch for plugin start
```
2017-08-13 14:07:18.603 (UPS PIco) Started.
2017-08-13 14:07:18.854 (UPS PIco) Entering work loop.
2017-08-13 14:07:18.854 (UPS PIco) Initialized version 0.1, author 'mivo'
2017-08-13 14:07:18.874 (UPS PIco) PCB version: A
2017-08-13 14:07:18.874 (UPS PIco) Bootloader version: S
2017-08-13 14:07:18.874 (UPS PIco) FW version: 38
2017-08-13 14:07:18.875 (UPS PIco) Bat Powering running time (min): 5
```
- In Setup / Devices you should see new devices named like "hardware name - device name" for example:
    - UPS PIco - RPi Voltage
    - UPS PIco - NTC1 Temperature
    - UPS PIco - BAT Voltage
    - UPS PIco - Enabled LEDs
    - UPS PIco - Green LED
    - UPS PIco - Orange LED
    - UPS PIco - Blue LED
    - UPS PIco - Powering Mode

- Add devices by clicking on green right arrow and then you should see it on corresponding pages - Switches, Temperature, Utility
