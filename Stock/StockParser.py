# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import re
from lxml import etree
from SpiderBase.SBConvenient import safetofloat
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#股票的一日行情
class StockQuotation(object):

    CODE_KEY = 'code'
    CODE_CHINESE_KEY = u'A股代码'

    SHORT_NAME_KEY = 'shortname'
    SHORT_NAME_CHINESE_KEY = u'A股简称'

    PE_KEY = 'pe'
    PE_CHINESE_KEY = u'静态市盈率'

    PE_TTM_KEY = 'pe_ttm'
    PE_TTM_CHINESE_KEY = u'动态市盈率'

    PB_KEY = 'pb'
    PB_CHINENE_KEY = u'市净率'

    PRICE_KEY = 'price'




class StockInfo(object):

    CODE_KEY = 'code'
    CODE_CHINESE_KEY = u'A股代码'

    SHORT_NAME_KEY = 'shortname'
    SHORT_NAME_CHINESE_KEY = u'A股简称'

    FULL_NAME_KEY = 'fullname'
    FULL_NAME_CHINESE_KEY = u'公司名称'

    USED_NAME_KEY = 'usedname'
    USED_NAME_CHINESE_KEY = u'曾用名'

    MARKET_KEY = 'market'
    MARKET_CHINESE_KEY = u'证券类别'

    INDUSTRY_KEY = 'industry'
    INDUSTRY_CHINESE_KEY = u'所属行业'

    RELEASE_DATE_KEY = 'releasedata'
    RELEASE_DATE_CHINESE_KEY = u'上市日期'

    URL_KEY = u'url'
    URL_CHINESE_KEY = u'东方财富介绍页'

    ALL_KEYS = [CODE_KEY, SHORT_NAME_KEY, FULL_NAME_KEY, USED_NAME_KEY, MARKET_KEY, INDUSTRY_KEY, RELEASE_DATE_KEY, URL_KEY]
    ALL_CHINESE_KEYS = [CODE_CHINESE_KEY, SHORT_NAME_CHINESE_KEY, FULL_NAME_CHINESE_KEY, USED_NAME_CHINESE_KEY, MARKET_CHINESE_KEY, INDUSTRY_CHINESE_KEY, RELEASE_DATE_CHINESE_KEY, URL_CHINESE_KEY]

    def __init__(self):
        self.code = u''
        self.shortname = u''
        self.fullname = u''
        self.usednames = []
        self.market = u''
        self.industry = u''
        self.releasedate = u''
        self.url = u''

    def parse_sqlresult(self, sqlresult):
        self.code = sqlresult[0]
        self.shortname = sqlresult[1]
        self.fullname = sqlresult[2]
        self.usednames = sqlresult[3].split(',')
        self.market = sqlresult[4]
        self.industry = sqlresult[5]
        self.releasedate = sqlresult[6]
        self.url = sqlresult[7]

    def __str__(self):
        return self.full_desc()

    #简单的就只打印编号,简称和url
    def short_desc(self):
        return u'{}: {} {}: {} {}: {} '.format(StockInfo.CODE_CHINESE_KEY, self.code, StockInfo.SHORT_NAME_CHINESE_KEY, StockInfo.shortname, StockInfo.URL_CHINESE_KEY, StockInfo.url)


    #全称吗自然全打印咯
    def full_desc(self):
        format = u''
        for i, key in enumerate(StockInfo.ALL_KEYS):
            v = getattr(self, key)
            if isinstance(v, float):
                v = str(v)
            elif isinstance(v, int):
                v = str(v)
            elif isinstance(v, list):
                v = ','.join(v)
            format += StockInfo.ALL_CHINESE_KEYS[i] + ' : ' + v + ' \n'
        return format


class StockParser(object):

    #现在只关心股票哦,逆回购基金什么的不在意
    def _isstock(self, code):
        #分别是沪市,深市和创业板
        return code.startswith('60') or code.startswith('00') or code.startswith('30')


    #解析全股票代码,返回形式是[(600000, 浦发银行)]
    def parse_home(self, content):
        #好气啊,又是源代码里写gb2312,实际要gbk才能解析的
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='gbk'))
        items = html.xpath('//div[@class="quotebody"]//li/a')
        stocks = []
        for item in items:
            #这个i是形如浦发银行(600000)
            i = item.text.strip()
            if len(i.split('(')) == 2:
                name = i.split('(')[0]
                code = i.split('(')[1][0:6]
                if self._isstock(code):
                    stocks.append((code, name))
                #     url = item.attribute('href')
                #     #url形如http://quote.eastmoney.com/sh600009.html,而我们只需要其中的sh600009即可
                #     url = url.split('/')[3].split('.')[0]
                #     stocks.append((code, name, url))

        return stocks

    #解析单个股票的基础信息
    def parse_stock(self, content):
        stock = StockInfo()

        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))

        return stock

    #解析单个股票行情
    def parse_quotation(self, content):
        pass

