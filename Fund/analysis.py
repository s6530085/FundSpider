# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from entity import FundInfo
from spider_base.analysis import *
from spider_base.convenient import *
reload(sys)
sys.setdefaultencoding('utf-8')
from collector import FundCollector
import os

#数据库的分析器,前提是数据库已经下载好了,所以先要运行main
class FundAnalysis(SBAnalysis):

    def __init__(self, db_name=FundCollector.DATABASE_NAME):
        # 有点很烦的
        # self.stock_analysis = FundAnalysis('..'+os.sep+'stock'+os.sep+StockCollector.DATABASE_NAME)
        super(FundAnalysis, self).__init__(db_name)

    #code和name都是只对相应值进行检索
    def querycode(self, code, order='', isasc=True):
        return self.querybycol(FundInfo.CODE_KEY, code, order, isasc)

    def queryname(self, name, order='', isasc=True):
        return self.querybycol(FundInfo.NAME_KEY, name, order, isasc)

    def querytrack(self, track, order='', isasc=True):
        return self.querybycol(FundInfo.TRACK_KEY, track, order, isasc)

    def querystyle(self, style, order="", isasc=True):
        return self.querybycol(FundInfo.STYLE_KEY, style, order, isasc)

    #其他方法懒得扩展了,如果想要检索
    def querybycol(self, colname, colvalue, order='', isasc=True):
        sql = '''
        select * from {} where {} like "%{}%"
        '''.format(FundCollector.DATABASE_TABLE_NAME, colname, colvalue)
        if len(order) > 0 :
            sql += ' order by {} {}'.format(order,  'asc' if isasc else 'desc')
        return self.query(sql)

    #一般从名字,追踪标的,投资范围和策略里搜索
    def querykeyword(self, keyword):
        #投资策略废话太多,什么都有,搜索其无意义
        sql = '''
        select * from fundinfo where name like "%{}%" or compare like "%{}%" or track like "%{}%" or limits like "%{}%"
        '''.format(keyword, keyword, keyword, keyword)
        return self.query(sql)

    #这个是直接写好sql传啦.理论上都是最后调这个的哦
    def query(self, sql):
        result = self.db.cursor().execute(sql)
        results = []
        for item in result:
            f = FundInfo()
            f.parse_sqlresult(item)
            results.append(f)
        return results

    # 现在增加了持股比例,所以是传递的票综合起来最多的排前面,但无法处理那种你关注两个票a,b,其中A基金有9%的a,1%的b,B基金有1%的a,10%的b
    # 他们的排名会B会在A前的,可a其实涨了10%,而b涨了2%,实际上我希望是A在前面才好,这只能要么加权重,要么自己看了
    # 传递参数和权重主要是为了套利,但是基金三个月才出一次季报,鬼知道是不是已经换股了,只能说是投资有风险了
    # weight要么不传,要传就要统一口径,建议全传整数
    def querystocks(self, stocks, weights=[], cap=10):
        all = self.db.cursor().execute('select * from fundinfo')
        results = []
        for item in all:
            f = FundInfo()
            f.parse_sqlresult(item)
            results.append(f)
        for fundinfo in results:
            fundinfo.inter = 0
            if len(fundinfo.stocks) > 1:
                for (index, stock_per) in enumerate(fundinfo.stocks):
                    stock, per = stock_per.split('-')
                    if stock in stocks:
                        # 如果没权重就当1了
                        if len(weights) > 0:
                            i = stocks.index(stock)
                            fundinfo.inter += float(per.split('%')[0]) * float(weights[i])
                        else:
                            fundinfo.inter += float(per.split('%')[0])
        results.sort(lambda x,y: int(y.inter-x.inter))
        return results[0:cap]

def _printfunds(funds, simplify=True):
    print 'funds count is ' + str(len(funds))
    for fund in funds:
        if simplify:
            print fund.code, fund.shortname, fund.url, fund.track, fund.compare
        else:
            print fund


if __name__ == "__main__":
    a = FundAnalysis()
    # printfunds(a.querykeyword('基本面'))
    # printfunds(a.queryname('景顺长城沪深300'),False)
    # for a,b in enumerate('a,b,c'):
    #     print a, b
    # printfunds(a.querystocks(['国投电力', '川投能源']))
    # printfunds(a.querycode('161227'), False)
    _printfunds(a.querykeyword('环保'))