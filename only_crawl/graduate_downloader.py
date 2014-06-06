from pyquery import PyQuery as pq
from commonPicCrawler import commonPicCrawler as commonCrawler
import urllib2
import copy


class GraduatePageIter(commonCrawler.CrawlerIterator):
    def __init__(self):
        commonCrawler.CrawlerIterator.__init__(self)

    def init(self, url):
        self.urlList.append(url)
        self.size = 1
        
    def clone(self):
        copyObj = GraduatePageIter()
        copyObj.size = self.size
        copyObj.urlList = copy.deepcopy(self.urlList)
        return copyObj

class GraduatePicIter(commonCrawler.CrawlerIterator):
    def __init__(self):
        commonCrawler.CrawlerIterator.__init__(self)
        self.opener = urllib2.build_opener()

    def init(self, url):
        htmlContent = urllib2.urlopen(url).read()
        q = pq(htmlContent)
        li = q("li")
        for i in range(1, li.size()):
            fileName = li.eq(i).find('a').attr('href')
            url = 'http://yangwen.hostyd.com/files/heads/' + fileName
            self.urlList.append(url)

        self.size = len(self.urlList)

    def clone(self):
        copyObj = GraduatePicIter()
        copyObj.size = self.size
        copyObj.urlList = copy.deepcopy(self.urlList)
        return copyObj


if __name__ == "__main__":
    pageIter = GraduatePageIter()
    picIter = GraduatePicIter()
    opener = urllib2.build_opener()
    conf = commonCrawler.crawlerConf('http://yangwen.hostyd.com/files/heads', '/home/nyankosama/downloads/other/graduate/', opener)
    crawler = commonCrawler.CrawlerManager(conf, picIter, pageIter)
    crawler.startCrawl()
