import urllib2
import threading
import socket
import os
import copy
from utils import *

class RangeDownloadThread(threading.Thread):
    def __init__(self, startByte, opener, request, file, lock):
        threading.Thread.__init__(self)
        self.startByte =startByte
        self.request = request
        self.opener = copy.copy(opener)
        self.file = file
        self.lock = lock

    def run(self):
        rangeContent = urlopenWithRetry(self.opener, self.request)
        self.lock.acquire()
        self.file.seek(self.startByte)
        if rangeContent is not None:
            self.file.write(rangeContent)
            self.ret = 0 #download succeed
        else:
            syslog("error! retry too many times in range:%s" % (startByte), LOG_ERROR)
            self.ret = -1 #download fail
        self.lock.release()

class RangeDownloader(object):
    def __init__(self, opener):
        self.opener = opener
        self.downloadThreadList = list()
        self.fileList = list()
        self.lock = threading.Lock()

    def rangeDownload(self, url, savePath, partNum = 5):
        self.savePath = savePath
        self.url = url
        #print url + " part=" + str(partNum) + " download start!"
        fileSize = self.__getFileSize(url)
        #print "file size=%s" % (fileSize)
        shardingSize = self.__sharding(fileSize, partNum)
        beginByte = 0
        while beginByte < fileSize:
            file = open(savePath, "w")
            self.fileList.append(file)
            endByte = beginByte + shardingSize - 1
            if (endByte >= fileSize):
                endByte = fileSize - 1
            req = urllib2.Request(url)
            req.headers['Range'] = 'bytes=%s-%s' % (beginByte, endByte)
            #print "start:%s, end:%s" % (beginByte, endByte)
            th = RangeDownloadThread(beginByte, self.opener, req, file, self.lock)
            self.downloadThreadList.append(th)
            th.start()
            beginByte += shardingSize

        self.__handleResult()

        
    def __handleResult(self):
        hasError = False
        for th in self.downloadThreadList:
            th.join()

        for th in self.downloadThreadList:
            if th.ret != 0:
                hasError = True

        for f in self.fileList:
            f.close()

        if hasError:
            syslog("download fail because of http timeout, url=%s" % (self.url), LOG_ERROR)
            os.remove(self.savePath)

    def __getFileSize(self, url):
        res = self.opener.open(url)
        return int(res.info()['Content-Length'])

    def __sharding(self, fileSize, partNum):
        return upDiv(fileSize, partNum)
