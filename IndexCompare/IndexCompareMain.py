# -*- coding: utf-8 -*-
from IndexCompareURLManager import *
from IndexCompareDownloader import *
from IndexCompareParser import *
from IndexCompareCollector import *

class IndexCompareMain(object):

    def __init__(self):
        self.url_manager = IndexCompareURLManager()
        self.html_downloader = IndexCompareDownloader()
        self.html_paser = IndexCompareParser()
        self.collector = IndexCompareCollector()

    #先定接口，再做实现，其中首页特殊处理一下
    def craw(self, homeurl):
        # 先处理首页
        home_content = self.html_downloader.download(homeurl)
        if home_content is None:
            return

        funds_info = self.html_paser.parse_home(home_content)
        if funds_info is None:
            return

        count = 0
        finished_count = [0]

        # for fund_info in funds_info:
        #     (code, name) = fund_info
        #     #其实name根本没用到
        #     self.url_manager.add_url('http://fund.eastmoney.com/f10/jbgk_' + code + '.html')
        #     count += 1
        self.url_manager.add_url("http://fund.eastmoney.com/f10/jbgk_001317.html")
        print '共需爬取基金详情 ' + str(count) + " 个"

        def inner_craw(isretry=False):
            if isretry:
                self.url_manager.transfer_url()

            while (not self.url_manager.is_empyt() and not self.url_manager.is_overflow()):
                try:
                    url = self.url_manager.pop_url()
                    print 'start parse ' + url
                    content = self.html_downloader.download(url)
                    if content is None or len(content) == 0:
                        print 'download' + url + 'failed'
                        self.url_manager.fail_url(url)
                        continue
                    self.url_manager.finish_url(url)
                    result = self.html_paser.parse_fund(content, url)
                    self.collector.addFund(result)
                    finished_count[0] += 1
                    print 'finish parse url ' + url + " " + str(finished_count[0]) + '/' + str(count)
                except Exception as e:
                    print 'parse url ' + url + ' fail, cause ' + str(e)
                    self.url_manager.fail_url(url)

        #尝试重试两次吧,因为第一时间就重试其实很可能还是出错
        inner_craw()
        inner_craw(True)
        inner_craw(True)

        print 'success finish parse url sum ' + str(finished_count[0])
        print 'failed urls is'
        self.url_manager.output_faileds()


if __name__ == "__main__":
    icMain = IndexCompareMain()
    icMain.craw('http://fund.eastmoney.com/allfund.html')
