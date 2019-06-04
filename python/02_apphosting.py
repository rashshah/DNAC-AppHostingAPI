#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime
import sys
import json, re, os, time
from util import get_iox_url, call_script
from dnac_apphosting import list_app_on_dnac, find_app_ver_on_dnac, update_app_version
from docker_hub import get_docker_url

def auto_upgrade_app(appname, app_curr_ver):
    while True:
        print("checking available app versions on dockerhub")
        resp = get_docker_url(appname)
        #print("%s" % resp)
        for data in resp['results']:
            pattern = "^[.|0-9]+$"
            #print("dh version - %s" % data['name'])
            if re.match(pattern, data['name']):
                if data['name'] > app_curr_ver:
                    print("need to upgrade the app on dnac to latest version %s on dockerhub" % data['name'])
                    # call docker script to pull new version 
                    dir_path = os.path.dirname(os.path.realpath("docker_image_cmd.sh"))
                    call_script(os.path.join(dir_path, "docker_image_cmd.sh"), appname, data['name'])
                    # call dnac api to update and upgrade the app on all devices
                    new_docker_image_path = os.path.join(dir_path,appname+"_"+data['name']+".tar")
                    resp = update_app_version(appname, app_curr_ver, new_docker_image_path)
                    print("Successfully updated app %s on Cisco DNAC" % (appname))# resp["version"]))
                    break
            else:
                continue
        app_curr_ver = find_app_ver_on_dnac(appname)
        print("Current app version on DNAC - %s" % app_curr_ver)
        time.sleep(30)
    
    
if __name__ == "__main__":
    list_app_on_dnac()
    print("\n\n")
    if len(sys.argv) < 2:
        print("\n\nMissing arguments")
        print("Usage: python 02_apphosting.py appname")
    else:
        ret_ver = find_app_ver_on_dnac(sys.argv[1])
        if ret_ver == "-1":
            print("App %s not found on Cisco DNA-C controller" % sys.argv[1])
            sys.exit()
        else:
            pattern = "^[.|0-9]+$"
            if re.match(pattern, ret_ver):
                print("%s:%s" % (sys.argv[1], ret_ver))
            else:
                print("App %s with version %s cannot be monitored for auto upgrade" % (sys.argv[1], ret_ver))
                sys.exit()
            
            auto_upgrade_app(sys.argv[1], ret_ver)
     
       if new_ver != "":
            print ("Need to upgrade to %s" % new_ver)
            command = ('/usr/local/bin/docker pull %s:%s' % (sys.argv[1], new_ver))
            print(command)
            subprocess.call(command)
       else: 
            print ("No Upgarde needed")
          
