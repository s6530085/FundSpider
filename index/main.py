# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from collector import *
from parser import *
from downloader import *
from stock.main import *
from analysis import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class IndexMain(object):

    def __init__(self):
        self.collector = IndexCollector()
        self.parser = IndexParser()
        self.downloader = IndexDownloader()
        self.analysis = IndexAnalysis()

    #这个基本上不会重试放心啦
    def crawl(self, incremental=True):
        #先获取指数列表,指数一般不会变,所以只有全量的时候才刷
        if not incremental:
            index_list_url = 'https://www.joinquant.com/data/dict/indexData'
            index_list_content = self.downloader.download(index_list_url)
            if index_list_content != None and len(index_list_content) > 0:
                index_list = self.parser.parse_index_list(index_list_content)
                #当然了,如果一个都没有其实也未必影响后续,因为可能之前就有数据库的数据了
                if len(index_list_content) == 0:
                    print 'download index list fail, exit'
                    exit(0)
                self.collector.update_indexs(index_list)

            #然后开始加载指数的成分股变化,同样也是全量的时候才刷哦
            self.collector.load_index_constituent()


    #具体的分析交由具体分析,main里做的事情是输出固定的指数pepb估值百分比
    def output_standard_index(self, stock_main):
        #先来个输出医药100的嘻嘻
        indexs = ['000978']
        indexs_info = []
        for index in indexs:
            i = 1


if __name__ == '__main__':
    #指数是建立在个股基础上的,所以要先获取个股信息
    # stock_incremental = True
    # sm = StockMain()
    # sm.craw(stock_incremental)

    index_incremental = False
    im = IndexMain()
    im.crawl(index_incremental)
    # im.output_standard_index()


