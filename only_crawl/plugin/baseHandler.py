from ..third_party.abc import ABCMeta, abstractmethod

class BaseConf():
    def __init__(self, url, savePath):
        self.url = url
        self.savePath = savePath

class BaseHandler():
    @abstractmethod
    def initPara(self):pass

    @abstractmethod
    def initOpener(self):pass
    
    @abstractmethod
    def getUrlList(self, conf):pass
