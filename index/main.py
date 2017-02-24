# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from collector import *
from parser import *
from downloader import *
from stock.main import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class IndexMain(object):

    def __init__(self):
        self.collector = IndexCollector()
        self.parser = IndexParser()
        self.download = IndexDownload()

    def craw(self, incremental=True):
        #先获取指数列表,指数一般不会变,所以只有全量的时候才刷
        if not incremental:
            index_list_url = 'https://www.joinquant.com/data/dict/indexData'
            index_list_content = self.download.download(index_list_url)
            if index_list_content != None and len(index_list_content) > 0:
                index_list = self.parser.parse_index_list(index_list_content)
                #当然了,如果一个都没有其实也未必影响后续,因为可能之前就有数据库的数据了
                if len(index_list_content) == 0:
                    print 'download index list fail, exit'
                    exit(0)
            indexs = self.parser.parse_index_list(index_list)
            self.collector.update_index(indexs)



if __name__ == '__main__':
    #指数是建立在个股基础上的,所以要先获取个股信息
    # sm = StockMain()
    # sm.craw(incremental=False)
    im = IndexMain()
    im.craw(False)
    # print 'aaa' + u'aaa' + u'哈哈' + '呵呵'

