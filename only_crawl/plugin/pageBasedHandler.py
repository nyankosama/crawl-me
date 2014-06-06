import threading
import urllib2
import copy
from baseHandler import BaseHandler
from ..common.utils import *
from ..third_party.abc import ABCMeta, abstractmethod

class PictureUrlThread(threading.Thread):
    def __init__(self, threadName, pageUrl, handler):
        threading.Thread.__init__(self, name=threadName)
        self.pageUrl = pageUrl
        self.handler = handler

    def run(self):
        syslog("getting page url=%s" % (self.pageUrl), LOG_INFO)
        self.pictureUrlList = self.handler.getPictureUrl(self.pageUrl, copy.copy(self.handler.opener))

    def getPictureUrlList(self):
        return self.pictureUrlList

#abstruct base class
class PageBasedHandler(BaseHandler):
    def getUrlList(self):
        pageUrlList = self.getPageUrl(self.args.url, copy.copy(self.opener), self.args.beginPage, self.args.endPage)
        pageNum = len(pageUrlList)
        threadList = list()
        for index, url in enumerate(pageUrlList):
            th = PictureUrlThread("pictureUrlThread:%s" % (index), url, self)
            threadList.append(th) 
            th.start()

        pictureUrlList = list()
        for th in threadList:
            th.join()
            pictureUrlList.extend(th.getPictureUrlList())

        return pictureUrlList

    
    @abstractmethod
    def getPageUrl(self, baseUrl, opener, beginPage, endPage):pass

    @abstractmethod
    def getPictureUrl(self, pageUrl, opener):pass

    def initPara(self, parser):
        parser.add_argument('url', help='your url to crawl')
        parser.add_argument('savePath', help='the path where the imgs ars saved')
        parser.add_argument('beginPage', help='the page where we start crawling', type=int)
        parser.add_argument('endPage', help='the page where we end crawling', type=int)
        self.args = parser.parse_args()
        return self.args
