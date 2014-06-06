###This is a crawler for gamersky's pictures, multi-thread crawling supported.

from commonPicCrawler import commonPicCrawler as commonCrawler
import urllib2
import argparse
import os
import thread
import threading
import signal
import time
import copy
from pyquery import PyQuery as pq

class GameskyPageIterator(commonCrawler.CrawlerIterator):
    def __init__(self, beginPage, endPage):
        commonCrawler.CrawlerIterator.__init__(self)
        self.beginPage = beginPage
        self.endPage = endPage

    def init(self, url):
        for page in range(self.beginPage, self.endPage + 1):
            if page == 1:
                crawlUrl = url
            else:
                crawlUrl = url[0: url.index('.shtml')] + "_" + str(page) + ".shtml"

            self.urlList.append(crawlUrl)
        
        self.size = len(self.urlList)

    def clone(self):
        copyObj = GameskyPageIterator(self.beginPage, self.endPage)
        copyObj.size = self.size
        copyObj.urlList = copy.deepcopy(self.urlList)
        return copyObj 

class GameskyPicIterator(commonCrawler.CrawlerIterator):
    def __init__(self):
        commonCrawler.CrawlerIterator.__init__(self)
        self.opener = urllib2.build_opener()

    def init(self, url):
        htmlContent = commonCrawler.urlopenWithRetry(self.opener, url)
        if htmlContent == None:
            print "GameskyPicIterator init fail at url=" + url
        q = pq(htmlContent)
        imgP = q('p')
        for i in range(0, imgP.size()):
            try:
                #check if the sub element has a href attribute
                href = imgP.eq(i).find('a').attr('href')
                if (href == None):
                    continue
                #check postfix 
                imgUrl = href.split('?')[1]
                self.urlList.append(imgUrl)
                print "urlappend: " + imgUrl + " size: " + str(len(self.urlList))
            except:
                print "the href doesn't end with .jpg or .png"
                continue

        self.size = len(self.urlList)

    def clone(self):
        copyObj = GameskyPicIterator()
        copyObj.size = self.size
        copyObj.urlList = copy.deepcopy(self.urlList)
        return copyObj


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='your url to crawl')
    parser.add_argument('savePath', help='the path where the imgs ars saved')
    parser.add_argument('beginPage', help='the page where we start crawling', type=int)
    parser.add_argument('endPage', help='the page where we end crawling', type=int)
    args = parser.parse_args()

    pageIterator = GameskyPageIterator(args.beginPage, args.endPage)
    picIterator = GameskyPicIterator()

    opener = urllib2.build_opener()
    conf = commonCrawler.crawlerConf(args.url, args.savePath, opener) 
    crawler = commonCrawler.CrawlerManager(conf, picIterator, pageIterator)
    crawler.startCrawl()
