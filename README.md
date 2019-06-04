# Get Started with Cisco Application Hosting API for DNA Center

This repository contains a few simple scripts to get started with Cisco Application Hositng API.
Cisco Application Hosting API will be released in DNAC 1.4 (coming soon)

You will need the requests[secure] python module

pip install requests

You change the controller credentials either through environment variables or by editing dnac_config.py file

## Starting/Stopping Application running on Multiple devices

python 01_apphosting py <appname> start|stop


Example:
python 01_apphosting.py mlabbe_iperf3 stop

Finding all devices where Application is hosted
https://172.25.101.181:443/api/iox/service/api/v1/appmgr/devices?searchByApp=mlabbe_iperf3
RASHSHAH-M-R0MT:python rashshah$ python 01_apphosting.py mlabbe/iperf3 stop

Finding all devices where Application is hosted
https://172.25.101.181:443/api/iox/service/api/v1/appmgr/devices?searchByApp=mlabbe/iperf3
9d43e828-11bf-42c1-b090-47d70fc160bb

Stopping Application
https://172.25.101.181:443/api/iox/service/api/v1/appmgr/myapps?searchByName=mlabbe/iperf3
{u'response': u'STOPPED'}


RASHSHAH-M-R0MT:python rashshah$ python 01_apphosting.py mlabbe/iperf3 start

Finding all devices where Application is hosted
https://172.25.101.181:443/api/iox/service/api/v1/appmgr/devices?searchByApp=mlabbe/iperf3
9d43e828-11bf-42c1-b090-47d70fc160bb

Starting Application
https://172.25.101.181:443/api/iox/service/api/v1/appmgr/myapps?searchByName=mlabbe/iperf3
{u'response': u'RUNNING'}
