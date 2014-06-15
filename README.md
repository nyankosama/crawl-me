crawl-me
========

[中文README](https://github.com/nyankosama/crawl-me/wiki/%E4%B8%AD%E6%96%87README).

Crawl-me is a light-weight fast plugin based web picture crawler. You can download your favorite pictures via the plugin if the website is supported. For now, the plugins include gamersky and pixiv. If you want to contribute, please just feel free to contact with me.

Fork me on Github :) [https://github.com/nyankosama/crawl-me](https://github.com/nyankosama/crawl-me)

Features
=======

- Crawl-me core supports muti-thread downloading using http range-headers, so it's very fast.
- It's plugin based, so you can free add any plugin you want. 


Available plugins
============

- pixiv : This plugin allows you to download any author's paintings in [pixiv](http://www.pixiv.net/) site.
- gamersky : This plugin supports downloading all pictures in special topic from [gamersky](http://www.gamersky.com/) site.


Installation
========

## install via pip

Make sure you have already installed [python2.7](https://www.python.org/downloads/) and [pip](https://pypi.python.org/pypi/pip/1.5.6)

Due to the fact that package relies on lxml, if your platform is linux, please make sure you have installed lib libxslt-devel libxml2-devel. And for windows please select a suitable [lxml installer](https://pypi.python.org/pypi/lxml/3.3.5#downloads) to install.

And then:

    $ pip install crawl-me

For windows, please add {$python-home}/Scripts/ to systempath

## install via git

### 1. Ubuntu

Install the prerequisite library first:
    
    sudo apt-get install libxml2-dev
    sudo apt-get install libxslt1-dev 
    
And then you should install [setuptools](https://pypi.python.org/pypi/setuptools#downloads "setuptools") in order to run the setup.py file

    sudo apt-get install python-setuptools

Finally, git clone the source, and install:

    $ git clone https://github.com/nyankosama/crawl-me.git
    $ cd crawl-me/
    $ sudo python setup.py install

### 2. Windows

Make sure you have already installed [python2.7](https://www.python.org/downloads/) and [pip](https://pypi.python.org/pypi/pip/1.5.6).

You can install python2.7 via windows installer. You can install pip via downloading the [get-pip.py](https://bootstrap.pypa.io/get-pip.py), and run it via python:

    python get-pip.py

And then install the prerequisite library lxml. please select a suitable [lxml installer](https://pypi.python.org/pypi/lxml/3.3.5#downloads) to install.

Finally git clone the source, and install:
    
    $ git clone https://github.com/nyankosama/crawl-me.git
    $ cd crawl-me/
    $ sudo python setup.py install

For windows, please add {$python-home}/Scripts/ to systempath

Usage
========

## Examples

1. Download 10 pages pictures at the url of http://www.gamersky.com/ent/201404/352055.shtml in gamersky site, and store the pictures into local direcotry.

        crawl-me gamersky http://www.gamersky.com/ent/201404/352055.shtml ./gamersky-crawl 1 10

2. Download all the paintings of 藤原(Fujiwara, Pixiv ID=27517), and store them into local directory. 
        
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

- Functions:
    - support breakpoint resume

- Plugins:
    - weibo
    - qq zone

Licenses
========

[MIT](http://opensource.org/licenses/MIT "MIT")
