# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import csv
import codecs
import scrapy
import requests
import sys
from scrapy.selector import Selector
reload(sys)                      # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')

class XmlaSpider(scrapy.Spider):
    name = "xmly"
    allowed_domains = ["ximalaya.com"]
    baseUrl = 'http://www.ximalaya.com'

    headers = {
        "Host":"www.ximalaya.com",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Referer":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    }
    start_urls = 'http://www.ximalaya.com/dq/all/'
    data = []
    for num in range(2,87):
        try:
            tmpUrl = "{start_urls}{num}.ajax?_toSub_=true&toSub=true".format(start_urls = start_urls, num = num)
            print tmpUrl
            res = requests.get(tmpUrl, headers=headers)
            a = Selector(text=(eval(res.content))['html'])
            album_items = a.css('div.discoverAlbum_item')
            for album in album_items:
                albumName = album.xpath('div/a/span/img/@alt').extract()[0]
                playTime = album.xpath('div/div/span/text()').extract()[0]
                a = (albumName, playTime)
                data.append(a)
        except:
            pass
    print data
    with open("xmly.csv", "wb") as f:
        f.write(codecs.BOM_UTF8)
        writer = csv.writer(f)
        writer.writerow(['目录集','播放数'])
        writer.writerows(data)