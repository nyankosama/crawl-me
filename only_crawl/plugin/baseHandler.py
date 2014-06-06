from ..third_party.abc import ABCMeta, abstractmethod

class BaseHandler():
    @abstractmethod
    def initPara(self):pass

    @abstractmethod
    def initOpener(self):pass
    
    @abstractmethod
    def getUrlList(self):pass
