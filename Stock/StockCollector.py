# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys
import datetime
from StockParser import StockInfo
reload(sys)
sys.setdefaultencoding('utf-8')

class StockCollector(object):

    DB_NAME = 'Stock.db'
    MAIN_TABLE_NAME = 'stock_list'
    #A股的最早上市时间,没有记录的统统按这个算
    STOCK_BEGIN_DATE = '1990-12-19'

    #因为不定,所以表名为stock_#code#
    def _stock_tablename(self, code):
        return 'stock_' + code

    def _create_stock_table(self, code):
        sql = '''
        '''.format()
        self.db.execute(sql)


    def __init__(self):
        self.db = sqlite3.connect(StockCollector.DB_NAME)
        #stock分表,第一个是所有股票的列表,另外就是每股的每日行情了
        self._create_main_table()
        #全stock需要爬虫后才有哦

    def _create_main_table(self):
        self.db.execute('''
        CREATE TABLE IF NOT EXISTS {} (
        {} TEXT PRIMARY KEY NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} DATE NOT NULL,
        {} TEXT NOT NULL
        );
        '''.format(StockCollector.MAIN_TABLE_NAME,
                   StockInfo.CODE_KEY,
                   StockInfo.SHORT_NAME_KEY,
                   StockInfo.FULL_NAME_KEY,
                   StockInfo.USED_NAME_KEY,
                   StockInfo.MARKET_KEY,
                   StockInfo.INDUSTRY_KEY,
                   StockInfo.RELEASE_DATE_KEY,
                   StockInfo.URL_KEY)
        )
        self.db.execute('''
        CREATE UNIQUE INDEX if not exists fund_code on {} ({});
        '''.format(StockCollector.MAIN_TABLE_NAME, StockInfo.CODE_KEY))

    # def updatestockstable(self, stocks):
    #     for (code, name, url) in stocks:


    def is_stock_existsin_main(self, code):
        result = self.db.cursor().execute('select * from {} where {} = "{}"'.format(StockCollector.MAIN_TABLE_NAME, StockInfo.CODE_KEY, code)).fetchall()
        return len(result) > 0


    #某只股票的行情最后更新时间,其实理论上每个最后更新时间应该都是一样的,
    def stock_last_update_date(self, code):
        sql = 'select {} from {} order by {} desc limit 1'.format(StockInfo.RELEASE_DATE_KEY, self._stock_tablename(code), StockInfo.RELEASE_DATE_KEY)
        #也有可能没有哦,没有的话就返回最大可能的期限
        result = self.db.execute(sql).fetchall()
        if len(result) == 0:
            return (True, StockCollector.STOCK_BEGIN_DATE)
        else:
            return self._stock_really_need_update_date(result[0])

    #有些时候即使最后更新时间不是今天也不需要更新,比如最后更新到今天还没有开市或者第一个休市,目前尚未实现嘻嘻
    def _stock_really_need_update_date(self, last_update_date):
        now_day = datetime.datetime.now().strftime("%Y-%m-%d")
        if last_update_date < now_day:
            #最后一天自然是有数据的,得加一天哦
            last_date = datetime.datetime.strptime(last_update_date, "%Y-%m-%d")
            tomorrow_date = last_date + datetime.timedelta(days = 1)
            return (True, tomorrow_date.strftime('%Y-%m-%d'))
        else:
            return (False, '')

    def update_stock_info(self, stock_info):
        pass

    def update_stock_quotation(self, stock_quotation):
        pass

if __name__ == "__main__":
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print '2017-02-15' < '2017-01-15'