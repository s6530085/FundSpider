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
        for item in result:
            print item

    def __del__( self ):
        if self.db != None:
            self.db.close()


if __name__ == "__main__":
    # a = IndexCompareAnalysis()
    # a.chooseTargets([u"医", u"药"])
    # a.queryfund(u"001550")
    t = FundInfo()
    print t