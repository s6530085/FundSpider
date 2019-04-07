# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from url_manager import *
from downloader import *
from collector import *
from stock_parser import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class StockMain(object):

    def __init__(self, path=''):
        self.url_manager = StockURLManager()
        self.downloader = StockDownloader()
        self.parser = StockParser()
        self.collector = StockCollector(path)

    def crawl(self, incremental=True):
        # homeurl = 'http://quote.eastmoney.com/stocklist.html'
        #除非指定全量更新,否则都是自动检查是否需要全量的
        #首页怎么都要来一次
        # stock_home = self.downloader.download(homeurl)
        # stocks = self.parser.parse_home(stock_home)
        # stocks = ['000621']
        stocklisturl = "http://stock.gtimg.cn/data/get_hs_xls.php?id=ranka&type=1&metric=chr";
        listname = self.downloader.download_file(stocklisturl)
        stocks = self.parser.parse_list_excel(listname)
        for code in stocks:
            self.url_manager.add_url(code)
        stock_count = len(stocks)
        finish_count = [0]
        print '共需处理股票行情{}个'.format(stock_count)

        #因为数据的原因,历史记录改为提前加载
        if not incremental:
            self.collector.load_stock_history_quotation(stocks)
            print 'load history finish'

        def _inner_crawl(isretry=False):
            if isretry:
                self.url_manager.transfer_url()

            while (not self.url_manager.is_empyt() and not self.url_manager.is_overflow()):
                (code, url, infourl, quotation_url) = self.url_manager.pop_url()
                print 'start parst stock ' + code
                try:
                    # 股票基本信息几乎不会更新,只有强制更新或没有的时候再刷吧
                    # 目前发现很多退市的股票缺乏信息了,但也无关大雅,因为退市的自然没有最新行情了
                    if not incremental or not self.collector.is_stock_exists_in_main(code):
                        stock_content = self.downloader.download(url)
                        if stock_content is None or len(stock_content) == 0:
                            print 'download stock info ' + url + ' failed'
                            self.url_manager.fail_url(code)
                            continue
                        stock_info = self.parser.parse_stock(stock_content)
                        stock_info.code = code
                        stock_info.url = infourl
                        self.collector.update_stock_info(stock_info)

                    # 全量是从本地文件里先转为数据库数据,然后再尝试获取最新一天的数据,增量只能获得最近一天的数据
                    # 为什么这么做是数据使然,可靠的历史数据并不能从网络上爬虫获得,而是在各种专业的收费软件中导出,所以就是全量的时候先从历史文件
                    # 中加载历史数据,之后和增量一致从网络中爬取最新一天的数据
                    if not incremental:
                        self.collector.load_stock_history_quotation(code)
                    # 看看今天是否需要有行情哦,有几种可能,比如今天不开市,不过更可能的是在重试流程里,本日本股行情已经爬过了,没必要再爬
                    if self.collector.is_stock_need_update_quotation(code):
                        quotation_content = self.downloader.download(quotation_url)
                        if quotation_content is None or len(quotation_content) == 0:
                            print 'download stock quotation ' + quotation_url + ' failed'
                            self.url_manager.fail_url(code)
                            continue

                        quotation_info = self.parser.parse_quotation(quotation_content)
                        finish_count[0] += 1
                        # 已经退市的就没必要更新了
                        if len(quotation_info.s_date) > 0:
                            self.collector.update_stock_quotation(code, quotation_info)
                        print 'finish stock ' + code + " quotation parse " + str(finish_count[0]) + ' / ' + str(stock_count)
                except Exception as e:
                    print 'parse stock ' + code + ' fail, cause ' + str(e)
                    self.url_manager.fail_url(code)

        _inner_crawl()
        _inner_crawl(True)
        _inner_crawl(True)

        print 'success stock count is ' + str(finish_count[0])
        print 'failed stock is'
        self.url_manager.output_faileds()


def random_rich(count, init, round):
    a = list()
    # 一上来每个人都有init元
    for i in count:
        a.append(init)
    # 开始round轮的公平随机输赢
    for i in round:
        for n in count:
            # 已经为0就出局了
            if a[n] == 0:
                continue


    # 最后打印出结果
    print "最后结果为: "
    print a

def sameday(count):
    r = 1
    for i in range(1, count):
        r *= (365-i)/365.0
    return 1 - r




if __name__ == "__main__":
    sk = StockMain()
    sk.crawl(incremental=True)