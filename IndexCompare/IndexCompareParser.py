# -*- coding: utf-8 -*-

class IndexCompareParser:

    #解析首页主要是获取每个基金的一些基础信息,如基金名,id
    def parse_home_url(self, content):
        if content is None:
            return None



    #这里是解析每个基金的详情了,获得的东西很多,反正都在dict里,键可能会逐步增加,根据未来需要分析的东西扩展
    def parse_fund_url(self, content):
        pass

