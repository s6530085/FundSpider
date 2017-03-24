# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from spider_base.analysis import *
from spider_base.convenient import *
reload(sys)
sys.setdefaultencoding('utf-8')
from collector import StockCollector
from entity import StockQuotation, StockInfo
from enum import Enum, unique
@unique
# 数据抹平策略:
# 1.无视
# 2.小于0的按0算
# 3.小于0的抛弃
# 4.过高的数据(pe>100)抛弃
class StockDataFlatPolicy(Enum):
    pass

#数据输出策略,有些是必然的我先写明,比如1号,3号有数据,但2号数据缺失,此时2号的数据就按照(1+3)/2处理
#1.统计结果是算数平均还是中位数
@unique
class StockDataOutputPolicy(Enum):
    pass

#提供个股信息,纯数据输出,可以自己用也可以指数模块用
class StockAnalysis(SBAnalysis):

    # 查询单个股票的pe和pb,开始结束日期是[]的范围哦,如果不写就从最久到最新
    # 本来是想把处理抹平数据放函数里,输出数据放别的地方,后来发现处理数据也不能放函数里,不然中位数就不准了,故而本函数输出的都是原始数据
    def query_pepb(self, stock_code, begin_date='', end_date=''):
        if begin_date == '' or end_date == '':
            sql = 'SELECT MIN({date}), MAX({date}) FROM {table};'.format(
                date=StockQuotation.DATE_KEY, table=StockCollector._stock_tablename(stock_code))
            result = self.db.execute(sql).fetchone()
            if begin_date == '':
                begin_date = result[0]
            if end_date == '':
                end_date = result[1]

        sql = 'SELECT {}, {}, {} FROM {} WHERE {} BETWEEN "{}" AND "{}";'.format(
            StockQuotation.DATE_KEY, StockQuotation.PE_TTM_KEY, StockQuotation.PB_KEY, StockCollector._stock_tablename(stock_code), StockQuotation.DATE_KEY, begin_date, end_date)
        result = self.db.execute(sql)
        raw_results = result.fetchall()
        results = []
        for raw_result in raw_results:
            quotation = StockQuotation()
            quotation.parse_sqlresult(raw_result)
            results.append(quotation)
        return results


    # 抹平数据
    # pb一般不抹平,极少会有极大pb或者负pb的,所以就当全是pe啦嘻嘻
    def _flat_data(self, quotations, policy=''):
        pass




if __name__ == "__main__":
    a = StockAnalysis(StockCollector.DATABASE_NAME)
    print_container(a.query_pepb('600000'))