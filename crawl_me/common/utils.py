import sys
import socket
import os
import threading
import urllib2
import cookielib
import copy
from ..sysconf import *

def urlopenWithRetry(opener, request, timeout=URL_OPEN_TIMEOUT, retryTime=URL_OPEN_RETRY_TIME):
    if isinstance(request, urllib2.Request):
        url = request.get_full_url()
    else:
        url = request

    while retryTime >= 0 :
        try:
            return opener.open(request, timeout=timeout)
        except socket.timeout, e1:
            retryTime -= 1 
            #syslog("http timeout, retry again.(retry remains %s) url=%s" % (retryTime, url), LOG_ERROR)
            continue
        except urllib2.HTTPError, error:
            if error.code == 404:
                syslog("http error 404 not found, url=%s" % (url), LOG_ERROR)
                return None
        except Exception, e2:
            syslog(str(e2) + " (retry remains %s)" % (retryTime) +", at url=" + url, LOG_ERROR)
            retryTime -= 1
            continue
    return None

def resReadWithRetry(opener, request, response, timeout=URL_OPEN_TIMEOUT, retryTime=URL_OPEN_RETRY_TIME):
    if isinstance(request, urllib2.Request):
        url = request.get_full_url()
    else:
        url = request
    needRetry = False
    if response == None:
        return None
    while retryTime >= 0 :
        try:
            if needRetry == False:
                return response.read()
            else:
                return opener.open(request, timeout=timeout).read()
        except socket.timeout, e1:
            retryTime -= 1 
            #syslog("response read http timeout, retry again.(retry remains %s), url=%s" % (retryTime, url), LOG_ERROR)
            needRetry = True
            continue
        except Exception, e2:
            syslog(str(e2) + " (retry remains %s)" % (retryTime) + ", at url=" + url, LOG_ERROR)
            retryTime -= 1
            needRetry = True
            continue
    return None

def urlReadWithRetry(opener, request, timeout=URL_OPEN_TIMEOUT, retryTime=URL_OPEN_RETRY_TIME):
    return resReadWithRetry(opener, request, urlopenWithRetry(opener, request, timeout, retryTime), timeout, retryTime)

def upDiv(a, b):
    return (a+b-1) / b

def getShardingConf(size, maxThreadCount=MAX_THREAD_COUNT, perferedSplitNum=SPLIT_NUM):
    tmpCount = upDiv(size, perferedSplitNum)
    if tmpCount > maxThreadCount:
        tmpCount = maxThreadCount
    
    splitNum = upDiv(size, tmpCount)
    downloadCount = tmpCount
    return [splitNum, downloadCount]

def getPathWithSep(path):
    if path[len(path) - 1] != os.sep:
        return path + os.sep
    else:
        return path

def createDir(savePath):
    #create dir
    if os.path.isdir(savePath) is not True:
        os.makedirs(savePath)

#following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)

#constant
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR = range(4)
level_str = ["DEBUG", "INFO", "WARNING", "ERROR"]

def getLogColour(level):
    color_range = [WHITE, GREEN, YELLOW, RED]
    return color_range[level]

syslogLock = threading.Lock()

def syslog(text, level=LOG_INFO):
    syslogLock.acquire()
    if has_colours:
        seq = "\x1b[1;%dm" % (30+getLogColour(level)) + "[%s]: " % (level_str[level]) + "\x1b[0m"
        sys.stdout.write(seq)
        sys.stdout.write(text + "\n")
    else:
        sys.stdout.write(text + "\n")
    syslogLock.release()

def dynamicImport(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

#default only copy opener's headers and cookiejar'
def openerDefaultClone(oldOpener, oldCookieJar = None):
    for handler in oldOpener.handlers:
        if isinstance(handler, urllib2.HTTPCookieProcessor):
            oldCookieJar = handler.cookiejar
    newCookieJar = cookielib.CookieJar()
    if oldCookieJar != None:
        newCookieJar._cookies = copy.deepcopy(oldCookieJar._cookies) 
        newCookieJar._policy = copy.deepcopy(oldCookieJar._policy)
    newOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(newCookieJar))
    newOpener.addheaders = copy.deepcopy(oldOpener.addheaders)
    return newOpener
