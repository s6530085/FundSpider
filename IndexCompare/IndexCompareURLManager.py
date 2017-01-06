# -*- coding: utf-8 -*-

class IndexCompareURLManager(object):
    #管理的其实不是真实url,而是code加上相关url
    def __init__(self):
        self.finished_urls = set()
        self.feed_urls = set()
        self.failed_urls = set()

    #吃进来的是code
    def add_url(self, url):
        if url not in self.finished_urls and url not in self.feed_urls:
            self.feed_urls.add(url)

    def add_urls(self, urls):
        for url in urls:
            self.add_url(url)

    # 加可以批量加,但移除肯定是一个个移除的
    def finish_url(self, url):
        self.feed_urls.discard(url)
        self.finished_urls.add(url)

    def fail_url(self, url):
        self.failed_urls.add(url)

    def is_empyt(self):
        return len(self.feed_urls) == 0

    def is_overflow(self):
        return False #len(self.finished_urls) >= 2

    #吐出来的是若干页面,先用list表示,第一是基础页面,第二是f10,第三是持有者结构,第四是标准差
    FUND_URL_INDEX_MAIN = 0
    FUND_URL_INDEX_BASE = 1
    FUND_URL_INDEX_RATIO = 2
    FUND_URL_INDEX_STATISTIC = 3
    FUND_URL_INDEX_CODE = 4
    def pop_url(self):
        return self.__urlsfromcode(self.feed_urls.pop())

    def output_faileds(self):
        for url in self.failed_urls:
            print url

    def transfer_url(self):
        self.feed_urls = self.feed_urls.union(self.failed_urls)


    def __urlsfromcode(self, code):
        return ["http://fund.eastmoney.com/" + code + '.html', "http://fund.eastmoney.com/f10/jbgk_" + code + '.html', "http://fund.eastmoney.com/f10/cyrjg_" + code + '.html', "http://fund.eastmoney.com/f10/tsdata_" + code + '.html', code]