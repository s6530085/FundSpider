# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from spider_base.entity import SBObject

#股票的一日行情
class StockQuotation(SBObject):

    DATE_KEY = 's_date'
    DATE_CHINESE_KEY = u'日期'

    PE_TTM_KEY = 'pe_ttm'
    PE_TTM_CHINESE_KEY = u'动态市盈率'

    PB_KEY = 'pb'
    PB_CHINENE_KEY = u'市净率'

    #其实很多东西目前用不到,先写个key占位,但没有存储到数据库里,防止因为空数据导致过大
    #另外就是历史数据也是很多没有的,但可以保证一定有pe_ttm和pb可供分析
    PE_KEY = 'pe'
    PE_CHINESE_KEY = u'静态市盈率'

    OPENING_PRICE_KEY = 'opening_price'
    OPENING_PRICE_CHINESE_KEY = u'开盘价'

    CLOSING_PRICE_KEY = 'closing_price'
    CLOSING_PRICE_CHINESE_KEY = u'收盘价'

    YIELD_KEY = 'yield_rate'
    YIELD_CHINESE_KEY = u'股息率'

    @classmethod
    def all_keys(cls):
        return [StockQuotation.DATE_KEY, StockQuotation.PE_TTM_KEY, StockQuotation.PB_KEY
            # , StockQuotation.PE_KEY,StockQuotation.OPENING_PRICE_KEY, StockQuotation.CLOSING_PRICE_KEY, StockQuotation.YIELD_KEY
                ]

    @classmethod
    def all_desc_keys(cls):
        return [StockQuotation.DATE_CHINESE_KEY, StockQuotation.PE_TTM_CHINESE_KEY, StockQuotation.PB_CHINENE_KEY,
                # StockQuotation.PE_CHINESE_KEY, StockQuotation.OPENING_PRICE_CHINESE_KEY,
                # StockQuotation.CLOSING_PRICE_CHINESE_KEY, StockQuotation.YIELD_CHINESE_KEY
                ]

    def __init__(self):
        self.s_date = u''
        self.pe_ttm = 0.0
        self.pb = 0.0
        # self.pe = 0.0
        # self.opening_price = 0.0
        # self.closing_price = 0.0
        # self.yield_rate = 0.0


    def parse_sqlresult(self, sqlresult):
        self.s_date = sqlresult[0]
        self.pe_ttm = sqlresult[1]
        self.pb = sqlresult[2]
        # self.pe = sqlresult[3]


    #简单的就只打印日期,pe和pb
    def short_desc(self):
        return u'{}: {} {}: {} {}: {} '.format(StockQuotation.DATE_CHINESE_KEY, self.date, StockQuotation.PE_TTM_CHINESE_KEY, self.pe_ttm, StockQuotation.PB_CHINENE_KEY, self.pb)


class StockInfo(SBObject):

    CODE_KEY = 'code'
    CODE_CHINESE_KEY = u'A股代码'

    SHORT_NAME_KEY = 'shortname'
    SHORT_NAME_CHINESE_KEY = u'A股简称'

    FULL_NAME_KEY = 'fullname'
    FULL_NAME_CHINESE_KEY = u'公司名称'

    USED_NAME_KEY = 'used_names'
    USED_NAME_CHINESE_KEY = u'曾用名'

    MARKET_KEY = 'market'
    MARKET_CHINESE_KEY = u'证券类别'

    INDUSTRY_KEY = 'industry'
    INDUSTRY_CHINESE_KEY = u'所属行业'

    #区域在很多时候也很重要,比如有些人就不喜欢东北或者福建的企业
    AREA_KEY = 'area'
    AREA_CHINESE_KEY = u'区域'

    RELEASE_DATE_KEY = 'release_date'
    RELEASE_DATE_CHINESE_KEY = u'上市日期'

    URL_KEY = u'url'
    URL_CHINESE_KEY = u'东方财富介绍页'

    @classmethod
    def all_keys(cls):
        return [StockInfo.CODE_KEY, StockInfo.SHORT_NAME_KEY, StockInfo.FULL_NAME_KEY, StockInfo.USED_NAME_KEY, StockInfo.MARKET_KEY,
                StockInfo.INDUSTRY_KEY, StockInfo.AREA_KEY, StockInfo.RELEASE_DATE_KEY, StockInfo.URL_KEY]

    @classmethod
    def all_desc_keys(cls):
        return [StockInfo.CODE_CHINESE_KEY, StockInfo.SHORT_NAME_CHINESE_KEY, StockInfo.FULL_NAME_CHINESE_KEY,
                StockInfo.USED_NAME_CHINESE_KEY, StockInfo.MARKET_CHINESE_KEY, StockInfo.INDUSTRY_CHINESE_KEY,
                StockInfo.AREA_CHINESE_KEY, StockInfo.RELEASE_DATE_CHINESE_KEY, StockInfo.URL_CHINESE_KEY]

    def __init__(self):
        self.code = u''
        self.shortname = u''
        self.fullname = u''
        self.used_names = []
        self.market = u''
        self.industry = u''
        self.area = u''
        self.release_date = u''
        self.url = u''

    def parse_sqlresult(self, sqlresult):
        self.code = sqlresult[0]
        self.shortname = sqlresult[1]
        self.fullname = sqlresult[2]
        self.used_names = sqlresult[3].split(',')
        self.market = sqlresult[4]
        self.industry = sqlresult[5]
        self.area = sqlresult[6]
        self.release_date = sqlresult[7]
        self.url = sqlresult[8]


    #简单的就只打印编号,简称和url
    def short_desc(self):
        return u'{}: {} {}: {} {}: {} '.format(StockInfo.CODE_CHINESE_KEY, self.code, StockInfo.SHORT_NAME_CHINESE_KEY, StockInfo.shortname, StockInfo.URL_CHINESE_KEY, StockInfo.url)
