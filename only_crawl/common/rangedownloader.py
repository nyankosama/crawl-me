import urllib2
import threading
import socket
import os
from utils import *

class RangeDownloadThread(threading.Thread):
    def __init__(self, startByte, opener, request, file):
        threading.Thread.__init__(self)
        self.startByte = startByte
        self.request = request
        self.opener = openerDefaultClone(opener)
        self.file = file

    def run(self):
        res = self.__checkRangeHeaderSupport()
        if res == None:
            self.ret = -1
        rangeContent = resReadWithRetry(res)
        self.file.seek(self.startByte)
        if rangeContent is not None:
            self.file.write(rangeContent)
            self.ret = 0 #download succeed
        else:
            syslog("error! retry too many times in range:%s" % (self.startByte), LOG_ERROR)
            self.ret = -1 #download fail

    def __checkRangeHeaderSupport(self):
        retryTime = 10
        while retryTime >= 0:
            res = urlopenWithRetry(self.opener, self.request)
            if res.info().get("Content-Range") != None:
                return res
            retryTime -= 1

        if retryTime == -1:
            syslog("rangeHeader not support at this file part, file=%s, url=%s, startByte=%s" % (self.file.name, self.request.get_full_url(), self.startByte), LOG_ERROR)
        return None

class RangeDownloader(object):
    def __init__(self, opener):
        self.opener = openerDefaultClone(opener)
        self.downloadThreadList = list()
        self.fileList = list()

    def rangeDownload(self, url, savePath, partNum = 5):
        self.savePath = savePath
        self.url = url
        fileSize = self.__getFileSize(url)
        if fileSize == 0:
            return
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
            th = RangeDownloadThread(beginByte, self.opener, req, file)
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
        try:
            res = urlopenWithRetry(self.opener, url)
        except urllib2.HTTPError, e:
            syslog("http 404, url=%s" % (url), LOG_INFO)
            return 0
        return int(res.info()['Content-Length'])

    def __sharding(self, fileSize, partNum):
        return upDiv(fileSize, partNum)
