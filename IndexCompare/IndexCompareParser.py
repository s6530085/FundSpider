# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

class IndexCompareParser:

    #解析首页主要是获取每个基金的一些基础信息,如基金名,id
    def parse_home(self, home_content):
        if home_content is None:
            return None
        pattern_match = re.compile(ur"（\d{6}）.+")
        pattern_capture = re.compile(ur"（(\d{6})）(.+)")
        # soup = BeautifulSoup(home_content, 'html.parser', from_encoding='gb2312')
        soup = BeautifulSoup(home_content, 'html.parser', from_encoding='utf-8')
        funds = soup.find_all('a', text=pattern_match)
        l = []
        for fund in funds:
            match = pattern_capture.match(fund.text)
            if match:
                l.append((match.group(1), match.group(2)))

        return l

    #这里是解析每个基金的详情了,获得的东西很多,反正都在dict里,键可能会逐步增加,根据未来需要分析的东西扩展
    def parse_fund(self, fund_content, fund_url):
        pass
