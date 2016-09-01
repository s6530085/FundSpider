# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

class IndexCompareParser:

    #解析首页主要是获取每个基金的一些基础信息,如基金名,id
    def parse_home(self, home_content):
        if home_content is None:
            return None

        # soup = BeautifulSoup(home_content, 'html.parser', from_encoding='gb2312')
        soup = BeautifulSoup('<a href="http://fund.eastmoney.com/000028.html" fuck="you">呵呵</a>', 'html.parser', from_encoding='utf-8')
        funds = soup.find_all('a', text=re.compile(ur"呵呵"))
        print funds[0].text


    #这里是解析每个基金的详情了,获得的东西很多,反正都在dict里,键可能会逐步增加,根据未来需要分析的东西扩展
    def parse_fund(self, fund_content, fund_url):
        pass
