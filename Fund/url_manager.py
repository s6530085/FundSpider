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
    ASSET = 6 #资产配置
    CODE = 7 #编号

class FundURLManager(SBURLManager):

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
                "http://fund.eastmoney.com/f10/zcpz_" + code + ".html",\
                code]