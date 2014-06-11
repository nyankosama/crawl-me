from pyquery import PyQuery as pq

from pageBasedHandler import *
from ..common.utils import *


class GamerskyHandler(PageBasedHandler):
    # def getPageUrl(self, baseUrl, opener, beginPage, endPage):
    def getPageUrl(self, opener, paraConf):
        urlList = list()
        for page in range(paraConf["beginPage"], paraConf["endPage"] + 1):
            if page == 1:
                crawlUrl = paraConf["url"]
            else:
                crawlUrl = paraConf["url"][0: paraConf["url"].index('.shtml')] + "_" + str(page) + ".shtml"
            urlList.append(crawlUrl)
        return urlList

    def getPictureUrl(self, pageUrl, opener):
        urlList = list()
        htmlContent = urlReadWithRetry(opener, pageUrl)
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
                syslog("Exception:" + str(Exception) + ", " + str(e), LOG_ERROR)
                continue

        return urlList

    def initOpener(self, conf):
        self.opener = urllib2.build_opener()
        return self.opener

    def initPara(self, parser):
        parser.add_argument('url', help='your url to crawl')
        parser.add_argument('savePath', help='the path where the imgs ars saved')
        parser.add_argument('beginPage', help='the page where we start crawling', type=int)
        parser.add_argument('endPage', help='the page where we end crawling', type=int)
        args = parser.parse_args()
        return {
            "url": args.url,
            "savePath": args.savePath,
            "beginPage": args.beginPage,
            "endPage": args.endPage
        }
