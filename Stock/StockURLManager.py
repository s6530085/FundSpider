# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from SpiderBase import SBURLManager
import sys
from SpiderBase.SBConvenient import now_day
from StockConvenient import *

reload(sys)
sys.setdefaultencoding('utf-8')

class StockURLManager(SBURLManager):

    #比较诡异一些,返回的依次是(code, 基础信息url, 介绍页url)
    def pop_url(self):
        code = self.feed_urls.pop()
        return (code, 'http://f10.eastmoney.com/f10_v2/CompanySurvey.aspx?code=' + joint_code(code, STOCK_INFO_NET),
                'http://quote.eastmoney.com/' + joint_code(code, STOCK_INFO_NET) + '.html')

    #行情url需要结合数据库,所以不能直接获得,如果是全量就获取a股开市日到今天的,如果是增量则获取起始日到今天的
    def joint_quotation_url(self, code, initdate):
        #形式是http://q.stock.sohu.com/hisHq?code=zs_000001&start=20000504&end=20151215&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp
        #code是600000sh形式的,数据库及参数里的日期都是2018-12-22形式的,注意处理为搜狐的数据形式
        initdate = initdate.replace('-', '')
        now = now_day().replace('-', '')
        return 'http://q.stock.sohu.com/hisHq?code=' + joint_code(code, STOCK_QUOTATION_NET) + '&start=' + initdate + '&end=' + now + '&stat=1&order=A&period=d&callback=historySearchHandler&rt=jsonp'


if __name__ == "__main__":
    now = now_day()
    now = now.replace('-', '')
    print now