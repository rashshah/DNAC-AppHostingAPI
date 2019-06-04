import requests
import json
import time
import logging
from dnac_config import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD
from requests.auth import HTTPBasicAuth
from util import get_iox_url, post_and_wait_iox, post_req_iox, post_multipart_file
requests.packages.urllib3.disable_warnings()

# -------------------------------------------------------------------
# Custom exception definitions
# -------------------------------------------------------------------
class TaskTimeoutError(Exception):
    pass

class TaskError(Exception):
    pass

# API ENDPOINTS
ENDPOINT_TICKET = "ticket"
ENDPOINT_TASK_SUMMARY ="task/%s"
RETRY_INTERVAL=2

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def get_app_info(appname):
     response = get_iox_url("appmgr/myapps?searchByName=%s" % appname)
     print("get app info - %s" % response)
     return response['myappId']
     
def update_app_version(appname, curr_ver, filepath):
    localappid = get_local_appid_on_dnac(appname)
    files = {'file': open(filepath, 'rb')}
    url =("appmgr/apps/%s/%s/package?type=docker&action=update" % (localappid, curr_ver))
    return post_multipart_file(url, files)

def start_app_on_device(appname, deviceid):
     appid = get_app_info(appname)
     data = { "action" : "start" }
     url = ("appmgr/devices/%s/apps/%s/action" % (deviceid, appid))
     post_req_iox(url, data)

def stop_app_on_device(appname, deviceid):
     appid = get_app_info(appname)
     data = { "action" : "stop" }
     url = ("appmgr/devices/%s/apps/%s/action" % (deviceid, appid))
     post_req_iox(url, data)

def list_app_on_device(deviceid):
     url = ("appmgr/devices/%s/apps" % deviceid)
     response=get_iox_url(url)
     print(response)
        
def list_app_on_dnac():
     url = ("appmgr/apps")
     response=get_iox_url(url)
     for data in response['data']:
       if 'descriptor' not in data:
           continue
       desc = data['descriptor']
       if 'info' not in desc:
           continue
       info = desc ['info']
       print("%s:%s" % (info['name'], info['version']))
       
def find_app_ver_on_dnac(appname):
     url = ("appmgr/apps")
     response=get_iox_url(url)
     for data in response['data']:
       if 'descriptor' not in data:
           continue
       desc = data['descriptor']
       if 'info' not in desc:
           continue
       info = desc ['info']
       if info['name'] == appname:
           #lprint("app response from dnac - %s" % data)
           return info['version']
     return("-1")

def get_local_appid_on_dnac(appname):
     url = ("appmgr/apps")
     response=get_iox_url(url)
     for data in response['data']:
       if 'descriptor' not in data:
           continue
       desc = data['descriptor']
       if 'info' not in desc:
           continue
       info = desc ['info']
       if info['name'] == appname:
           #lprint("app response from dnac - %s" % data)
           return data['localAppId']
     return("-1")
