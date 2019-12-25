from datetime import datetime

import requests
from ping3 import ping

from .ProxyUtils import get_my_ip

class Proxy():
    def __init__(self, proxy_ip_v4, proxy_port, proxy_type, proxy_delay = None, 
                 proxy_status = None, proxy_anonymity = None):

        self.ip_v4 = proxy_ip_v4
        self.port = proxy_port
        self.type = proxy_type

        self.anonymity = proxy_anonymity

        self.delay = proxy_delay
        self.status = proxy_status

    def proxy_as_url(self):
        """Returns proxy address, port and type in URL format."""
        return '%s://%s:%s' % (self.type, self.ip_v4, self.port)

    def ping_proxy(self):
        """Pings the proxy server and returns the delay in ms or False, if timeout."""
        return ping(self.ip_v4, timeout = 2, unit = 'ms')

    def verify_proxy(self, my_ip = None):
        """Uses AWS checkIP to verify that webpages are reachable and
           that the real IP is not leaked."""

        aws_checkip = 'http://checkip.amazonaws.com'
        proxyDict = {self.type : self.proxy_as_url()}
        
        if my_ip is None:
            my_ip = get_my_ip()

        try:
            response = requests.get(aws_checkip, proxies = proxyDict, timeout=5).text.strip()

            if len(response) > 15:
                return False
            else:
                proxy_ip = response
        except requests.exceptions.ReadTimeout:
            return False
        except requests.exceptions.ConnectionError:
            return False
        except requests.exceptions.ChunkedEncodingError:
            return False
        except:
            raise

        return not (proxy_ip == my_ip)

    def check_proxy(self, my_ip = None):
        delay = self.ping_proxy()
        up = self.verify_proxy(my_ip = my_ip)

        now = datetime.now()

        if delay:
            self.delay = int(delay)
        else:
            self.delay = 9999

        if up and not self.status == 'UP':
            self.status = 'UP'
            self.up_since = now
            self.down_since = None
        elif not up and self.status == 'UP':
            self.status = 'DOWN'
            self.up_since = None
            self.down_since = now

        self.last_checked = now


