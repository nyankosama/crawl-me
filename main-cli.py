import argparse
import sys
from only_crawl.common.utils import *
from only_crawl.plugin import *
from only_crawl.common.crawlercore import CrawlerManager

availableModule = [
        "gamersky",
        ]

def printHelp(parser):
    parser.print_help()
    print ""
    print "available modules:"
    for module in availableModule:
        print "----" + module
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('plugin', help='plugin the crawler uses')
    if len(sys.argv) < 2:
        printHelp(parser)
        sys.exit(0)
    
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        printHelp(parser)
        sys.exit(0)

    pluginName = sys.argv[1]
    try:
        module = dynamicImport("only_crawl.plugin." + pluginName)
    except Exception, e:
        syslog("moudle not found! moudleName:%s" % (pluginName), LOG_ERROR)
        printHelp(parser)
        sys.exit(-1)

    class_ = getattr(module, pluginName[0].upper() + pluginName[1:] + "Handler")
    plugin = class_()
    args = plugin.initPara(parser)
    opener = plugin.initOpener()
    urlList = plugin.getUrlList()
    manager = CrawlerManager(args.savePath, opener, urlList) 
    manager.startCrawl()
