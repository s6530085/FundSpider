# -*- coding: utf-8 -*-
__author__ = 'study_sun'

from lxml import etree
import json
import datetime
from entity import StockInfo, StockQuotation
from spider_base.convenient import *
import sys
import xlrd
reload(sys)
sys.setdefaultencoding('utf-8')

class StockParser(object):

    #现在只关心股票哦,逆回购基金什么的不在意
    def _isstock(self, code):
        #分别是沪市,深市和创业板
        return code.startswith('60') or code.startswith('00') or code.startswith('30')

    #现在改由excel读取股票列表了哦
    def parse_list_excel(self, filename):
        listfile = xlrd.open_workbook(filename, on_demand = True)
        codesheet = listfile.sheet_by_name('sheet 1')
        codes = codesheet.col_values(0)
        stocks = []
        for i in range(2, len(codes)):
            codename = codes[i]
            code = codename[2:]
            stocks.append(code)
        return stocks

    #解析全股票代码,返回形式是[600000,]
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
                    stocks.append(code)
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
            if value == '--':
                value = ''
            if key == StockInfo.FULL_NAME_CHINESE_KEY:
                stock.fullname = value
            elif key == StockInfo.USED_NAME_CHINESE_KEY:
                #可能没有哦
                stock.used_names = value.split('->')
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
            # 很奇怪,东方财富是不是网站出问题了,很多退市的公司基础信息都没了,
            elif key == StockInfo.RELEASE_DATE_CHINESE_KEY:
                stock.release_date = value
        return stock

    TODAY_DATE = ''
    #不好意思,比较准的数据如果靠爬虫只有当天的
    #https://xueqiu.com/v4/stock/quote.json?code=SZ399001&_=1460380110118
    def parse_quotation(self, quotation_content):
        content = json.loads(quotation_content, encoding='utf-8')
        quotation = content.values()[0]
        quotation_info = StockQuotation()
        #不过可能是各种情况失败的json哦
        if isinstance(quotation, basestring):
            quotation_info.pe_ttm = 0.0
            quotation_info.pb = 0.0
            quotation_info.pe = 0.0
            quotation_info.opening_price = 0.0
            quotation_info.closing_price = 0.0
            quotation_info.yield_rate = 0.0
            if len(StockParser.TODAY_DATE) == 0:
                quotation_info.s_date = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            quotation_info.pe_ttm = safe_to_float(quotation['pe_ttm'])
            quotation_info.pb = safe_to_float(quotation['pb'])
            quotation_info.pe = safe_to_float(quotation['pe_lyr'])
            quotation_info.opening_price = safe_to_float(quotation['open'])
            quotation_info.closing_price = safe_to_float(quotation['close'])
            quotation_info.yield_rate = safe_to_float(quotation['yield'])
            #time的格式很怪,形如"time": "Wed Mar 08 14:59:50 +0800 2017",
            if len(StockParser.TODAY_DATE) == 0:
                StockParser.TODAY_DATE = datetime.datetime.strptime(quotation['time'], '%a %b %d %X +0800 %Y').strftime("%Y-%m-%d")
            quotation_info.s_date = StockParser.TODAY_DATE
        return quotation_info


if __name__ == "__main__":
    d = StockParser()
    d.parse_home("aaaaa")
    print d
