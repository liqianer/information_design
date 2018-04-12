import requests
import time
import random

import stem
import stem.connection

from stem import Signal
from stem.control import Controller
from agents import agentList

from bs4 import BeautifulSoup

def get_public_ip(headers, proxies):
    res = requests.get("http://icanhazip.com", headers = headers, proxies = proxies)
    return res.content.decode("utf-8").strip()

def scraper(urlList, suffix, file):
    # 代理
    proxies = {
        'http': '127.0.0.1:8118'
    }

    # ptime = time.time()
    # print(ptime)
    wfile = open(file, "w", encoding="utf-8")

    for url in urlList:
        url = url + suffix
        nextUrl = url

        while(nextUrl):
            # ntime = time.time()

            # if(ntime - ptime > 120):
            #     print(ntime)

            #     renew_connection()
            #     ptime = time.time()

            agent = random.choice(agentList)

            header = {"User-Agent": agent}

            print("当前ip: " + get_public_ip(header, proxies) + ", 正在爬取：" + nextUrl)

            page = requests.get(nextUrl, headers=header, proxies = proxies)
            # print(page.text)
            result = BeautifulSoup(page.text, "lxml")

            commentList = result.select("span.comment-info")
            for comment in commentList:
                rate = comment.select("span.rating")
                if rate:
                    print(comment.a["href"] + "\t" + rate[0]["title"])
                    wfile.write(url + "\t" + comment.a["href"] + "\t" + rate[0]["title"] + "\n")

            next = result.select("a.next")
            if next and next[0]["href"]:
                nextUrl = url + next[0]["href"]
            elif result and (result.title.text != "503 - Forwarding failure (Privoxy@Matrix)"):
                nextUrl = None
            else:
                print("Error! Retrying...")
                time.sleep(5)

            # renew_connection()

    print("end")

def file2List(path):
    with open(path, encoding="utf-8") as f:
        myList = [line.strip() for line in f]

    return myList

if __name__ == "__main__":
    urlList = file2List("F:\Project\MyNotebook\Information Design\src\choice.txt")
    suffix = "comments"
    wfile = "test1.txt"
    scraper(urlList, suffix, wfile)
