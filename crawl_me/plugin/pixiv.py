import urllib

from pyquery import PyQuery as pq

from pageBasedHandler import *
from ..common.utils import *


def getUrlFromId(memberID):
    url = 'http://www.pixiv.net/member_illust.php?id=' + str(memberID)
    return url


class PixivHandler(PageBasedHandler):
    def getPageUrl(self, opener, conf):
        urlList = list()
        openUrl = conf["url"]
        while True:
            htmlContent = urlReadWithRetry(opener, openUrl)
            if htmlContent == None:
                syslog("pixiv plugin pageCrawl init fail! timeout retry too many times, url=%s" % (conf["url"]), LOG_ERROR)
                sys.exit(1)
            d = pq(htmlContent)
            pageLi = d(".page-list").eq(0)("li")
        
            size = pageLi.size()
            if size <= 5:
                if size == 0:
                    pageNum = 1
                else:
                    lastLi = pageLi.eq(size - 1)
                    if lastLi.find("a").html() != None:
                        pageNum = int(lastLi.find("a").html())
                    else:
                        pageNum = int(pageLi.eq(size - 1).html())
                break
            else:
                openUrl = conf["url"] + "&p=" + str(pageLi.eq(size - 1).find("a").html())

        syslog("total " + str(pageNum) + " pages", LOG_INFO)
        urlList.append(conf["url"])
        for page in range(2, pageNum + 1):
            urlList.append(conf["url"] + "&p=" + str(page))
        return urlList

    def getPictureUrl(self, pageUrl, opener):
        urlList = list()
        htmlContent = urlReadWithRetry(opener, pageUrl)
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
            bigImgContent = urlReadWithRetry(opener, bigImgUrl)
            if bigImgContent == None:
                syslog("retry too many times at url=" + bigImgUrl, LOG_ERROR)

            bigD = pq(bigImgContent)
            imgUrl = bigD("img").attr("src")
            if imgUrl == None:
                syslog("error!" + " big image url wrong url=" + bigImgUrl, LOG_ERROR)
            else:
                urlList.append(imgUrl)
        return urlList

    def initOpener(self, conf):
        cookieJar = cookielib.CookieJar()
        cookie = urllib2.HTTPCookieProcessor(cookieJar)
        opener = urllib2.build_opener(cookie)
        opener.addheaders = [
            ('Referer', 'http://www.pixiv.net/member_illust.php?mode=medium'),
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36')]
        postData = {
            "mode": "login",
            "return_to": "/",
            "pixiv_id": conf["pixivId"],
            "pass": conf["password"]
        }
        login_headers = {
            'Referer': 'https://www.secure.pixiv.net/login.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'
        }
        request = urllib2.Request("https://www.secure.pixiv.net/login.php", urllib.urlencode(postData),
                                  headers=login_headers)
        syslog("www.pixiv.net logining!", LOG_INFO)
        urlopenWithRetry(opener, request)
        syslog("login completed!", LOG_INFO)
        self.opener = opener
        return opener

    def initPara(self, parser):
        parser.add_argument('authorId', help='the author id you want to crawl')
        parser.add_argument('savePath', help='the path where the imgs ars saved')
        parser.add_argument('pixivId', help='your pixiv login id')
        parser.add_argument('password', help='your pixiv login password')
        args = parser.parse_args()
        return {
            "url": getUrlFromId(args.authorId),
            "savePath": args.savePath,
            "pixivId": args.pixivId,
            "password": args.password
        }
