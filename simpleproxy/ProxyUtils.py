import os

import requests

def get_my_ip():
    return os.popen('curl -s ifconfig.me').readline()

def get_my_ip_aws():
    aws_checkip = 'http://checkip.amazonaws.com'
    try:
        ip = requests.get(aws_checkip).text.strip()
    except:
        raise
    return ip
