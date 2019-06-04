#!/usr/bin/env python
from __future__ import print_function
import sys
import json
from util import get_iox_url
from dnac_apphosting import start_app_on_device, stop_app_on_device

def find_devices(app):
    return get_iox_url("appmgr/devices?searchByApp=%s" % app)

if __name__ == "__main__":
    if len(sys.argv) < 3:
       print("Missing arguments")
       print("Usage: python 01_apphosting.py appname start|stop")
    else:
       print("\nFinding all devices where Application is hosted")
       response = find_devices(sys.argv[1])
       for data in response['data']:
           deviceid = data['deviceId']
           print(deviceid)
           if (sys.argv[2] == 'start'):
              if (data['appStatus'] == 'RUNNING'):
                 print ("App %s already running on %s" % (sys.argv[1], data['hostname']))
              else:
                 print("\nStarting Application")
                 start_app_on_device(sys.argv[1], deviceid)
           else:
              if (data['appStatus'] == 'STOPPED'):
                 print ("App %s already in stopped state on %s" % (sys.argv[1], data['hostname']))
              else:
                 print("\nStopping Application")
                 stop_app_on_device(sys.argv[1], deviceid)

