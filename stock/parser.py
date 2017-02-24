# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from lxml import etree
import xlrd
import sys
from entity import StockInfo
reload(sys)
sys.setdefaultencoding('utf-8')

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



