import unittest
import urllib2
from crawl_me.common import utils

class UtilsTest(unittest.TestCase):

    def setUp(self):
        self.opener = urllib2.build_opener()
        self.commonUrl = "http://www.google.com"
        self.downloadUrl = "http://img1.gamersky.com/image2014/06/20140613tqy_4/gamersky_19origin_37_20146132063C9.jpg" 

    def test_urlOpenAndReadWithRetry(self):
        res = utils.urlopenWithRetry(self.opener, self.commonUrl)
        self.assertNotEqual(res, None)
        content = utils.resReadWithRetry(self.opener, self.commonUrl, res) 
        self.assertNotEqual(content, None)

    def test_urlReadWithRetry(self):
        content = utils.urlReadWithRetry(self.opener, self.commonUrl)
        self.assertNotEqual(content, None)
    
    def test_checkRangeHeader(self):
        ret = utils.checkRangeHeaderSupport(self.opener, self.downloadUrl)
        self.assertEqual(ret, True)
