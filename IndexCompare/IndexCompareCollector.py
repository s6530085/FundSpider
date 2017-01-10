# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys
from IndexCompareParser import FundInfo

reload(sys)
sys.setdefaultencoding('utf-8')

class IndexCompareCollector(object):

    def __init__(self):
        self.db = sqlite3.connect('test.db')
        cursor = self.db.cursor()
        cursor.execute('''
        create table if not exists {} (
        {} text not null,
        {} text not null,
        {} text not null,
        {} numeric not null,
        {} text not null,
        {} text not null,
        {} text not null,
        {} text not null,
        {} text not null,
        {} text not null,
        {} text not null,
        {} numberic not null,
        {} numberic not null,
        {} numberic not null,
        {} numberic not null
        );
        '''.format(FundInfo.DATABASE_TABLE_NAME, FundInfo.CODE_KEY, FundInfo.NAME_KEY, FundInfo.SHORTNAME_KEY, FundInfo.SIZE_KEY, FundInfo.COMPANY_KEY,\
                   FundInfo.MANAGER_KEY, FundInfo.COMPARE_KEY, FundInfo.TRACK__KEY, FundInfo.LIMITS_KEY, FundInfo.TACTICS_KEY, FundInfo.URL_KEY,\
                   FundInfo.INRATIO_KEY, FundInfo.STD_KEY, FundInfo.SHARPERATIO_KEY, FundInfo.INFORATIO_KEY))
        cursor.execute('''
        CREATE UNIQUE INDEX if not exists fund_code on {} ({});
        '''.format(FundInfo.DATABASE_TABLE_NAME, FundInfo.CODE_KEY))

    def addFund(self, fundInfo):
        #insert or replace 是sqlite特有的,以后如果升级sql需要注意这里
        self.db.cursor().execute("\
        insert or replace into fundinfo (code, name, shortname, size, company, manager, compare, track, limits, tactics, url)\
        values ('''{0}''', '''{1}''', '''{2}''', '''{3}''', '''{4}''', '''{5}''', '''{6}''', '''{7}''', '''{8}''', '''{9}''', '''{10}''');\
        ".format(FundInfo.DATABASE_TABLE_NAME, FundInfo.CODE_KEY, FundInfo.NAME_KEY, FundInfo.SHORTNAME_KEY, FundInfo.SIZE_KEY, FundInfo.COMPANY_KEY,\
                   FundInfo.MANAGER_KEY, FundInfo.COMPARE_KEY, FundInfo.TRACK__KEY, FundInfo.LIMITS_KEY, FundInfo.TACTICS_KEY, FundInfo.URL_KEY,\
                   FundInfo.INRATIO_KEY, FundInfo.STD_KEY, FundInfo.SHARPERATIO_KEY, FundInfo.INFORATIO_KEY

            fundInfo.code, fundInfo.name, fundInfo.shortname, fundInfo.size, fundInfo.company, u','.join(fundInfo.manager), fundInfo.compare, fundInfo.track, fundInfo.limits, fundInfo.tactics, fundInfo.url))
        self.db.commit()

    def __del__( self ):
        if self.db != None:
            self.db.close()