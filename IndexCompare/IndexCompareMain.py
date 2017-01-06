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
        #     self.url_manager.add_url(code)
        #     count += 1
        self.url_manager.add_url("001317")
        print '共需爬取基金详情 ' + str(count) + " 个"

        def inner_craw(isretry=False):
            if isretry:
                self.url_manager.transfer_url()

            while (not self.url_manager.is_empyt() and not self.url_manager.is_overflow()):
                urls = self.url_manager.pop_url()
                fundcode = urls[IndexCompareURLManager.FUND_URL_INDEX_CODE]
                try:
                    #简化一下问题,只有所有相关页面都下载完毕才算ok
                    print 'start parse ' + urls[IndexCompareURLManager.FUND_URL_INDEX_MAIN]
                    basecontent = self.html_downloader.download(urls[IndexCompareURLManager.FUND_URL_INDEX_BASE])
                    ratiocontent = self.html_downloader.download(urls[IndexCompareURLManager.FUND_URL_INDEX_RATIO])
                    statisticcontent = self.html_downloader.download(IndexCompareURLManager.FUND_URL_INDEX_STATISTIC)
                    #只要有一个失败就都重试哦
                    if basecontent is None or len(basecontent) == 0 or ratiocontent is None or len(ratiocontent) == 0\
                            or statisticcontent is None or len(statisticcontent) == 0:
                        print 'download fund ' + fundcode + ' failed'
                        self.url_manager.fail_url(fundcode)
                        continue
                    self.url_manager.finish_url(fundcode)
                    result = self.html_paser.parse_fund(basecontent, ratiocontent, statisticcontent, urls[IndexCompareURLManager.FUND_URL_INDEX_MAIN])
                    self.collector.addFund(result)
                    finished_count[0] += 1
                    print 'finish parse fund ' + fundcode + " " + str(finished_count[0]) + '/' + str(count)
                except Exception as e:
                    print 'parse fund ' + fundcode + ' fail, cause ' + str(e)
                    self.url_manager.fail_url(fundcode)

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
