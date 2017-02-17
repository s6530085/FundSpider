# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys
from parser import FundInfo

reload(sys)
sys.setdefaultencoding('utf-8')

class FundCollector(object):

    DATABASE_TABLE_NAME = u'fundinfo'
    DATABASE_NAME = 'Fund.db'

    def __init__(self):
        self.db = sqlite3.connect(FundCollector.DATABASE_NAME)
        cursor = self.db.cursor()

        #数据库逐步扩展中 0.代码 1.全称 2.简称 3.类型 4.成立日期 5.规模 6.基金公司 7.经理 8.比较基准 9.追踪标的 10.范围 11.网页 12.机构持有比例 13.标准差 14.夏普比率 15.信息比例 16.跟踪误差 17.持仓 18.年化收益 19.收益排行 20.投资风格 21.费用
        cursor.execute('''
        create table if not exists {} (
        {} text PRIMARY KEY not null,
        {} text not null,
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
        {} numberic not null,
        {} numberic not null,
        {} numberic not null,
        {} numberic not null,
        {} numberic not null,
        {} text not null,
        {} numberic not null,
        {} numberic not null,
        {} text not null,
        {} numberic not null
        );
        '''.format(FundCollector.DATABASE_TABLE_NAME, \
                   FundInfo.CODE_KEY, \
                   FundInfo.NAME_KEY, \
                   FundInfo.SHORTNAME_KEY, \
                   FundInfo.TYPE_KEY, \
                   FundInfo.RELEASETIME_KEY, \
                   FundInfo.SIZE_KEY, \
                   FundInfo.COMPANY_KEY, \
                   FundInfo.MANAGER_KEY, \
                   FundInfo.COMPARE_KEY, \
                   FundInfo.TRACK_KEY, \
                   FundInfo.LIMITS_KEY, \
                   FundInfo.URL_KEY, \
                   FundInfo.INRATIO_KEY, \
                   FundInfo.STD_KEY, \
                   FundInfo.SHARPERATIO_KEY, \
                   FundInfo.INFORATIO_KEY, \
                   FundInfo.BIAS_KEY, \
                   FundInfo.STOCKS_KEY, \
                   FundInfo.ANNUALYIELD_KEY, \
                   FundInfo.ANNUALRANK_KEY, \
                   FundInfo.STYLE_KEY, \
                   FundInfo.FEE_KEY \
                   ))
        cursor.execute('''
        CREATE UNIQUE INDEX if not exists fund_code on {} ({});
        '''.format(FundCollector.DATABASE_TABLE_NAME, FundInfo.CODE_KEY))

    def addFund(self, fundInfo):
        #insert or replace 是sqlite特有的,以后如果升级sql需要注意这里
        sql = "insert or replace into fundinfo ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}) "\
        .format(FundInfo.CODE_KEY,\
                FundInfo.NAME_KEY,\
                FundInfo.SHORTNAME_KEY,\
                FundInfo.TYPE_KEY,\
                FundInfo.RELEASETIME_KEY,\
                FundInfo.SIZE_KEY,\
                FundInfo.COMPANY_KEY,\
                FundInfo.MANAGER_KEY,\
                FundInfo.COMPARE_KEY,\
                FundInfo.TRACK_KEY,\
                FundInfo.LIMITS_KEY,\
                FundInfo.URL_KEY,\
                FundInfo.INRATIO_KEY,\
                FundInfo.STD_KEY,\
                FundInfo.SHARPERATIO_KEY,\
                FundInfo.INFORATIO_KEY,\
                FundInfo.BIAS_KEY,\
                FundInfo.STOCKS_KEY,\
                FundInfo.ANNUALYIELD_KEY,\
                FundInfo.ANNUALRANK_KEY,\
                FundInfo.STYLE_KEY,\
                FundInfo.FEE_KEY)
        sql += "values ('{0}', '{1}', '{2}', '{3}', '{4}', {5}, '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', {12}, {13}, {14}, {15}, {16}, '{17}', {18}, {19}, '{20}', {21});"\
        .format(fundInfo.code, fundInfo.name, fundInfo.shortname, fundInfo.type, fundInfo.releasetime, fundInfo.size,\
                fundInfo.company, u','.join(fundInfo.manager), fundInfo.compare, fundInfo.track, fundInfo.limits,\
                fundInfo.url, fundInfo.inratio, fundInfo.std, fundInfo.sharperatio, fundInfo.inforatio, fundInfo.bias,\
                u",".join(fundInfo.stocks), fundInfo.annualyield, fundInfo.annualrank, fundInfo.style, fundInfo.fee)
        self.db.cursor().execute(sql)
        self.db.commit()

    def __del__( self ):
        if self.db != None:
            self.db.close()

    def fundexist(self, code):
        sql = 'select * from {} where {} = "{}";'.format(FundCollector.DATABASE_TABLE_NAME, FundInfo.CODE_KEY, code)
        result = self.db.execute(sql).fetchall()
        return len(result) > 0


if __name__ == "__main__":
    pass