# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sqlite3
import sys
import datetime
import xlrd
import os
from entity import StockInfo, StockQuotation
from spider_base.convenient import safetofloat
reload(sys)
sys.setdefaultencoding('utf-8')

class StockCollector(object):

    DATABASE_NAME = 'Stock.db'
    MAIN_TABLE_NAME = 'stock_list'
    #A股的最早上市时间,没有记录的统统按这个算
    STOCK_BEGIN_DATE = '1990-12-19'

    #因为不定,所以表名为stock_#code#
    @classmethod
    def _stock_tablename(cls, code):
        return 'stock_' + code

    def _create_stock_quotation_table(self, code):
        sql ='''
        CREATE TABLE IF NOT EXISTS {} (
        {} DATE PRIMARY KEY NOT NULL,
        {} NUMBERIC NOT NULL,
        {} NUMBERIC NOT NULL
        );
        '''.format(
            StockCollector._stock_tablename(code),
            StockQuotation.DATE_KEY,
            StockQuotation.PE_TTM_KEY,
            StockQuotation.PB_KEY
        )
        self.db.execute(sql)
        self.db.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS fund_code ON {} ({});
        '''.format(StockCollector._stock_tablename(code), StockQuotation.DATE_KEY))


    def __init__(self):
        self.db = sqlite3.connect(StockCollector.DATABASE_NAME)
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
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL
        );
        '''.format(StockCollector.MAIN_TABLE_NAME,
                   StockInfo.CODE_KEY,
                   StockInfo.SHORT_NAME_KEY,
                   StockInfo.FULL_NAME_KEY,
                   StockInfo.USED_NAME_KEY,
                   StockInfo.MARKET_KEY,
                   StockInfo.INDUSTRY_KEY,
                   StockInfo.AREA_KEY,
                   StockInfo.RELEASE_DATE_KEY,
                   StockInfo.URL_KEY)
        )
        self.db.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS fund_code ON {} ({});
        '''.format(StockCollector.MAIN_TABLE_NAME, StockInfo.CODE_KEY))


    def is_stock_exists_in_main(self, code):
        result = self.db.cursor().execute('select * from {} where {} = "{}"'.format(
            StockCollector.MAIN_TABLE_NAME, StockInfo.CODE_KEY, code)).fetchall()
        return len(result) > 0

    #该股票是否需要更新今日行情
    def is_stock_need_update_quotation(self, code):
        #逻辑稍显复杂,首先如果今日已经更新过了,自然是不需要重复更新的
        (_, last_date) = self.stock_last_update_date(code)
        if last_date >= datetime.datetime.now().strftime("%Y-%m-%d"):
            return False
        #其他的可能性太多了,比如碰巧遇到休市的日子,这没法控制,还有就是今天是周六,但是周五忘记获取了,其实也是可以拿的,所以手动简化下
        #只要不是今天已经获取过了,就强行再获取一次
        return True
        # weekday = datetime.now().weekday()
        # if weekday == 5 or weekday == 6:
        #     return False



    #某只股票的行情最后更新时间,其实理论上每个最后更新时间应该都是一样的,
    def stock_last_update_date(self, code):
        sql = 'SELECT {} FROM {} ORDER BY {} DESC LIMIT 1'.format(StockQuotation.DATE_KEY, StockCollector._stock_tablename(code), StockQuotation.DATE_KEY)
        #也有可能没有哦,没有的话就返回最大可能的期限
        result = self.db.execute(sql).fetchall()
        if len(result) == 0:
            #如果没有的话,应该再去搜索一下基础数据表,获得其上市日期最好,当然其实这无所谓啦
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
        sql = u'INSERT OR REPLACE INTO {0} ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}) '.format(
            StockCollector.MAIN_TABLE_NAME,
            StockInfo.CODE_KEY,
            StockInfo.SHORT_NAME_KEY,
            StockInfo.FULL_NAME_KEY,
            StockInfo.USED_NAME_KEY,
            StockInfo.MARKET_KEY,
            StockInfo.INDUSTRY_KEY,
            StockInfo.AREA_KEY,
            StockInfo.RELEASE_DATE_KEY,
            StockInfo.URL_KEY)
        sql += u'VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}");'.format(
            stock_info.code,
            stock_info.shortname,
            stock_info.fullname,
            u','.join(stock_info.used_names),
            stock_info.market,
            stock_info.industry,
            stock_info.area,
            stock_info.releasedate,
            stock_info.url
        )
        self.db.execute(sql)
        self.db.commit()

        #建立了这个条目之后,就应该建立对应的表了,当然可能已经创建过了
        self._create_stock_quotation_table(stock_info.code)

    def _update_stock_history_quotation(self, code, date, pe, pb):
        sql = u'INSERT OR REPLACE INTO {0} ({1}, {2}, {3}) '.format(
            StockCollector._stock_tablename(code),
            StockQuotation.DATE_KEY,
            StockQuotation.PE_TTM_KEY,
            StockQuotation.PB_KEY
        )
        sql += u'VALUES ("{0}", {1}, {2});'.format(
            date,
            pe,
            pb
        )

        self.db.execute(sql)
        self.db.commit()

    #批量操作,差不多一个表批量一次吧,算是始终的程度
    def _batch_update_stock_history_quotation(self, quotations):
        for key in quotations.keys():
            sql = u'INSERT OR REPLACE INTO {} VALUES (?, ?, ?);'.format(StockCollector._stock_tablename(key))
            self.db.cursor().executemany(sql, quotations[key])
            self.db.commit()


    #加载历史的行情,从excel中加载,按照现有excel的结构,要读取一个股票的历史数据就得翻遍整个excel文件,但目前也没有太好的处理方法
    #后来因为这个读取太好资源,改为一次性加载完毕得了,反复打开实在受不了
    def load_stock_history_quotation(self, stock_codes):
        #先创建个股的表哦
        for stock_code in stock_codes:
            self._create_stock_quotation_table(stock_code)

        history_files = []
        for root, _, files in os.walk('./stock_history/'):
            for f in files:
                if f.startswith(u'历史行情'):
                    history_files.append(root + f)
        #最好反序一下,不然日期也是倒的
        history_files.reverse()
        for history_file in history_files:
            excel = xlrd.open_workbook(history_file)
            #现在都是单表哦
            sheet = excel.sheets()[0]
            # codes_line = sheet.row_values(2)
            #也不过分批量,一个表做一次数据插入,怕太少会太卡,太多会崩溃
            quotations = dict()
            for col in range(1, sheet.ncols, 2):
                code = sheet.cell(1, col).value.split('.')[0]
                #有可能东方财富和choice的code不一致
                ss = []
                if code in stock_codes:
                    #我为什么要反过来插?因为有些数据可能是1号,2号还没有,3号有了,此时我必须一个个读下去,读到有位置,太浪费资源了,但如果
                    #我反过来读,最新的一天都没有,当然全都没有啦,而且日期是date型数据,排序什么的无所谓
                    for row in range(sheet.nrows-3, 3, -1):
                        #如果没有数值,则不添加哦
                        date_data = sheet.cell(row, 0).value
                        if isinstance(date_data, basestring) and len(date_data) == 0:
                            break
                        pb = sheet.cell(row, col).value
                        pe = sheet.cell(row, col+1).value
                        #pb,pe如果有,那么是浮点型,此时不能用数值判断,因为完全可能不盈利,但如果没有,则是空字符串
                        #不管数据时正还是负,是否过于夸张比如上百倍的市盈率,都先存起来,到底怎么处理由output确定
                        if (isinstance(pb, basestring) and len(pb) == 0) or (isinstance(pe, basestring) and len(pe) == 0):
                            break
                        else:
                            date_tuple = xlrd.xldate_as_tuple(date_data, 0)
                            date = '{}-{:0>2}-{:0>2}'.format(date_tuple[0], date_tuple[1], date_tuple[2])
                            ss.append((date, safetofloat(pe), safetofloat(pb)))
                else:
                    print 'code ' + code + " not in eastmoney"
                if len(ss) > 0:
                    quotations[code] = ss
            self._batch_update_stock_history_quotation(quotations)
            print 'load history file finish ' + history_file


    #更新当天行情
    def update_stock_quotation(self, code, stock_quotation):
        self._update_stock_history_quotation(code, stock_quotation.s_date, stock_quotation.pe_ttm, stock_quotation.pb)

    def __del__( self ):
        if self.db != None:
            self.db.close()

if __name__ == "__main__":
    a = StockInfo()
    a.__setattr__()
