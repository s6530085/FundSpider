# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
import sqlite3
reload(sys)
sys.setdefaultencoding('utf-8')
from entity import IndexInfo, IndexConstituent
import os
import xlrd
from datetime import datetime
from spider_base.convenient import *

class IndexCollector(object):

    DATABASE_TABLE_NAME = 'indexinfo'
    DATABASE_NAME = 'index.db'

    # 目前比较关注的指数,会加载历史数据,不过这些指数很有意思的,指定深沪市场的除外,跨市场的都会有两个指数,分别供使用,一般000开头的是沪市的,399开头的是深市的,都有的话优先采用沪市
    # 全部存在数据库里,但未必感兴趣,因为有很多是暂时没有机会,或者指数重叠性太高,所以差不多的指数就选了数据量较大的
    # 上证50,基本面50,沪深300,中证500, 中证800, 中证1000, 中小板综, 创业板指, 中证全指, 上证综指, 深证成指 -- 这是各种宽基
    # 全指可选, 军工指数, 国证有色, 中证TMT, 中证新兴,  -- 这是暂时没什么兴趣的行业主题
    # 中证环保,  医药100, 全指消费, 全指医药, 全指金融, 全指信息, 国证食品, 中证红利, 中证养老(养老产业) -- 这是目前感兴趣的行业主题
    ALL_INDEXS = ['000016', '000925', '000300', '000905', '000906', '000852', '399101', '399006', '000985', '000001', '399001',
                  '000989', '399959', '399395', '000998', '000964',
                  '000827',  '000978', '000990', '000991', '000992', '000993', '399396', '000922', '399812']

    # 关注的宽基指数,主要是看市场热度而非真的要买这些指数
    # 上证50,沪深300,中证500, 中小板综, 创业板指, 深证成指
    ATTENTION_BROAD_INDEXS = ['000016', '000300', '000905', '399101', '399006', '399001']

    # 关注的行业或主题指数
    # 医药100, 中证养老, 中证环保, 中证红利, 全指消费
    ATTENTION_SECTOR_INDEXS = ['000978', '399812', '000827', '000922', '000990', '399396']

    ATTENTION_INDEXS = ATTENTION_BROAD_INDEXS + ATTENTION_SECTOR_INDEXS
    ATTENTION_BROAD_INDEXS_BEGIN_DATE = '2004-01-01'
    ATTENTION_SECTOR_INDEXS_BEGIN_DATE = '2011-01-01'

    TEST_ATTENTION_INDEXS = ['000905', '000978', '399006']
    TEST_INDEXS_BEGIN_DATE = '2000-01-01'

    def __init__(self):
        self.db = sqlite3.connect(IndexCollector.DATABASE_NAME)
        #指数的表大体上是一个基础表,包含所有指数的基本信息
        #然后是每个指数的成分变化表
        self._create_main_table()

    def __del__( self ):
        if self.db != None:
            self.db.close()

    def _create_main_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS {} (
        {} TEXT PRIMARY KEY NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} DATE NOT NULL,
        {} TEXT NOT NULL
        );
        '''.format(IndexCollector.DATABASE_TABLE_NAME,
                   IndexInfo.CODE_KEY,
                   IndexInfo.FULL_CODE_KEY,
                   IndexInfo.NAME_KEY,
                   IndexInfo.SHORT_NAME_KEY,
                   IndexInfo.BEGIN_TIME_KEY,
                   IndexInfo.WEAVE_KEY)
        self.db.execute(sql)
        self.db.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS index_code ON {} ({});
        '''.format(IndexCollector.DATABASE_TABLE_NAME, IndexInfo.CODE_KEY))

    @classmethod
    def _constituent_tablename(cls, index_code):
        return 'constituent_' + index_code

    def _create_constituent_table(self, index_code):
        sql = '''
        CREATE TABLE IF NOT EXISTS {} (
        {} DATE PRIMARY KEY NOT NULL,
        {} TEXT NOT NULL
        );
        '''.format(
            IndexCollector._constituent_tablename(index_code), \
            IndexConstituent.DATE_KEY, \
            IndexConstituent.CONSTITUENTS_KEY
        )
        self.db.execute(sql)
        self.db.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS constituent_date ON {} ({});
        '''.format(IndexCollector._constituent_tablename(index_code), IndexConstituent.DATE_KEY))


    # 刷新指数的基本信息,另外顺便把成分股的表也建好
    def update_indexs(self, indexs):
        for index_info in indexs:
            sql = u'INSERT OR REPLACE INTO {0} ({1}, {2}, {3}, {4}, {5}, {6}) '.format(
                IndexCollector.DATABASE_TABLE_NAME,
                IndexInfo.CODE_KEY,
                IndexInfo.FULL_CODE_KEY,
                IndexInfo.NAME_KEY,
                IndexInfo.SHORT_NAME_KEY,
                IndexInfo.BEGIN_TIME_KEY,
                IndexInfo.WEAVE_KEY
            )
            sql += u'VALUES (?, ?, ?, ?, ?, ?);'
            self.db.execute(sql, (index_info.code, index_info.full_code, index_info.name, index_info.short_name, index_info.begin_time, index_info.weave))
            self.db.commit()
            # self._create_constituent_table(index_info.code)


    #加载指数成分的历史数据,从软件导出的文档中读取
    def load_index_constituent(self):
        #我们不需要所有的指数数据,只要一些我们关注的即可,目前问题是文件名和指数不太对应,还有就是有些指数的历史数据也不是很全,先凑合着用吧
        # constituent_files = []
        for root, _, files in os.walk('./constituent_history/'):
            for f in files:
                #文件名就是追踪的指数标号
                file_name = f.split('.')[0]
                if IndexCollector.ALL_INDEXS.__contains__(file_name):
                    print 'load index change ' + file_name
                    self._load_index_constituent(root+f, file_name)

    # 指数的剔除和纳入不是同一天哦,暂时按超过10天算更迭了
    def _in_index_change_range(self, current, last):
        days = (datetime.strptime(current, STAND_DATE_FORMAT) - datetime.strptime(last, STAND_DATE_FORMAT)).days
        return days > 10

    def _load_index_constituent(self, file_path, index_code):
        self._create_constituent_table(index_code)
        excel = xlrd.open_workbook(file_path)
        sheet = excel.sheets()[0]
        current_date = ''
        current_constituent = []
        for row in range(1, sheet.nrows-6):
            # 喷了,结果这里的时间就是直接是字符串
            row_date = sheet.cell(row, 1).value
            #第1条先设置初始时间,以后每次时间不一致就算一次成分股变更
            if row == 1:
                current_date = row_date
            # 除了日期更换,当然到了最后一行也要提交以下咯
            # 很头疼,纳入和剔除不是同一天做的,经常是前一天先剔除老的,后一天再纳入新的,所以一定天数之前的变动都当作一次变动了
            # if row_date != current_date or row == sheet.nrows-7:
            if self._in_index_change_range(row_date, current_date) or row == sheet.nrows-7:
                # sql = u'INSERT OR REPLACE INTO {} ({}, {}) VALUES ({}, "{}");'.format(
                #     IndexCollector._constituent_tablename(index_code), IndexConstituent.DATE_KEY, IndexConstituent.CONSTITUENTS_KEY, current_date, ','.join(current_constituent))
                # self.db.execute(sql)
                #不要问我为什么,总之我用date型的就只能用?的形式插入,否则纯字符串会出问题
                self.db.execute(u'INSERT OR REPLACE INTO '+ IndexCollector._constituent_tablename(index_code) +' VALUES (?, ?);', (current_date, ','.join(current_constituent)))
                self.db.commit()
                current_date = row_date
            stock_code = sheet.cell(row, 2).value.split('.')[0]
            # 有个问题,就是某些指数纳入了b股,但是我的股票数据库里又没有b股的历史数据,只能目前暂时屏蔽了
            if stock_code.startswith('2'):
                continue
            operation = sheet.cell(row, 4).value
            if operation == u'纳入':
                current_constituent.append(stock_code)
            else:
                current_constituent.remove(stock_code)

    # 刷新指数的成分信息,不过现在没这个数据好气啊,可能会从东方财富那里更新
    def update_index_constituent(self):
        pass

if __name__ == '__main__':
    c = IndexCollector()
    c.load_index_constituent()