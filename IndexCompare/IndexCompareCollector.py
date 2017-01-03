# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class IndexCompareCollector(object):

    def __init__(self):
        self.db = sqlite3.connect('test.db')
        self.db.execute('''
        create table if not exists fundinfo (
        code text not null,
        name text not null,
        shortname text not null,
        size numeric not null,
        company text not null,
        manager text not null,
        compare text not null,
        track text not null,
        tactics text not null,
        url text not null
        );
        ''')
        self.db.execute('''
        CREATE UNIQUE INDEX if not exists fund_code on fundinfo (code);
        ''')

    def addFund(self, fundInfo):
        #insert or replace 是sqlite特有的,以后如果升级sql需要注意这里
        self.db.execute('''
        insert or replace into fundinfo (code, name, shortname, size, company, manager, compare, track, tactics, url)
        values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}');
        '''.format(fundInfo.code, fundInfo.full_name, fundInfo.short_name, fundInfo.size, fundInfo.company, u','.join(fundInfo.manager), fundInfo.compare_target, fundInfo.track_target, fundInfo.tactics, fundInfo.url))
        self.db.commit()

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

    def choosePolicys(self, policys):
        pass

    def __del__( self ):
        if self.db != None:
            self.db.close()