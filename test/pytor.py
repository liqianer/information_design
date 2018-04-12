import requests
from lxml import html
import sys
import urlparse
import collections
import time
from PIL import Image
import os
import random

import stem
import stem.connection

from stem import Signal
from stem.control import Controller

# 让Tor重建连接，获得新的线路
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password = 'test1234')
        controller.signal(Signal.NEWNYM)
        controller.close()

def get_public_ip(headers):
    res = requests.get("http://icanhazip.com", headers = headers, proxies = proxies)
    print(res.content)

if __name__ == "__main__":
    # 代理
    proxies = {
        'http': '127.0.0.1:8118'
    }

    url = "http://movie.douban.com/subject/7155083/comments"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    get_public_ip(headers)

    response = requests.get(url, headers = headers, proxies = proxies)