import argparse
import sys
from only_crawl.common.utils import *
from only_crawl.plugin import *
from only_crawl.common.crawlercore import CrawlerManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('plugin', help='plugin the crawler uses')
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    
    pluginName = sys.argv[1]
    module = dynamicImport("only_crawl.plugin." + pluginName)
    class_ = getattr(module, pluginName[0].upper() + pluginName[1:] + "Handler")
    plugin = class_()
    args = plugin.initPara(parser)
    opener = plugin.initOpener()
    urlList = plugin.getUrlList()
    manager = CrawlerManager(args.savePath, opener, urlList) 
    manager.startCrawl()
