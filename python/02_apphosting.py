#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime
import sys
import subprocess
import json
from util import get_iox_url
from dnac_apphosting import list_app_on_dnac, find_app_ver_on_dnac
from docker_hub import get_docker_url

if __name__ == "__main__":
    list_app_on_dnac()
    print("\n\n")
    if len(sys.argv) < 2:
       print("Missing arguments")
       print("Usage: python 02_apphosting.py appname")
       
    else:
       ret_ver = find_app_ver_on_dnac(sys.argv[1])
       print("Version of %s on DNAC is %s" % (sys.argv[1], ret_ver))

       resp = get_docker_url(sys.argv[1])
    
       for data in resp['results']:
         if data['name'] == ret_ver:
            date = (data['last_updated'].split('.'))
	    datetime_obj = datetime.strptime(date[0], '%Y-%m-%dT%H:%M:%S')

       new_ver = ""
       for data in resp['results']:
         date = (data['last_updated'].split('.'))
         chk_date = datetime.strptime(date[0], '%Y-%m-%dT%H:%M:%S')
	 if chk_date > datetime_obj:
            new_ver = data['name']
            # Check if there are mutliple new version, it should
            # upgrade to latest
            datetime_obj = chk_date
     
       if new_ver != "":
            print ("Need to upgrade to %s" % new_ver)
            command = ('/usr/local/bin/docker pull %s:%s' % (sys.argv[1], new_ver))
            print(command)
            subprocess.call(command)
       else: 
            print ("No Upgarde needed")
          
