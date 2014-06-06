import urllib2
import sys
from pageBasedHandler import PageBasedHandler
from ..common.utils import *
from pyquery import PyQuery as pq

class PixivHandler(PageBasedHandler):
    def getPageUrl(self, baseUrl, opener, beginPage, endPage):
        urlList = list()
        htmlContent = urlopenWithRetry(opener, baseUrl)
        if htmlContent == None:
            syslog("pixiv plugin pageCrawl init fail! timeout retry too many times, url=%s" % (baseUrl), LOG_ERROR)
            sys.exit(1)
        d = pq(htmlContent)
        pageLi = d(".page-list").eq(0)("li")
        size = pageLi.size()
        if size == 0:
            size = 1
        syslog("total " + str(size) + " pages", LOG_INFO)
        urlList.append(url)
        for page in range(2, size + 1):
            urlList.append(url + "&p=" + str(page))
        return urlList        

    def getPictureUrl(self, pageUrl, opener):
        urlList = list()
        htmlContent = urlopenWithRetry(opener, pageUrl)
        if htmlContent == None:
            syslog("pixiv plugin pictureCrawl init fail! timeout retry too many times, url=%s" % (baseUrl), LOG_ERROR)
            return

        d = pq(htmlContent)
        profile = d(".profile-unit")
        src = profile.find("img").attr("src")
        userName = src[src.find("profile") + len("profile") + 1: src.rfind("/")]
        item = d(".image-item")
        for index in range(0, item.size()):
            href = item.eq(index).find("a").attr("href")
            imgID = href[href.rfind("=") + 1:]
            bigImgUrl = "http://www.pixiv.net/member_illust.php?mode=big&illust_id=" + imgID
            syslog("opening " + bigImgUrl, LOG_INFO) 
            bigImgContent = urlopenWithRetry(self.urlopener, bigImgUrl)
            if bigImgContent == None:
                syslog("retry too many times at url=" + bigImgUrl, LOG_ERROR)

            bigD = pq(bigImgContent)
            imgUrl = bigD("img").attr("src")
            if imgUrl == None:
                syslog("error!" + " big image url wrong url=" + bigImgUrl, LOG_ERROR)
            else:
                urlList.append(imgUrl)
        return urlList
         
    def initOpener(self):
        cookieJar = cookielib.CookieJar()
        cookie = urllib2.HTTPCookieProcessor(cookieJar)
        opener = urllib2.build_opener(cookie)
        opener.addheaders = [
                ('Referer', 'http://www.pixiv.net/member_illust.php?mode=medium'),
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36')]
        postData = {
                "mode":"login",
                "return_to":"/",
                "pixiv_id":self.args.pixivId,
                "pass":self.args.password
                }
        login_headers = {
                'Referer':'https://www.secure.pixiv.net/login.php',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'
                }
        request = urllib2.Request("https://www.secure.pixiv.net/login.php", urllib.urlencode(postData), headers = login_headers)
        syslog("www.pixiv.net logining!", LOG_INFO)
        urlopenWithRetry(opener, request)
        syslog("login completed!", LOG_INFO)
        return opener
