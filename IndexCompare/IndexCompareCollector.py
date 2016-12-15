# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class IndexCompareCollector:

    def __init__(self):
        self.db = sqlite3.connect('test.db')
        # self.time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.db.execute('''
        create table if not exists fundinfo (
        code text not null,
        name text not null,
        target text not null,
        policy text not null
        );
        ''')

    def addFund(self, fundInfo):
        # value = u'{},{},{},{}'.format(fundInfo.code, fundInfo.full_name, fundInfo.trace_target, fundInfo.policy)
        self.db.execute('''
        insert into fundinfo (code, name, target, policy)
        values ('{0}', '{1}', '{2}', '{3}');
        '''.format(fundInfo.code, fundInfo.full_name, fundInfo.trace_target, fundInfo.policy))
        self.db.commit()

    def chooseTargets(self, targets):
        like = u""
        for (index, target) in enumerate(targets):
            if index < len(targets) - 1:
                like = like + u"like '%%{}%%' or ".format(target)
            else:
                like = like + u"like '%%{}%%'".format(target)

        result = self.db.execute('''
        select name, code from fundinfo where target {};
        '''.format(like))

        for item in result:
            print u'符合条件标的为{}, 基金代码{}'.format(item[0], item[1])

    def choosePolicys(self, policys):
        pass

    def __del__( self ):
        if self.db != None:
            self.db.close()