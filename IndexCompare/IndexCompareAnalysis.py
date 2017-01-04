# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys
from IndexCompareParser import FundInfo
reload(sys)
sys.setdefaultencoding('utf-8')

#数据库的分析器,前提是数据库已经下载好了,所以先要运行main
class IndexCompareAnalysis(object):

    def __init__(self):
        self.db = sqlite3.connect('test.db')

    def chooseTargets(self, targets):
        like = u""
        for (index, target) in enumerate(targets):
            if index < len(targets) - 1:
                like = like + u"track like '%{}%' or ".format(target)
            else:
                like = like + u"track like '%{}%'".format(target)

        result = self.db.execute('''
        select name, code, url from fundinfo where {};
        '''.format(like))

        print "符合条件的标的有:"
        for item in result:
            print u'{}, 基金代码 {}, 网址 {}'.format(item[0], item[1], item[2])

    def queryfund(self, code):
        result = self.db.execute('''
        select * from fundinfo where code == '{}'
        '''.format(code))
        results = []
        for item in result:
            f = FundInfo()
            f.parse_sqlresult(item)
            results.append(f)
        return results

    #一般从名字,追踪标的,投资范围和策略里搜索
    def querykeyword(self, keyword):
        sql = '''
        select * from fundinfo where ((name like "%{}%" or compare like "%{}%" or track like "%{}%" or limits like "%{}%" or tactics like "%{}%") and size > 5.0)
        '''.format(keyword, keyword, keyword, keyword, keyword)
        print sql
        result = self.db.execute(sql)
        results = []
        for item in result:
            f = FundInfo()
            f.parse_sqlresult(item)
            results.append(f)
        return results

    def __del__( self ):
        if self.db != None:
            self.db.close()


if __name__ == "__main__":
    codeSet = set()
    a = IndexCompareAnalysis()
    for keyword in (u'医', u'药'):
        results = a.querykeyword(keyword)
        print 'total count is ' + str(len(results))
        for result in results:
            if result.code not in codeSet:
                codeSet.add(result.code)
                print result.code, result.full_name, result.url, result.size