import threading
import urllib2
import copy
from baseHandler import *
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
    def getUrlList(self, conf):
        pageUrlList = self.getPageUrl(copy.copy(self.opener), conf)
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
    def getPageUrl(self, opener, paraConf):pass

    @abstractmethod
    def getPictureUrl(self, pageUrl, opener):pass
