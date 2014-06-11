crawl-me
========

crawl-me是一个基于plugin的轻量级快速网页图片下载工具。crawl-me通过简单的命令行就可以用你想要的方式下载各个网站下的图片。目前暂时只支持gamersky(游明星空), pixiv（P站），更多plugin尽请期待，欢迎为它添加新的plugin。

Fork me on Github :) [https://github.com/nyankosama/crawl-me](https://github.com/nyankosama/crawl-me)


Features
=======

- 支持Http range-headers 并发分段下载，速度更快
- 支持添加plugin自定义新的行为，例如添加对微博的支持


Available plugins
============

- pixiv : P站图片下载插件，支持下载某P主所有作品
- gamersky : 游明星空图库下载插件，支持下载游民星空图库中的某一个专题的所有图片


Installation
========

## 通过pip安装

首先请确保已安装python2.7和pip

由于代码依赖了pyquery，linux下请先确保libxslt-devel libxml2-devel已安装，windows下选择对应的[lxml installer](https://pypi.python.org/pypi/lxml/3.3.5#downloads)下载并安装。

以上步骤完成后，只需执行下面的命令

    $ pip install crawl-me

windows平台下使用crawl-me命令之前，请确保把{$python-home}/Scripts/ 加入Windows环境变量中


## 通过git安装

### 1. Ubuntu下安装

由于代码依赖了pyquery，安装前请确保libxslt-devel libxml2-devel已被安装
    
    sudo apt-get install libxml2-dev
    sudo apt-get install libxslt1-dev 
    
然后请确保安装了[setuptools](https://pypi.python.org/pypi/setuptools#downloads "setuptools"), Ubuntu下你可以：

    sudo apt-get install python-setuptools

然后从github clone source到本地

    $ git clone https://github.com/nyankosama/crawl-me.git
    $ cd crawl-me/
    $ sudo python setup.py install

### 2. Windows下安装

首先你需要安装[python2.7](https://www.python.org/download/releases/2.7.7/)和[pip](https://pip.pypa.io/en/latest/installing.html)，python2.7可以通过windows installer安装。安装pip首先下载[get-pip.py](https://bootstrap.pypa.io/get-pip.py)， 然后执行下面命令。
    
    python get-pip.py
    
然后，你需要安装pyquery的所依赖的lxml，选择对应的[lxml installer](https://pypi.python.org/pypi/lxml/3.3.5#downloads)下载并安装
    
最后从github clone 到本地
    
    $ git clone https://github.com/nyankosama/crawl-me.git
    $ cd crawl-me/
    $ sudo python setup.py install
    
在使用crawl-me之前，请确保把{$python-home}/Scripts/ 加入Windows环境变量中
    

Usage
========

## Examples

1. 下载gamersky下的http://www.gamersky.com/ent/201404/352055.shtml
的第1页到第10页的所有图片到当前目录的gamersky-crawl文件夹下
    
        crawl-me gamersky http://www.gamersky.com/ent/201404/352055.shtml ./gamersky-crawl 1 10

2. 一键下载P站藤原桑的所有作品到pixiv-crawl文件夹（藤原桑的id是27517）
        
        crawl-me pixiv 27517 ./pixiv-crawl <your pixiv loginid> <your password>

## Command line options

1. general help

        $ crawl-me -h    
    
        usage: crawl-me [-h] plugin

        positional arguments:
            plugin      plugin the crawler uses
        
        optional arguments:
            -h, --help  show this help message and exit
    
        available plugins:
        ----gamersky
        ----pixiv

2. gamersky

        $ crawl-me gamersky -h
        
        usage: crawl-me [-h] plugin url savePath beginPage endPage

        positional arguments:
            plugin      plugin the crawler uses
            url         your url to crawl
            savePath    the path where the imgs ars saved
            beginPage   the page where we start crawling
            endPage     the page where we end crawling 
        
        optional arguments:
            -h, --help  show this help message and exit

3. pixiv
        
        $ crawl-me pixiv -h

        usage: crawl-me [-h] plugin authorId savePath pixivId password

        positional arguments:
            plugin      plugin the crawler uses
            authorId    the author id you want to crawl
            savePath    the path where the imgs ars saved
            pixivId     your pixiv login id
            password    your pixiv login password
        
        optional arguments:
            -h, --help  show this help message and exit

TODO
========

- 添加通过pip安装的支持
- 添加自动判断Server是否支持HTTP Range headers的支持


Licenses
========

[MIT](http://opensource.org/licenses/MIT "MIT")
