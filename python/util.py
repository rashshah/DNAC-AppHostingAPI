from __future__ import print_function

import os
import sys
import requests
import json
import subprocess

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
#from tests.fake import fake, fake_post
#FAKE=True
FAKE=False


from dnac import get_auth_token, create_url, wait_on_task, create_iox_url

def get_url(url):

    if FAKE:
        return fake[url]
    url = create_url(path=url)
    print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

def get_iox_url(url):

    if FAKE:
        return fake[url]
    url = create_iox_url(path=url)
    print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

def post_and_wait(url, data):
    if FAKE:
        return fake_post[url]
    token = get_auth_token()
    url = create_url(path=url)
    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    taskid = response.json()['response']['taskId']
    print ("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token)

    return task_result

def post_req_iox(url, data):
    if FAKE:
        return fake_post[url]
    token = get_auth_token()
    url = create_iox_url(path=url)
    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    print (response.json())

def post_and_wait_iox(url, data):
    if FAKE:
        return fake_post[url]
    token = get_auth_token()
    url = create_iox_url(path=url)
    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    print (json.dumps(response.json()))
    taskid = response.json()['response']['taskId']
    print ("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token)

    return task_result

def post_multipart_file(url, files):
    token = get_auth_token()
    url = create_iox_url(path=url)
    headers= { 'x-auth-token': token['token']}
    print("url - %s" % url)
    try:
        response = requests.post(url, files=files, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)
    
    resp_json = json.dumps(response.json())
    return resp_json
    
def call_script(script, *args, **env):
    """
    Calls script with environment variables defined in env (if any) 
    and returns output,returncode.
    """
    
    print("call_script: cmd:%s args:%s env:%s" % (script, args, env))
    if type(script) is list:
        li = script
    else:
        # string
        li = [script]
    li.extend(args)
    
    if env:
        li = ' '.join(li)
        env_str = ''
        for key, value in env.items():
            env_str += str(key) + '=' + str(value) + ' '    
        li = env_str + li
        
    try:
        if env:
            print("Executing script : %s" % li)
            rval = subprocess.check_output(li, stderr=subprocess.STDOUT, shell=True)
        else:
            print("Executing script : %s" % " ".join(li))
            rval = subprocess.check_output(li, stderr=subprocess.STDOUT)
        return rval, 0
    except subprocess.CalledProcessError as c:
        return c.output, c.returncode
    except Exception as ex:
        print("Error executing script : %s, exception - %s" % (" ".join(li), ex))
        return str(ex), -1
