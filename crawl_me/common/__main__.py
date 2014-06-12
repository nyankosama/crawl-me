import argparse

from utils import *
from crawlercore import CrawlerManager
from ..sysconf import *


def printHelp(parser):
    parser.print_help()
    print ""
    print "available plugins:"
    for module in AVAILABLE_MODULES:
        print "----" + module

def handlePreArgs(parser):
    preArg = sys.argv[1]
    if preArg == "-h" or preArg == "--help":
        printHelp(parser)
        sys.exit(0)
    elif preArg == "-v" or preArg == "--version":
        print "version: %s" % (PROJECT_CONF["version"]) 
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('plugin', help='plugin the crawler uses')
    if len(sys.argv) < 2:
        printHelp(parser)
        sys.exit(0)

    handlePreArgs(parser) 

    pluginName = sys.argv[1]
    try:
        module = dynamicImport("crawl_me.plugin." + pluginName)
    except Exception, e:
        syslog(str(e), LOG_DEBUG)
        syslog("moudle not found! moudleName:%s" % (pluginName), LOG_ERROR)
        printHelp(parser)
        sys.exit(-1)

    class_ = getattr(module, pluginName[0].upper() + pluginName[1:] + "Handler")
    plugin = class_()
    conf = plugin.initPara(parser)
    opener = plugin.initOpener(conf)
    urlList = plugin.getUrlList(conf)
    if len(urlList) == 0:
        syslog("picture not found in the base url", LOG_ERROR)
        sys.exit(-1)
    syslog("total pictures to crawl:%s" % (len(urlList)))
    manager = CrawlerManager(opener, urlList, conf["savePath"])
    manager.startCrawl()
