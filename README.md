crawl-me
========

crawl-me 是一个基于plugin的网页图片下载工具。crawl-me通过简单的命令行就可以用你想要的方式下载各个网站下的图片。目前暂时只支持gamersky(游明星空), pixiv（P站），更多plugin尽请期待，欢迎为它添加新的plugin。


Installation
========

### 通过git安装

1. ####Ubuntu下安装

    由于代码依赖了pyquery，安装前请确保libxslt-devel libxml2-devel已被安装
    
        sudo apt-get install libxml2-dev
        sudo apt-get install libxslt1-dev 
    
    然后请确保安装了[setuptools](https://pypi.python.org/pypi/setuptools#downloads "setuptools"), Ubuntu下你可以：

        sudo apt-get install python-setuptools

    然后从github clone source到本地

        $ git clone https://github.com/nyankosama/crawl-me.git
        $ cd crawl-me/
        $ sudo python setup.py install

2. ####Windows下安装

    首先你需要安装[python2.7](https://www.python.org/download/releases/2.7.7/)和[pip](https://pip.pypa.io/en/latest/installing.html)，python2.7可以通过windows installer安装。安装pip首先下载[get-pip.py](https://bootstrap.pypa.io/get-pip.py)， 然后执行下面命令。
    
        python get-pip.py
    
    然后，你需要安装pyquery的所依赖的lxml，选择对应的[lxml installer](https://pypi.python.org/pypi/lxml/3.3.5#downloads)下载并安装
    
    最后从github clone 到本地
    
        $ git clone https://github.com/nyankosama/crawl-me.git
        $ cd crawl-me/
        $ sudo python setup.py install
    

Usage
========
### Examples
1. 下载gamersky下的http://www.gamersky.com/ent/201404/352055.shtml
的第1页到第10页的所有图片到当前目录的gamersky-crawl文件夹下
    
        crawl-me gamersky http://www.gamersky.com/ent/201404/352055.shtml ./gamersky-crawl 1 10

2.  下载pixiv中id为3878890的用户的所有作品到pixiv-crawl文件下
        
        crawl-me pixiv 3878890 ./pixiv-crawl <your pixiv id> <your password>

### Command line options
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
        
        usage: crawl-me [-h] plugin authorId savePath pixivId password

        positional arguments:
            plugin      plugin the crawler uses
            authorId    the author id you want to crawl
            savePath    the path where the imgs ars saved
            pixivId     your pixiv login id
            password    your pixiv login password

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
