crawl-me
========

crawl-me 是一个基于plugin的网页图片下载工具。crawl-me通过简单的命令行就可以用你想要的方式下载各个网站下的图片。目前暂时只支持gamersky(游明星空), pixiv（P站），更多plugin尽请期待，欢迎为它添加新的plugin。

TODO
========
目前暂且支持Linux平台 

Installation
========

### 通过git安装
由于代码依赖了pyquery，安装前请确保libxslt-devel libxml2-devel已被安装

Ubuntu下安装

    sudo apt-get install libxml2-dev
    sudo apt-get install libxslt1-dev 
    
然后请确保安装了[setuptools](https://pypi.python.org/pypi/setuptools#downloads "setuptools"), Ubuntu下你可以：

    sudo apt-get install python-setuptools

然后从github clone source到本地

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

Licenses
========

[MIT](http://opensource.org/licenses/MIT "MIT")
