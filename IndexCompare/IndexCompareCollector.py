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
        #数据库逐步扩展中 1.代码 2.全称 3.简称 4.规模 5.基金公司 6.经理 7.比较基准 8.追踪标题 9.范围 10.策略 11.网页 12.机构持有比例 13.标准差 14.夏普比率 15.信息比例 16.跟踪误差 17.持仓
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
        {} numberic not null,
        {} numberic not null,
        {} text not null
        );
        '''.format(FundInfo.DATABASE_TABLE_NAME,\
                   FundInfo.CODE_KEY,\
                   FundInfo.NAME_KEY,\
                   FundInfo.SHORTNAME_KEY,\
                   FundInfo.SIZE_KEY,\
                   FundInfo.COMPANY_KEY,\
                   FundInfo.MANAGER_KEY,\
                   FundInfo.COMPARE_KEY,\
                   FundInfo.TRACK_KEY,\
                   FundInfo.LIMITS_KEY,\
                   FundInfo.TACTICS_KEY,\
                   FundInfo.URL_KEY,\
                   FundInfo.INRATIO_KEY,\
                   FundInfo.STD_KEY,\
                   FundInfo.SHARPERATIO_KEY,\
                   FundInfo.INFORATIO_KEY,\
                   FundInfo.BIAS_KEY,\
                   FundInfo.STOCKS_KEY))
        cursor.execute('''
        CREATE UNIQUE INDEX if not exists fund_code on {} ({});
        '''.format(FundInfo.DATABASE_TABLE_NAME, FundInfo.CODE_KEY))

    def addFund(self, fundInfo):
        #insert or replace 是sqlite特有的,以后如果升级sql需要注意这里
        sql = "insert or replace into fundinfo ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16})"\
        .format(FundInfo.CODE_KEY,\
                FundInfo.NAME_KEY,\
                FundInfo.SHORTNAME_KEY,\
                FundInfo.SIZE_KEY,\
                FundInfo.COMPANY_KEY,\
                FundInfo.MANAGER_KEY,\
                FundInfo.COMPARE_KEY,\
                FundInfo.TRACK_KEY,\
                FundInfo.LIMITS_KEY,\
                FundInfo.TACTICS_KEY,\
                FundInfo.URL_KEY,\
                FundInfo.INRATIO_KEY,\
                FundInfo.STD_KEY,\
                FundInfo.SHARPERATIO_KEY,\
                FundInfo.INFORATIO_KEY,\
                FundInfo.BIAS_KEY,\
                FundInfo.STOCKS_KEY)
        sql + "values ('''{0}''', '''{1}''', '''{2}''', '''{3}''', '''{4}''', '''{5}''', '''{6}''', '''{7}''', '''{8}''', '''{9}''', '''{10}''', '''{11}''', '''{12}''', '''{13}''', '''{14}''', '''{15}''', '''{16}''');"\
        .format(fundInfo.code, fundInfo.name, fundInfo.shortname, fundInfo.size, fundInfo.company, u','.join(fundInfo.manager), fundInfo.compare, fundInfo.track, fundInfo.limits, fundInfo.tactics, fundInfo.url, fundInfo.inratio, fundInfo.std, fundInfo.sharperatio, fundInfo.inforatio, fundInfo.bias, u",".join(fundInfo.stocks))
        self.db.cursor().execute(sql)
        self.db.commit()

    def __del__( self ):
        if self.db != None:
            self.db.close()