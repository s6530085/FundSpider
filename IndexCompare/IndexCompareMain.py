# -*- coding: utf-8 -*-
from IndexCompareURLManager import *
from IndexCompareDownloader import *
from IndexCompareOutputer import *
from IndexCompareParser import *
from IndexCompareCollector import *

class IndexCompareMain:

    def __init__(self):
        self.url_manager = IndexCompareURLManager()
        self.html_downloader = IndexCompareDownloader()
        self.html_paser = IndexCompareParser()
        self.collector = IndexCompareCollector()
        self.outputer = IndexCompareOutputer()

    #先定接口，再做实现，其中首页特殊处理一下
    def craw(self, homeurl):
        #先处理首页
        home_content = self.html_downloader.download(homeurl)
        if home_content is None:
            return

        funds_info = self.html_paser.parse_home(home_content)
        if funds_info is None:
            return

        for fund_info in funds_info:
            (code, name) = fund_info
            #其实name根本没用到
            self.url_manager.add_url('http://fund.eastmoney.com/f10/jbgk_' + code + '.html')

        while (not self.url_manager.is_empyt() and not self.url_manager.is_overflow()):
            url = self.url_manager.pop_url()
            content = self.html_downloader.download(url)
            if content is None:
                print 'download' + url + 'failed'
                self.url_manager.add_url(url)
                continue
            self.url_manager.finish_url(url)
            result = self.html_paser.parse_fund(content, url)
            self.collector.addFund(result)
            print 'finish parse url ' + url

        self.collector.chooseTargets([u"无跟踪标"])
        # self.outputer.output_result()



if __name__ == "__main__":
    try:
        icMain = IndexCompareMain()
        icMain.craw('http://fund.eastmoney.com/allfund.html')
    except Exception as e:
        print e
