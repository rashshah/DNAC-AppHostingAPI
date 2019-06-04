import requests
import json
import time
import logging
from requests.auth import HTTPBasicAuth
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
def create_docker_url (appname):
    """ Helper function to create a DNAC API endpoint URL
    """

    return "https://hub.docker.com/v2/repositories/library/%s/tags?page_size=100000" % (appname)


def get_docker_url(appname):
    url = create_docker_url(appname)
    #print(url)
    try:
        response = requests.get(url, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()
    

