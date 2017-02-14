# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from StockParser import *
from StockURLManager import *
from StockDownloader import *
from StockCollector import *

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class StockMain(object):

    def __init__(self):
        self.url_manager = StockURLManager()
        self.html_downloader = StockDownloader()
        self.html_paser = StockParser()
        self.collector = StockCollector()

    def craw(self, homeurl, iswhole=False):
        #除非指定全量更新,否则都是自动检查是否需要全量的
        #首页怎么都要来一次
        stock_home = self.html_downloader.download(homeurl)
        stocks = self.html_paser.parse_home(stock_home)
        for (code, _, url) in stocks:
            #股票基本信息几乎不会更新,只有强制更新或没有的时候再刷吧
            if iswhole:
                self.url_manager.add_url(url)

        def _inner_craw(isretry=False):
            if isretry:
                self.url_manager.transfer_url()

            while (not self.url_manager.is_empyt() and not self.url_manager.is_overflow()):
                (url, rawrul) = self.url_manager.pop_url()
                stockcontent = self.html_downloader.download(url)
                if stockcontent is None or len(stockcontent) == 0:
                    print 'download stock ' + url + ' failed'
                    self.url_manager.fail_url(rawrul)
                    continue







if __name__ == "__main__":
    sk = StockMain()
    sk.craw('http://quote.eastmoney.com/stocklist.html')