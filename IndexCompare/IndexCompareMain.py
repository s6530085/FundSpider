# -*- coding: utf-8 -*-
import IndexCompareURLManager
import IndexCompareDownloader
import IndexCompareOutputer
import IndexCompareParser

class IndexCompareMain:
    def __init__(self):
        self.url_manager = IndexCompareURLManager()


    def craw(self, homeurl):

        #首页和详情页的解析稍有区别,
        self._url_manager.add_url(homeurl)
        while (not self._url_manager.is_empty):
            pass

if __name__ == "__main__":
    icMain = IndexCompareMain()
    icMain.craw('http://fund.eastmoney.com/allfund.html')