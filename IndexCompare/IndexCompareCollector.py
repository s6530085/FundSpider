# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys
from IndexCompareParser import FundInfo

reload(sys)
sys.setdefaultencoding('utf-8')

class IndexCompareCollector(object):

    def __init__(self):
        self.db = sqlite3.connect('Fund.db')
        cursor = self.db.cursor()

        #数据库逐步扩展中 0.代码 1.全称 2.简称 3.类型 4.规模 5基金公司 6.经理 7.比较基准 8.追踪标的 9.范围 10.网页 11.机构持有比例 12.标准差 13.夏普比率 14.信息比例 15.跟踪误差 16.持仓 17.年化收益 18.收益排行
        cursor.execute('''
        create table if not exists {} (
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
        {} numberic not null
        );
        '''.format(FundInfo.DATABASE_TABLE_NAME,\
                   FundInfo.CODE_KEY,\
                   FundInfo.NAME_KEY,\
                   FundInfo.SHORTNAME_KEY,\
                   FundInfo.TYPE_KEY,\
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
                   FundInfo.ANNUALRANK_KEY))
        cursor.execute('''
        CREATE UNIQUE INDEX if not exists fund_code on {} ({});
        '''.format(FundInfo.DATABASE_TABLE_NAME, FundInfo.CODE_KEY))

    def addFund(self, fundInfo):
        #insert or replace 是sqlite特有的,以后如果升级sql需要注意这里
        sql = "insert or replace into fundinfo ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}) "\
        .format(FundInfo.CODE_KEY,\
                FundInfo.NAME_KEY,\
                FundInfo.SHORTNAME_KEY,\
                FundInfo.TYPE_KEY,\
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
                FundInfo.ANNUALRANK_KEY)
        sql += "values ('{0}', '{1}', '{2}', '{3}', {4}, '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', {11}, {12}, {13}, {14}, {15}, '{16}', {17}, {18});"\
        .format(fundInfo.code, fundInfo.name, fundInfo.shortname, fundInfo.type, fundInfo.size, fundInfo.company, u','.join(fundInfo.manager), fundInfo.compare, fundInfo.track, fundInfo.limits, fundInfo.url, fundInfo.inratio, fundInfo.std, fundInfo.sharperatio, fundInfo.inforatio, fundInfo.bias, u",".join(fundInfo.stocks), fundInfo.annualyield, fundInfo.annualrank)
        self.db.cursor().execute(sql)
        self.db.commit()

    def __del__( self ):
        if self.db != None:
            self.db.close()


if __name__ == "__main__":
    a = '"aaa"bbb\'ccc\''
    print a.replace("'", '-').replace('"', "-")

    # db = sqlite3.connect('fuckyou.db')
    # cursor = db.cursor()
    # cursor.execute('''
    # create table if not exists hehe (
    # xixi text not null,
    # haha text not null
    # );''')
    # sql =  'insert into hehe (xixi, haha) values (\'\'\'zzza\'\'\', \"def\");'
    # cursor.execute(sql)
    # db.commit()
    # a = "abc'''def'''"
    # print a