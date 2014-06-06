import urllib2
from pageBasedHandler import PageBasedHandler
from ..common.utils import *
from pyquery import PyQuery as pq

class GamerskyHandler(PageBasedHandler):
    def getPageUrl(self, baseUrl, opener, beginPage, endPage):
        urlList = list()
        for page in range(self.args.beginPage, self.args.endPage + 1):
            if page == 1:
                crawlUrl = baseUrl
            else:
                crawlUrl = baseUrl[0: baseUrl.index('.shtml')] + "_" + str(page) + ".shtml"
            urlList.append(crawlUrl)
        return urlList        

    def getPictureUrl(self, pageUrl, opener):
        urlList = list()
        htmlContent = urlopenWithRetry(opener, pageUrl)
        if htmlContent == None:
            syslog("GameskyPicIterator init fail at url=" + pageUrl, LOG_ERROR)
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
                urlList.append(imgUrl)
                syslog("imgurl find, url=%s" % (imgUrl))
            except Exception, e:
                syslog("Exception:" + Exception + ", " + e, LOG_ERROR)
                continue

        return urlList
         
    def initOpener(self):
        self.opener = urllib2.build_opener()
        return self.opener
