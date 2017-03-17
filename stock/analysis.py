# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sys
from spider_base.analysis import *
reload(sys)
sys.setdefaultencoding('utf-8')
from collector import StockCollector
from entity import StockQuotation, StockInfo
from enum import Enum, unique
@unique
#数据填充策略:
#1.没有数据时按0算还是忽略
#2.低于0的数据按0还是用原始值
#3.过高的数据是忽略还是用原始值
class StockDataPaddingPolicy(Enum):
    pass

#数据输出策略,有些是必然的我先写明,比如1号,3号有数据,但2号数据缺失,此时2号的数据就按照(1+3)/2处理
#1.统计结果是算数平均还是中位数
@unique
class StockDataOutputPolicy(Enum):
    pass

#提供个股信息,纯数据输出,可以自己用也可以指数模块用
class StockAnalysis(SBAnalysis):

    #开始结束日期是[]的范围哦,如果不写就从最久到最新
    def query_pe(self, stock_code, begin_date='', end_date='', padding_policy='', output_policy=''):
        if begin_date == '' or end_date == '':
            sql = 'SELECT MIN({}), MAX({}) FROM {};'.format(StockQuotation.DATE_KEY, StockQuotation.DATE_KEY, StockCollector._stock_tablename(stock_code))
            result = self.db.execute(sql).fetchone()
            if begin_date == '':
                begin_date = result[0]
            if end_date == '':
                end_date = result[1]

        sql = 'SELECT {} FROM {} WHERE {} BETWEEN "{}" AND "{}";'.format(
            StockQuotation.PE_TTM_KEY, StockCollector._stock_tablename(stock_code), StockQuotation.DATE_KEY, begin_date, end_date)
        result = self.db.execute(sql)
        raw_pes = result.fetchall()
        pes = []
        for raw_pe in raw_pes:
            #此时根据填充策略进行处理
            pes.append(raw_pe[0])
        return self._flat_data(pes, output_policy)

    #抹平数据
    #pb一般不抹平,极少会有极大pb或者负pb的,所以就当全是pe啦嘻嘻
    def _flat_data(self, data, policy=''):
        flatted = []
        for raw in data:
            i = 1
        return flatted



if __name__ == "__main__":
    a = StockAnalysis(StockCollector.DATABASE_NAME)
    a.query_pe('600000')