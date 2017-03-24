# -*- coding: utf-8 -*-
from url_manager import *
from downloader import *
from parser import *
from collector import *
from url_manager import FundURLIndex

class FundMain(object):

    def __init__(self):
        self.url_manager = FundURLManager()
        self.html_downloader = FundDownloader()
        self.html_paser = FundParser()
        self.collector = FundCollector()

    #先定接口，再做实现，其中首页特殊处理一下,基金三个月才出一次一次季报,如果不是数据结构改了大部分时间没必要全量更新
    def crawl(self, homeurl, incremental=True):
        # 先处理首页
        home_content = self.html_downloader.download(homeurl)
        if home_content is None:
            return

        funds_info = self.html_paser.parse_home(home_content)
        if funds_info is None:
            return

        count = 0
        finished_count = [0]

        for fund_info_code in funds_info:
            # (code, name) = fund_info
            #其实name根本没用到
            #全量更新或者新的基金才下载
            if not incremental or not self.collector.fundexist(fund_info_code):
                self.url_manager.add_url(fund_info_code)
                count += 1
        # self.url_manager.add_url("004131")
        print '共需爬取基金详情 ' + str(count) + " 个"

        def inner_crawl(isretry=False):
            if isretry:
                self.url_manager.transfer_url()

            while (not self.url_manager.is_empyt() and not self.url_manager.is_overflow()):
                urls = self.url_manager.pop_url()
                fundcode = urls[FundURLIndex.CODE.value]
                try:
                    #简化一下问题,只有所有相关页面都下载完毕才算ok
                    print 'start parse ' + urls[FundURLIndex.MAIN.value]
                    basecontent = self.html_downloader.download(urls[FundURLIndex.BASE.value])
                    ratiocontent = self.html_downloader.download(urls[FundURLIndex.RATIO.value])
                    statisticcontent = self.html_downloader.download(urls[FundURLIndex.STATISTIC.value])
                    stockscontent = self.html_downloader.download(urls[FundURLIndex.STOCKS.value])
                    annualcontent = self.html_downloader.download(urls[FundURLIndex.ANNUAL.value])
                    #只要有一个失败就都重试哦,其实也有个别网页是真的不存在,但懒得管了
                    if basecontent is None or len(basecontent) == 0 or ratiocontent is None or len(ratiocontent) == 0\
                            or statisticcontent is None or len(statisticcontent) == 0 or stockscontent is None or len(stockscontent) == 0 \
                            or annualcontent is None or len(annualcontent) == 0:
                        print 'download fund ' + fundcode + ' failed'
                        self.url_manager.fail_url(fundcode)
                        continue
                    self.url_manager.finish_url(fundcode)
                    result = self.html_paser.parse_fund(basecontent, ratiocontent, statisticcontent, stockscontent, annualcontent, urls[FundURLIndex.MAIN.value])
                    self.collector.addFund(result)
                    finished_count[0] += 1
                    print 'finish parse fund ' + fundcode + " " + str(finished_count[0]) + '/' + str(count)
                except Exception as e:
                    print 'parse fund ' + fundcode + ' fail, cause ' + str(e)
                    self.url_manager.fail_url(fundcode)

        #尝试重试两次吧,因为第一时间就重试其实很可能还是出错
        inner_crawl()
        inner_crawl(True)
        inner_crawl(True)

        print 'success finish parse url sum ' + str(finished_count[0])
        print 'failed urls is'
        self.url_manager.output_faileds()


if __name__ == "__main__":
    icMain = FundMain()
    icMain.crawl('http://fund.eastmoney.com/allfund.html')
