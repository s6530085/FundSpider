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
        limits text not null,
        tactics text not null,
        url text not null
        );
        ''')
        self.db.execute('''
        CREATE UNIQUE INDEX if not exists fund_code on fundinfo (code);
        ''')

    def addFund(self, fundInfo):
        #insert or replace 是sqlite特有的,以后如果升级sql需要注意这里
        self.db.execute("\
        insert or replace into fundinfo (code, name, shortname, size, company, manager, compare, track, limits, tactics, url)\
        values ('''{0}''', '''{1}''', '''{2}''', '''{3}''', '''{4}''', '''{5}''', '''{6}''', '''{7}''', '''{8}''', '''{9}''', '''{10}''');\
        ".format(fundInfo.code, fundInfo.full_name, fundInfo.short_name, fundInfo.size, fundInfo.company, u','.join(fundInfo.manager), fundInfo.compare_target, fundInfo.track_target, fundInfo.limits, fundInfo.tactics, fundInfo.url))
        self.db.commit()

    def __del__( self ):
        if self.db != None:
            self.db.close()