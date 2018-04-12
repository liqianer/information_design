import time
import random
import requests

from agents import agentList
from bs4 import BeautifulSoup
from PyQt5.QtCore import pyqtSignal, QObject

class Scraper(QObject):
    suc = 0
    fail = 0
    finishSignal = pyqtSignal()
    setProSignal = pyqtSignal()
    maxSignal = pyqtSignal(int)
    addsSignal = pyqtSignal()
    addfSignal = pyqtSignal()
    setStatSignal = pyqtSignal(str)

    def __init__(self, urlPath, resultPath, sleepTime, user, pw):
        super().__init__()
        self.urlPath = urlPath
        self.resultPath = resultPath
        self.sleepTime = sleepTime
        self.user = user
        self.pw = pw

    def task(self):
        with open(self.urlPath, encoding="utf-8") as urlFile:
            urlList = [line.strip().split("\t")[0] for line in urlFile]

        self.maxSignal.emit(len(urlList))

        resultFile = self.resultPath + "/result.txt"
        wfile = open(resultFile, "a+", encoding="utf-8")

        for url in urlList:
            agent = random.choice(agentList)
            headers = {"User-Agent": agent}
            nextUrl =  url + "reviews/short/new.html"

            if self.user and self.pw:
                # 代理服务器
                proxyHost = "http-dyn.abuyun.com"
                proxyPort = "9020"

                # 代理隧道验证信息
                proxyUser = self.user
                proxyPass = self.pw

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
            else:
                proxies = None

            # 更新爬取结果
            self.runTask(url, nextUrl, wfile, headers, proxies)

            self.setProSignal.emit()

        # 关闭文件夹并退出
        wfile.close()
        self.finishSignal.emit()

    def runTask(self, url, nextUrl, wfile, headers, proxies=None):
        while nextUrl:
            try:
                self.setStatSignal.emit('正在爬取' + nextUrl)

                page = requests.get(nextUrl, headers=headers, proxies=proxies)
                result = BeautifulSoup(page.text, "lxml")

                # 获取全部评论
                comments = result.select("div.mod_short")

                for comment in comments:
                    # 获取用户资料
                    user = comment.find("div", class_="pic_58")
                    if user.span:
                        wfile.write("%s\t%s\t%s\t%s\n" % (url, user.p.a["href"], user.span.text, comment.h3.text))

                self.addsSignal.emit()

                # 获取下一页并判断
                next = result.find(id="key_nextpage")
                if next:
                    nextUrl = next["href"]
                else:
                    nextUrl = None

                time.sleep(self.sleepTime)

            except Exception as e:
                self.setStatSignal.emit('There is a error: ' + e)
                self.addfSignal.emit()

                with open("log.txt", "a+", encoding="utf-8") as log:
                    now = time.strftime("%m-%d %H:%M:%S", time.localtime())
                    log.write("[%s] %s\n" % (now, e))

if __name__ == "__main__":
    pass