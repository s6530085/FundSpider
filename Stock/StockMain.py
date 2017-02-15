# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from StockParser import *
from StockURLManager import *
from StockDownloader import *
from StockCollector import *
import datetime

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class StockMain(object):

    def __init__(self):
        self.url_manager = StockURLManager()
        self.html_downloader = StockDownloader()
        self.html_paser = StockParser()
        self.collector = StockCollector()

    def craw(self, homeurl, incremental=True):
        #除非指定全量更新,否则都是自动检查是否需要全量的
        #首页怎么都要来一次
        stock_home = self.html_downloader.download(homeurl)
        stocks = self.html_paser.parse_home(stock_home)
        for (code, _) in stocks:
            self.url_manager.add_url(code)

        def _inner_craw(isretry=False):
            if isretry:
                self.url_manager.transfer_url()

            while (not self.url_manager.is_empyt() and not self.url_manager.is_overflow()):
                (code, url) = self.url_manager.pop_url()
                #股票基本信息几乎不会更新,只有强制更新或没有的时候再刷吧
                if not incremental or not self.collector.is_stock_existsin_main(code):
                    stock_content = self.html_downloader.download(url)
                    if stock_content is None or len(stock_content) == 0:
                        print 'download stock info ' + url + ' failed'
                        self.url_manager.fail_url(code)
                        continue
                    stock_info = self.html_paser.parse_stock(stock_content)
                    self.collector.update_stock_info(stock_info)

                #全量就自然是从头开始获取,增量的话会先看数据库,找到最新一条的第二天开始获取,但如果数据库没有,一样是从头获取
                need_update = True
                initdate = datetime.datetime.now().strftime('%Y-%m-%d')
                if incremental:
                    (need_update,initdate) = self.collector.stock_last_update_date(code)
                if need_update:
                    quotation_url = self.url_manager.joint_quotation_url(code, initdate)
                    quotation_content = self.html_downloader.download(quotation_url)
                    if quotation_content is None or len(quotation_content) == 0:
                        print 'download stock quotation ' + url + ' failed'
                        self.url_manager.fail_url(code)
                        continue
                    stock_quotation = self.html_paser.parse_quotation(quotation_content)
                    self.collector.update_stock_quotation(stock_quotation)

        _inner_craw()
        _inner_craw(True)
        _inner_craw(True)


if __name__ == "__main__":
    sk = StockMain()
    sk.craw('http://quote.eastmoney.com/stocklist.html')