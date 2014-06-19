import unittest
import os
import shutil
from crawl_me.common.crawlercore import *
from crawl_me.plugin import gamersky

def testPlugin(plugin, conf):
    opener = plugin.initOpener(conf)
    urlList = plugin.getUrlList(conf)
    manager = CrawlerManager(opener, urlList, conf["savePath"])
    manager.startCrawl()
    shutil.rmtree("./tmp")

class PluginsTest(unittest.TestCase):

    def test_gamersky(self):
        plugin = gamersky.GamerskyHandler()
        conf = {
            "url":"http://www.gamersky.com/ent/201406/371882.shtml",
            "savePath": "./tmp",
            "beginPage": 1,
            "endPage": 1
        }
        testPlugin(plugin, conf)

if __name__== '__main__':
    unittest.main()
