import requests
from bs4 import BeautifulSoup
from agents import agentList
import random
import time
import re
import json

def getUrlList(url):
    agent = random.choice(agentList)
    headers = {"User-Agent": agent}

    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H60B1356I7L15S5D"
    proxyPass = "E9FDCDA96A210EEA"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host" : proxyHost,
        "port" : proxyPort,
        "user" : proxyUser,
        "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }

    urlList = []

    page = requests.get(url, headers=headers, proxies=proxies)

    try:
        parttern = re.compile("= (.*?);var")
        result = parttern.findall(page.text)[0]
        detailJson = json.loads(result)
        soup = BeautifulSoup(detailJson["value"]["listHTML"], "lxml")
        aList = soup.find_all("a")
        for a in aList:
            if "title" in a.attrs:
                urlList.append(a["href"] + "\t" + a["title"])

    except Exception as e:
        print("Error!")
        print(e)

    urlSet = set(urlList)
    return urlSet

if __name__ == "__main__":
    typeList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    pageList = range(1, 15)

    with open("urlList.txt", "w", encoding="utf-8") as f:

        for type in typeList:
            for page in pageList:
                t = time.strftime("%Y%m%d%H%M%S",time.localtime())
                url = """
                http://service.channel.mtime.com/service/search.mcs?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Channel.Pages.SearchService&Ajax_CallBackMethod=SearchMovieByCategory&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2Fmovie%2Fsearch%2Fsection%2F%23initialcn%3D1_A&t={t}4080788&Ajax_CallBackArgument0=&Ajax_CallBackArgument1=0&Ajax_CallBackArgument2=0&Ajax_CallBackArgument3=0&Ajax_CallBackArgument4=0&Ajax_CallBackArgument5=0&Ajax_CallBackArgument6=0&Ajax_CallBackArgument7=0&Ajax_CallBackArgument8=&Ajax_CallBackArgument9=0&Ajax_CallBackArgument10=0&Ajax_CallBackArgument11=0&Ajax_CallBackArgument12=0&Ajax_CallBackArgument13=1&Ajax_CallBackArgument14={type}&Ajax_CallBackArgument15=0&Ajax_CallBackArgument16=1&Ajax_CallBackArgument17=4&Ajax_CallBackArgument18={page}&Ajax_CallBackArgument19=0
                """.format(t=t, type=type, page=str(page))

                print("Is Crawling " + type + str(page))

                urlSet = getUrlList(url)

                for movieUrl in urlSet:
                    f.write(movieUrl + "\n")

    print("end!")