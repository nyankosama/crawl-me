import urllib2
import threading
import socket
import os
import copy
from utils import *

class RangeDownloadThread(threading.Thread):
    def __init__(self, startByte, opener, request, file):
        threading.Thread.__init__(self)
        self.startByte =startByte
        self.request = request
        self.opener = opener
        self.file = file

    def run(self):
        rangeContent = urlopenWithRetry(self.opener, self.request)
        self.file.seek(self.startByte)
        if rangeContent is not None:
            self.file.write(rangeContent)
            self.ret = 0 #download succeed
        else:
            syslog("error! retry too many times in range:%s" % (startByte), LOG_ERROR)
            self.ret = -1 #download fail

class RangeDownloader(object):
    def __init__(self, opener):
        self.opener = opener
        self.downloadThreadList = list()
        self.fileList = list()

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
            th = RangeDownloadThread(beginByte, copy.copy(self.opener), req, file)
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

