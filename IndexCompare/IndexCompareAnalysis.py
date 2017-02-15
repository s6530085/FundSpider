# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys
import re
from IndexCompareParser import FundInfo
reload(sys)
sys.setdefaultencoding('utf-8')

#数据库的分析器,前提是数据库已经下载好了,所以先要运行main
class IndexCompareAnalysis(object):

    def __init__(self):
        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.search(item) is not None

        self.db = sqlite3.connect('Fund.db')
        #关于正则函数是看这里的 http://stackoverflow.com/questions/5365451/problem-with-regexp-python-and-sqlite
        self.db.create_function("REGEXP", 2, regexp)

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
        select * from fundinfo where {} like "%{}%"
        '''.format(colname, colvalue)
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

    def rawquery(self, sql):
        return self.db.cursor().execute(sql)

    #这个以stocks里最多出现的基金为准
    def querystocks(self, stocks,cap=10):
        all = self.db.cursor().execute('select * from fundinfo')
        results = []
        for item in all:
            f = FundInfo()
            f.parse_sqlresult(item)
            results.append(f)
        for fundinfo in results:
            fundinfo.inter = len([i for i in stocks if i in fundinfo.stocks])
            print fundinfo.inter
        results.sort(lambda x,y: y.inter-x.inter)
        return results[0:10]

    def __del__( self ):
        if self.db != None:
            self.db.close()

def printfunds(funds, simplify=True):
    print 'funds count is ' + str(len(funds))
    for fund in funds:
        if simplify:
            print fund.code, fund.name, fund.url, fund.track
        else:
            print fund


if __name__ == "__main__":
    a = IndexCompareAnalysis()
    printfunds(a.querycode('000001'), False)