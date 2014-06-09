import argparse
import os
import thread
import threading
import signal
import time
import urllib2
import socket
import Queue
from multiprocessing import Process, Value, Lock
from pyquery import PyQuery as pq
from rangedownloader import RangeDownloader
from utils import *
from ..sysconf import *

class PictureThread(threading.Thread):
    def __init__(self,
            startIndex,
            splitNum,
            opener,
            urlList,
            savePath,
            useRangeHeaders,
            downloadLock,
            handlerName):
        threading.Thread.__init__(self)
        self.startIndex = startIndex
        self.urlList = urlList
        self.opener = opener
        self.splitNum = splitNum
        self.name = handlerName
        self.savePath = savePath
        self.useRangeHeaders = useRangeHeaders
        self.downloadLock = downloadLock

    def run(self):
        syslog(self.getName() + " picture thread start!", LOG_INFO)
        pictureSize = len(self.urlList)
        maxIndex = self.startIndex + self.splitNum - 1
        if maxIndex > pictureSize:
            maxIndex = pictureSize

        for index in range(self.startIndex - 1, maxIndex):
            self.downloadLock.acquire()
            self.__crawl(self.urlList[index], index)
            self.downloadLock.release()

    def __crawl(self, url, picIndex):
        syslog("downloading " + url, LOG_INFO)
        savePath = self.savePath + str(picIndex) + '.jpg'
        if self.useRangeHeaders:
            rd = RangeDownloader(self.opener)
            rd.rangeDownload(url, savePath)
        else:
            content = urlReadWithRetry(self.opener, url)
            if content == None:
                syslog("error! retry too many times, url=" % (url), LOG_ERROR)
                return
            file = open(savePath, "w")
            file.write(content)
            file.close()

class CrawlerManager(object):
    #conf.url and conf.savePath are required
    def __init__(self, opener, urlList, savePath, useRangeHeaders, maxDownloadCount = MAX_DOWNLOAD_COUNT):
        self.savePath = savePath
        self.useRangeHeaders = useRangeHeaders
        self.opener = opener
        self.urlList = urlList
        self.downloadLock = threading.Semaphore(maxDownloadCount)
        createDir(savePath)

    def startCrawl(self):
        beginTime = time.time()
        self.PictureThreadList = list()
        index = 1
        count = 1
        picNum = len(self.urlList)
        splitNum = getShardingConf(picNum)[0]
        
        while index <= picNum:
            picThread = PictureThread(
                    index,
                    splitNum,
                    self.opener,
                    self.urlList,
                    self.savePath,
                    self.useRangeHeaders,
                    self.downloadLock,
                    "pictureThread:" + str(count))
            self.PictureThreadList.append(picThread)
            picThread.start()
            index += splitNum
            count += 1

        for th in self.PictureThreadList:
            th.join()

        endTime = time.time()
        cost = round(endTime - beginTime, 1)
        average = cost / picNum
        syslog("download complete!", LOG_INFO)
        syslog('crawl ' + str(picNum) + " imgs", LOG_INFO)
        syslog('total cost: ' + str(cost) + 's', LOG_INFO)
        syslog('average ' + str(average) + 's per image', LOG_INFO)

    def stopCrawl(self):
        #TODO not surported yet
        pass
