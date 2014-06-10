from utils import *
from ..sysconf import *


class RangeDownloadThread(threading.Thread):
    def __init__(self, startByte, opener, request, file, lock):
        threading.Thread.__init__(self)
        self.startByte = startByte
        self.request = request
        self.opener = openerDefaultClone(opener)
        self.file = file
        self.lock = lock

    def run(self):
        rangeContent = self.__checkRangeHeaderSupport()
        self.lock.acquire()
        self.file.seek(self.startByte)
        if rangeContent is not None:
            self.file.write(rangeContent)
            self.ret = 0  # download succeed
        else:
            syslog("download fail in range:%s, file=%s" % (self.startByte, self.file.name), LOG_ERROR)
            self.ret = -1  # download fail
        self.lock.release()

    def __checkRangeHeaderSupport(self):
        retryTime = 10
        while retryTime >= 0:
            res = urlopenWithRetry(self.opener, self.request)
            if res == None:
                return None
            if res.info().get("Content-Range") != None:
                try:
                    return res.read()
                except Exception, e:
                    retryTime -= 1
                    continue

            retryTime -= 1

        if retryTime == -1:
            syslog("rangeHeader not support at this file part, file=%s, url=%s, startByte=%s" % (
                self.file.name, self.request.get_full_url(), self.startByte), LOG_ERROR)
        return None


class RangeDownloader(object):
    def __init__(self, opener):
        self.opener = openerDefaultClone(opener)
        self.downloadThreadList = list()
        self.fileList = list()
        self.lock = threading.Lock()

    def rangeDownload(self, url, savePath, partNum=RANGE_PART_NUM):
        self.savePath = savePath
        self.url = url
        fileSize = self.__getFileSize(url)
        if fileSize == 0:
            return
        shardingSize = self.__sharding(fileSize, partNum)
        beginByte = 0
        while beginByte < fileSize:
            file = open(savePath, "wb")
            self.fileList.append(file)
            endByte = beginByte + shardingSize - 1
            if (endByte >= fileSize):
                endByte = fileSize - 1
            req = urllib2.Request(url)
            req.headers['Range'] = 'bytes=%s-%s' % (beginByte, endByte)
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
            syslog("download fail file=%s, url=%s" % (self.savePath, self.url), LOG_ERROR)
            os.remove(self.savePath)

    def __getFileSize(self, url):
        res = urlopenWithRetry(self.opener, url)
        if res == None:
            return 0
        return int(res.info()['Content-Length'])

    def __sharding(self, fileSize, partNum):
        return upDiv(fileSize, partNum)
