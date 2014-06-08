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
        rangeContent = urlopenWithRetry(self.opener, self.request)
        #syslog("part len=%s, startByte=%s, file=%s" % (len(rangeContent), self.startByte, self.file.name))
        #self.contentLen = self.contentLen + len(rangeContent)
        self.file.seek(self.startByte)
        if rangeContent is not None:
            self.file.write(rangeContent)
            self.ret = 0 #download succeed
        else:
            syslog("error! retry too many times in range:%s" % (startByte), LOG_ERROR)
            self.ret = -1 #download fail

class RangeDownloader(object):
    def __init__(self, opener):
        self.opener = openerDefaultClone(opener)
        self.downloadThreadList = list()
        self.fileList = list()
        self.lock = threading.Lock()

    def rangeDownload(self, url, savePath, partNum = 5):
        self.savePath = savePath
        self.url = url
        #syslog(url + " part=" + str(partNum) + " download start!", LOG_DEBUG)
        fileSize = self.__getFileSize(url)
        if fileSize == 0:
            return
        #syslog("%s size=%s, url=%s" % (savePath, fileSize, url), LOG_ERROR)
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
            #if beginByte == 0:
                #self.__check206(req)
            syslog("start:%s, end:%s, file=%s" % (beginByte, endByte, savePath), LOG_DEBUG)
            th = RangeDownloadThread(beginByte, self.opener, req, file)

            self.downloadThreadList.append(th)
            th.start()
            beginByte += shardingSize

        self.__handleResult()

    def __check206(self, request):
        res = self.opener.open(request)
        syslog("code=%s, file=%s, content-len=%s" % (res.getcode(), self.savePath, res.info().get("Content-Range")), LOG_WARNING)

        
    def __handleResult(self):
        hasError = False
        contentSum = 0;
        for th in self.downloadThreadList:
            th.join()
            contentSum = contentSum + th.contentLen

        syslog("content len=%s, file=%s" % (contentSum, self.savePath), LOG_DEBUG)
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
            res = self.opener.open(url)
        except urllib2.HTTPError, e:
            syslog("http 404, url=%s" % (url), LOG_INFO)
            return 0
        return int(res.info()['Content-Length'])

    def __sharding(self, fileSize, partNum):
        return upDiv(fileSize, partNum)
