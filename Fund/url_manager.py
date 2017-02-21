# -*- coding: utf-8 -*-
from enum import Enum, unique
from spider_base import SBURLManager

@unique
class FundURLIndex(Enum):
    MAIN = 0 #主页
    BASE = 1 #基础信息
    RATIO = 2 #持有人比例
    STATISTIC = 3 #特色统计如标准差
    STOCKS = 4 #持仓
    ANNUAL = 5 #年度收益
    CODE = 6 #编号

class FundURLManager(SBURLManager):
    #管理的其实不是真实url,而是code加上相关url
    # def __init__(self):
    #     self.finished_urls = set()
    #     self.feed_urls = set()
    #     self.failed_urls = set()
    #
    # #吃进来的是code
    # def add_url(self, url):
    #     if url not in self.finished_urls and url not in self.feed_urls:
    #         self.feed_urls.add(url)
    #
    # def add_urls(self, urls):
    #     for url in urls:
    #         self.add_url(url)
    #
    # # 加可以批量加,但移除肯定是一个个移除的
    # def finish_url(self, url):
    #     self.feed_urls.discard(url)
    #     self.finished_urls.add(url)
    #
    # def fail_url(self, url):
    #     self.failed_urls.add(url)
    #
    # def is_empyt(self):
    #     return len(self.feed_urls) == 0
    #
    # def is_overflow(self):
    #     return False#len(self.finished_urls) >= 100

    #之前的是通用的,下面重载或者新建函数
    def pop_url(self):
        return self._urlsfromcode(self.feed_urls.pop())

    def output_faileds(self):
        for url in self.failed_urls:
            print "http://fund.eastmoney.com/" + url + '.html'



    def _urlsfromcode(self, code):
        return ["http://fund.eastmoney.com/" + code + '.html',\
                "http://fund.eastmoney.com/f10/jbgk_" + code + '.html',\
                "http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=cyrjg&code=" + code,\
                "http://fund.eastmoney.com/f10/tsdata_" + code + '.html',\
                "http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&code=" + code + "&topline=20",\
                "http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=yearzf&code=" + code,\
                code]