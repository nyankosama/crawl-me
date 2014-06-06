###This is a crawler for pivix user's pictures, multi-thread crawling supported.

from commonPicCrawler import commonPicCrawler as commonCrawler
import urllib2
import urllib
import httplib
import cookielib
import argparse
import os
import thread
import threading
import signal
import time
import copy
from pyquery import PyQuery as pq

def getUrlFromId(memberID):
    url = 'http://www.pixiv.net/member_illust.php?id=' + str(memberID)
    return url

def initLoginOpener(pixiv_id, password):
    cookieJar = cookielib.CookieJar()
    cookie = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie)
    opener.addheaders = [
            ('Referer', 'http://www.pixiv.net/member_illust.php?mode=medium'),
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36')]
    
    postData = {
            "mode":"login",
            "return_to":"/",
            "pixiv_id":pixiv_id,
            "pass":password
            }
    login_headers = {
            'Referer':'https://www.secure.pixiv.net/login.php',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'
            }
    request = urllib2.Request("https://www.secure.pixiv.net/login.php", urllib.urlencode(postData), headers = login_headers)
    print "www.pixiv.net logining!"
    commonCrawler.urlopenWithRetry(opener,request)
    print "login completed!"
    #urllib2.urlopen(request).read()
    return opener

class PivixPageIterator(commonCrawler.CrawlerIterator):
    def __init__(self, urlopener):
        commonCrawler.CrawlerIterator.__init__(self)
        self.urlopener = urlopener
    
    def init(self, url):
        htmlContent = commonCrawler.urlopenWithRetry(self.urlopener, url)
        if htmlContent == None:
            print "pivixPageIterator init fail! timeout retry too many times"
        d = pq(htmlContent)
        pageLi = d(".page-list").eq(0)("li")
        size = pageLi.size()
        if size == 0:
            size = 1
        print "total " + str(size) + " pages"
        self.urlList.append(url)
        for page in range(2, size + 1):
            self.urlList.append(url + "&p=" + str(page))

        self.size = len(self.urlList)
    
    def clone(self):
        copyObj = PivixPageIterator(self.urlopener)
        copyObj.size = self.size
        copyObj.urlList = copy.deepcopy(self.urlList)
        return copyObj

class PivixPicIterator(commonCrawler.CrawlerIterator):
    def __init__(self, urlopener):
        commonCrawler.CrawlerIterator.__init__(self)
        self.urlopener = urlopener

    def init(self, url):
        htmlContent = commonCrawler.urlopenWithRetry(self.urlopener, url)
        if htmlContent == None:
            print "pivixPicIterator init fail! timeout retry too many times"

        d = pq(htmlContent)
        profile = d(".profile-unit")
        src = profile.find("img").attr("src")
        userName = src[src.find("profile") + len("profile") + 1: src.rfind("/")]
        item = d(".image-item")
        for index in range(0, item.size()):
            href = item.eq(index).find("a").attr("href")
            imgID = href[href.rfind("=") + 1:]
            bigImgUrl = "http://www.pixiv.net/member_illust.php?mode=big&illust_id=" + imgID
            
            print "opening " + bigImgUrl
            bigImgContent = commonCrawler.urlopenWithRetry(self.urlopener, bigImgUrl)
            if bigImgContent == None:
                print "retry too many times at url=" + bigImgUrl

            bigD = pq(bigImgContent)
            imgUrl = bigD("img").attr("src")
            if imgUrl == None:
                print "error!" + " big image url wrong url=" + bigImgUrl
            else:
                self.urlList.append(imgUrl)

        self.size = len(self.urlList)
        
    
    def clone(self):
        copyObj = PivixPicIterator(self.urlopener)
        copyObj.size = self.size
        copyObj.urlList = copy.deepcopy(self.urlList)
        return copyObj


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('authorId', help='the author id you want to crawl')
    parser.add_argument('savePath', help='the path where the imgs ars saved')
    parser.add_argument('pixivId', help='your pixiv login id')
    parser.add_argument('password', help='your pixiv login password')
    args = parser.parse_args()

    opener = initLoginOpener(args.pixivId, args.password)
    pageIterator = PivixPageIterator(opener)
    picIterator = PivixPicIterator(opener)

    conf = commonCrawler.crawlerConf(getUrlFromId(args.authorId), args.savePath, opener) 
    crawler = commonCrawler.CrawlerManager(conf, picIterator, pageIterator)
    crawler.startCrawl(15)

