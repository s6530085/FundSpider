# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from lxml import etree
import xlrd
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#股票的一日行情
class StockQuotation(object):

    DATE_KEY = 's_date'
    DATE_CHINESE_KEY = u'日期'

    PE_KEY = 'pe'
    PE_CHINESE_KEY = u'静态市盈率'

    PE_TTM_KEY = 'pe_ttm'
    PE_TTM_CHINESE_KEY = u'动态市盈率'

    PB_KEY = 'pb'
    PB_CHINENE_KEY = u'市净率'

    OPENING_PRICE_KEY = 'opening_price'
    OPENING_PRICE_CHINESE_KEY = u'开盘价'

    CLOSING_PRICE_KEY = 'closing_price'
    CLOSING_PRICE_CHINESE_KEY = u'收盘价'



    #其实很多东西目前用不到,比如成交量等,但既然服务器给了,就先存起来吧

    ALL_KEYS = [DATE_KEY, PE_TTM_KEY, PB_KEY]
    ALL_CHINENE_KEYS = [DATE_CHINESE_KEY, PE_TTM_CHINESE_KEY, PB_CHINENE_KEY]

    def __init__(self):
        self.date = u''
        self.pe_ttm = 0.0
        self.pb = 0.0

    def parse_sqlresult(self, sqlresult):
        pass

    def __str__(self):
        return self.full_desc()

    #简单的就只打印日期,pe和pb
    def short_desc(self):
        return u'{}: {} {}: {} {}: {} '.format(StockQuotation.DATE, self.date, StockQuotation.PE_TTM_CHINESE_KEY, self.pe_ttm, StockQuotation.PB_CHINENE_KEY, self.pb)


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

    #区域在很多时候也很重要,比如有些人就不喜欢东北或者福建的企业
    AREA_KEY = 'area'
    AREA_CHINESE_KEY = u'区域'

    RELEASE_DATE_KEY = 'releasedata'
    RELEASE_DATE_CHINESE_KEY = u'上市日期'

    URL_KEY = u'url'
    URL_CHINESE_KEY = u'东方财富介绍页'

    ALL_KEYS = [CODE_KEY, SHORT_NAME_KEY, FULL_NAME_KEY, USED_NAME_KEY, MARKET_KEY, INDUSTRY_KEY, AREA_KEY, RELEASE_DATE_KEY, URL_KEY]
    ALL_CHINESE_KEYS = [CODE_CHINESE_KEY, SHORT_NAME_CHINESE_KEY, FULL_NAME_CHINESE_KEY, USED_NAME_CHINESE_KEY, MARKET_CHINESE_KEY, INDUSTRY_CHINESE_KEY, AREA_CHINESE_KEY, RELEASE_DATE_CHINESE_KEY, URL_CHINESE_KEY]

    def __init__(self):
        self.code = u''
        self.shortname = u''
        self.fullname = u''
        self.usednames = []
        self.market = u''
        self.industry = u''
        self.area = u''
        self.releasedate = u''
        self.url = u''

    def parse_sqlresult(self, sqlresult):
        self.code = sqlresult[0]
        self.shortname = sqlresult[1]
        self.fullname = sqlresult[2]
        self.usednames = sqlresult[3].split(',')
        self.market = sqlresult[4]
        self.industry = sqlresult[5]
        self.area = sqlresult[6]
        self.releasedate = sqlresult[7]
        self.url = sqlresult[8]

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
        ths = html.xpath('//th[@class="tips-fieldnameL"]')
        tds = html.xpath('//td[contains(@class, "tips-dataL")]')
        for (index, th) in enumerate(ths):
            key = th.text.strip()
            value = tds[index].text.strip()
            if key == StockInfo.FULL_NAME_CHINESE_KEY:
                stock.fullname = value
            elif key == StockInfo.USED_NAME_CHINESE_KEY:
                #可能没有哦
                if value == '--':
                    value = ''
                stock.usednames = value.split('->')
            elif key == StockInfo.CODE_CHINESE_KEY:
                stock.code = value
            elif key == StockInfo.SHORT_NAME_CHINESE_KEY:
                stock.shortname = value
            elif key == StockInfo.MARKET_CHINESE_KEY:
                stock.market = value
            elif key == StockInfo.INDUSTRY_CHINESE_KEY:
                stock.industry = value
            elif key == StockInfo.AREA_CHINESE_KEY:
                stock.area = value
            elif key == StockInfo.RELEASE_DATE_CHINESE_KEY:
                stock.releasedate = value

        return stock

    #解析单个股票行情,喷了,最后发现搜狐没有pe指标,雪球只有当天的,新浪有但是不准
    def parse_quotation(self, code):
        table = xlrd.open_workbook('pe_history.xlsx')



