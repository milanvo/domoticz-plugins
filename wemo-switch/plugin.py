#!/usr/bin/python3
#
# Domoticz Python Plugin for WeMo Switch by Belkin
#
# Based on code from:
# https://gist.github.com/pruppert/af7d38cb7b7ca75584ef
# https://github.com/pdumoulin/blinky
#
# Author: mivo
#
"""
<plugin key="wemo-switch" name="WeMo Switch (plugin)" author="mivo" version="0.1" wikilink="http://www.domoticz.com/wiki/plugins" externallink="https://github.com/milanvo/domoticz-plugins">
    <params>
        <param field="Address" label="IP Address" width="200px" required="true"/>
        <param field="Port" label="Port" width="50px" required="true" default="49153"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import urllib.request

class wemoSwitch:
    ip = None
    ports = [49153, 49152, 49154, 49151, 49155]

    def __init__(self, switch_ip=None, switch_port=None):
        self.ip = switch_ip
        if switch_port:
            self.ports = [switch_port]

    def action(self, action):
        value = None

        if action == 'on':
            method, obj, value = ('Set', 'BinaryState', 1)
        elif action == 'off':
            method, obj, value = ('Set', 'BinaryState', 0)
        elif action == 'status':
            method, obj = ('Get', 'BinaryState')
        elif action == 'name':
            method, obj = ('Get', 'FriendlyName')
        elif action == 'signal':
            method, obj = ('Get', 'SignalStrength')

        return self._send(method, obj, value)

    def on(self):
        return self.action('on')

    def off(self):
        return self.action('off')

    def status(self):
        return self.action('status')

    def name(self):
        return self.action('name')

    def signal(self):
        return self.action('signal')

    def _get_header_xml(self, method, obj):
        method = method + obj
        return '"urn:Belkin:service:basicevent:1#%s"' % method

    def _get_body_xml(self, method, obj, value=0):
        method = method + obj
        return '<u:%s xmlns:u="urn:Belkin:service:basicevent:1"><%s>%s</%s></u:%s>' % (method, obj, value, obj, method)

    def _send(self, method, obj, value=None):
        body_xml = self._get_body_xml(method, obj, value)
        header_xml = self._get_header_xml(method, obj)
        for port in self.ports:
            result = self._try_send(self.ip, port, body_xml, header_xml, obj) 
            if result is not None:
                self.ports = [port]
            return result
        raise Exception("_send TimeoutOnAllPorts")

    def _try_send(self, ip, port, body, header, data):
        try:
            request = urllib.request.Request('http://%s:%s/upnp/control/basicevent1' % (ip, port))
            request.add_header('Content-type', 'text/xml; charset="utf-8"')
            request.add_header('SOAPACTION', header)
            request_body = '<?xml version="1.0" encoding="utf-8"?>'
            request_body += '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
            request_body += '<s:Body>%s</s:Body></s:Envelope>' % body
            request.data = request_body.encode()
            result = urllib.request.urlopen(request, timeout=3)
            return self._extract(result.read().decode(), data)
        except Exception as e:
#        except:
#            raise
            print(str(e))
            return None

    def _get_request_data(self, method, obj, value=None):
        body_xml = self._get_body_xml(method, obj, value)
        header_xml = self._get_header_xml(method, obj)
        headers = dict()
        
        url = '/upnp/control/basicevent1'
        headers['Content-type'] = 'text/xml; charset="utf-8"'
        headers['SOAPACTION'] = header_xml

        body = '<?xml version="1.0" encoding="utf-8"?>' \
               '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
        body += '<s:Body>%s</s:Body></s:Envelope>' % body_xml

        headers['Content-Length'] = "%d"%(len(body))
        
        return dict(url=url, headers=headers, body=body)

    def _extract(self, XML, tagName):
        #print('XML:', XML)
        #print('tagName:', tagName)
        startTag = '<%s>' % (tagName)
        endTag = '</%s>' % (tagName)
        startPos = XML.find(startTag)
        endPos = XML.find(endTag, startPos+1)
        #print('start end:', startPos, endPos)
        if ((startPos == -1) or (endPos == -1)):
            print("'"+tagName+"' not found in supplied XML")
            raise Exception("_extract" + "'"+tagName+"' not found in supplied XML")
            return False
        #if ((startPos == -1) or (endPos == -1)): Domoticz.Error("'"+tagName+"' not found in supplied XML")
        #print('vystup:', XML[startPos+len(startTag):endPos])
        return XML[startPos+len(startTag):endPos]

global switch
switch = wemoSwitch()

def onStart():
    global switch

    if Parameters["Mode6"] == "Debug":
        Domoticz.Debugging(1)
    if (len(Devices) == 0):
        Domoticz.Device(Name="Switch 1", Unit=1, TypeName="Switch").Create()
        Domoticz.Log("Device created.")
    Domoticz.Heartbeat(30)
    
    switch.ip = Parameters["Address"]
    switch.port = Parameters["Port"]

    try:
        status = switch.status()
    except Exception as e:
        Domoticz.Error('Except onStart: ' + str(e))
        return

    updStatus(status)

    DumpConfigToLog()

def onStop():
    Domoticz.Log("Plugin is stopping.")

def onCommand(Unit, Command, Level, Hue):
    global switch

    try:
        if (Command.upper() == 'ON'):
            status = switch.on()
        else:
            status = switch.off()
    except Exception as e:
        Domoticz.Error('Except onCommand: ' + str(e))
        return
    
    updStatus(status)

def onHeartbeat():
    global switch

    try:
        status = switch.status()
    except Exception as e:
        Domoticz.Error('Except onHeartbeat: ' + str(e))
        return

    updStatus(status)

def updStatus(status):
    if not status:
        Domoticz.Error('False updStatus: ' + str(status))
        return

    try:
        istatus = int(status)
    except ValueError:
        Domoticz.Error('Except updStatus: ' + str(status))
        return

    Domoticz.Debug('Status: ' + str(status))

    if istatus == 1:
        if (1 in Devices):
            if Devices[1].nValue == 0:
                Devices[1].Update(1,"100")
                Domoticz.Debug('Updated to: ' + str(istatus))
    elif istatus == 0:
        if (1 in Devices):
            if Devices[1].nValue == 1:
                Devices[1].Update(0,"0")
                Domoticz.Debug('Updated to: ' + str(istatus))

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def main():
    import argparse

    parser = argparse.ArgumentParser(description='WeMo Switch control module for Python')
    parser.add_argument('action', choices=['on', 'off', 'status', 'name', 'signal'], help='Action')
    parser.add_argument('ip', help='IP address')
    parser.add_argument('port', nargs='?', default='49153', help='Port')
    args = parser.parse_args()

    IP=args.ip
    PORT=args.port

    switch = wemoSwitch(IP, PORT)

    if args.action:
        print(switch.action(args.action))

if __name__ == '__main__':
    main()
