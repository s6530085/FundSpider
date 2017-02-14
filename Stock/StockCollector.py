# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys
from StockParser import StockInfo
reload(sys)
sys.setdefaultencoding('utf-8')

class StockCollector(object):
    DB_NAME = 'Stock.db'
    MAIN_TABLE_NAME = 'stock_list'

    def _createmaintable(self):
        sql = '''
        create table if not exists {} (
        '''.format()
        self.db.execute(sql)

    #因为不定,所以表名为stock_#code#
    def _createstocktable(self, code):
        sql = '''
        '''.format()
        self.db.execute(sql)


    def __init__(self):
        self.db = sqlite3.connect(StockCollector.DB_NAME)
        #stock分表,第一个是所有股票的列表,另外就是每股的每日行情了
        self._createmaintable()
        #全stock需要爬虫后才有哦

    def _createmaintable(self):
        self.db.execute('''
        CREATE TABLE IF NOT EXIST {} (
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} DATE NOT NULL,
        {} TEXT NOT NULL
        );
        '''.format(StockCollector.MAIN_TABLE_NAME,\
                   StockInfo.CODE_KEY,\
                   StockInfo.SHORT_NAME_KEY,\
                   StockInfo.FULL_NAME_KEY,\
                   StockInfo.USED_NAME_KEY,\
                   StockInfo.MARKET_KEY,\
                   StockInfo.INDUSTRY_KEY,
                   StockInfo.RELEASE_DATE_KEY,
                   StockInfo.URL_KEY)
        )


    # def updatestockstable(self, stocks):
    #     for (code, name, url) in stocks:


    def stockexistinmain(self, code):
        result = self.db.cursor().execute('select * from {} where {} = {}'.format(StockCollector.MAIN_TABLE_NAME, StockInfo.CODE_KEY, code))
        return len(result) > 0
