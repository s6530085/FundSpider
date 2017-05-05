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

# 这个是主叫方,就不传path了嘻嘻
class IndexMain(object):

    def __init__(self):
        self.collector = IndexCollector()
        self.parser = IndexParser()
        self.downloader = IndexDownloader()
        self.analysis = IndexAnalysis()
        self.outputer = IndexOutputer()

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
    def output_standard_index(self):
        # 标准输出就只打那些我关注的指数啦
        # 后来发现所有关注的指数一下子输出实在有点看不清,就分宽基和宅基分别输出了
        # self.outputer.standard_output(self.analysis.query_indexs(IndexCollector.ATTENTION_BROAD_INDEXS, IndexCollector.ATTENTION_BROAD_INDEXS_BEGIN_DATE), IndexCollector.ATTENTION_BROAD_INDEXS_BEGIN_DATE)
        # self.outputer.standard_output(self.analysis.query_indexs(IndexCollector.ATTENTION_SECTION_INDEXS, IndexCollector.ATTENTION_SECTION_INDEXS_BEGIN_DATE), IndexCollector.ATTENTION_SECTION_INDEXS_BEGIN_DATE, True)
        self.outputer.standard_output(self.analysis.query_indexs(IndexCollector.TEST_ATTENTION_INDEXS, IndexCollector.TEST_INDEXS_BEGIN_DATE), IndexCollector.TEST_INDEXS_BEGIN_DATE, True)

if __name__ == '__main__':
    # 指数是建立在个股基础上的,所以要先获取个股信息
    # stock_incremental = True
    # sm = StockMain('..'+os.sep+'stock'+os.sep)
    # sm.crawl(stock_incremental)

    # index_incremental = False
    im = IndexMain()
    # im.crawl(index_incremental)

    im.output_standard_index()
