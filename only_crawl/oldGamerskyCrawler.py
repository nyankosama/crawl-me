###This is a crawler for gamersky's pictures, multi-thread crawling supported.

import urllib2
import argparse
import os
import thread
import threading
import signal
import time
from multiprocessing import Process, Value, Lock
from pyquery import PyQuery as pq

#max thread count allowed
MAX_THREAD_COUNT = 20 
SHARDING_PAGE = 2

class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value

class threadHandler(threading.Thread):
    def __init__(self, crawlerConf, index, handlerName):
        threading.Thread.__init__(self)
        self.conf = crawlerConf
        self.index = index
        threading.Thread.__init__(self, name=handlerName)
        self.isStop = False

    def run(self):
        print self.getName() + " start!"
        for page in range(self.index, self.index+self.conf.shardingPage):
            if self.isStop == True:
                return

            if (page > self.conf.endPage):
                break
            self.__craw(self.conf, page)

    def stop():
        self.isStop = True

    def __craw(self, conf, page):
        print 'start crawling page:' + str(page)
        if page == 1:
            crawUrl = self.conf.url
        else:
            crawUrl = self.conf.url[0:self.conf.url.index('.shtml')] + "_" + str(page) + '.shtml'

        htmlContent = urllib2.urlopen(crawUrl).read()
        q = pq(htmlContent)
        imgP = q('p')
        for i in range(0, imgP.size()):
            if self.isStop == True:
                return

            try:
                #check if the sub element has a href attribute
                href = imgP.eq(i).find('a').attr('href')
                if (href == None):
                    continue
                #check postfix 
                imgUrl = href.split('?')[1]
                print 'downloading ' + imgUrl
                saveFile = open(self.conf.savePath + str(page) + '_' + str(i) + '.jpg' , 'w')
                saveFile.write(urllib2.urlopen(imgUrl).read())
                saveFile.close()
                self.conf.counter.increment()
            except:
                print "the href doesn't end with .jpg or .png"
                continue

class crawlerConf():
    def __init__(self, url, savePath, beginPage, endPage):
        self.url = url
        self.savePath = savePath
        self.beginPage = beginPage
        self.endPage = endPage
        self.__createDir()
        ret = self.__getThreadConf(self.beginPage, self.endPage)
        self.shardingPage = ret["shardingPage"]
        self.threadCount = ret["threadCount"]
        self.counter = Counter()

    def __createDir(self):
        #create dir
        if os.path.isdir(self.savePath) is not True:
            os.makedirs(self.savePath)

    def __getThreadConf(self, beginPage, endPage):
        tmpCount = upDiv(endPage+1-beginPage, SHARDING_PAGE)
        if tmpCount > MAX_THREAD_COUNT:
            tmpCount = MAX_THREAD_COUNT

        shardingPage = upDiv(endPage+1-beginPage, tmpCount)
        threadCount = tmpCount
        return {"threadCount":threadCount, "shardingPage":shardingPage}


class gamerSkyCrawler:
    def __init__(self, url, savePath):
        self.url = url
        self.savePath = savePath

    def startCraw(self, beginPage, endPage):
        beginTime = time.time()
        conf = crawlerConf(self.url, self.savePath, beginPage, endPage)
        self.crawlerThreads = list()
        index = beginPage
        count = 1
        while index <= endPage:
            th = threadHandler(conf, index, "handler" + str(count))
            self.crawlerThreads.append(th)
            th.start()
            index += conf.shardingPage
            count += 1

        for th in self.crawlerThreads:
            th.join()

        endTime = time.time()
        cost = round(endTime - beginTime, 1)
        global counter
        average = cost / conf.counter.value()
        print 'complete!'
        print 'total cost: ' + str(cost) + 's'
        print 'average ' + str(average) + 's per image'

    def setUrl(self, url):
        self.url = url

    def setSavePath(self, savePath):
        self.savePath = savePath

    def stop(self):
        for handler in self.crawlerThreads:
            handler.stop()

    
def upDiv(a, b):
    return (a+b-1) / b

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='your url to crawl')
    parser.add_argument('savePath', help='the path where the imgs ars saved')
    parser.add_argument('beginPage', help='the page where we start crawling', type=int)
    parser.add_argument('endPage', help='the page where we end crawling', type=int)
    args = parser.parse_args()
    crawler = gamerSkyCrawler(args.url, args.savePath)
    crawler.startCraw(args.beginPage, args.endPage)

