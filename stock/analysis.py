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

    def __init__(self, db_name=StockCollector.DATABASE_NAME):
         super(StockAnalysis, self).__init__(db_name)


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

    # 因为日期明确,所以返回也很简单,就是(pes,pbs)但也有可能当天并未开市,所以可能数据是空的
    def _query_stocks_pepb_at_date(self, stocks, date):
        pes = []
        pbs = []
        for stock in stocks:
            sql = 'SELECT {pe}, {pb} FROM {table} WHERE {date_key} = "{date}";'.format(
                pe=StockQuotation.PE_TTM_KEY, pb=StockQuotation.PB_KEY, table=StockCollector._stock_tablename(stock),date_key=StockQuotation.DATE_KEY, date=date
            )
            result = self.db.execute(sql).fetchone()
            # 我大胆预测.有一个没有数据的话,肯定都没数据
            if result == None:
                break
            pes.append(result[0])
            pbs.append(result[1])
        return (pes, pbs)

    # 同样也是明确日期范围,不需要校验,但里面到底是不是天天有就不好说了,这里的时间区间是[),返回值形如[(date, [pes], [pbs]), ]
    def _query_stocks_pepb_in_range(self, stocks, begin_date, end_date):
        results = []
        # 这个date比较麻烦了,先按照工作日一个个去尝试搜索,如果有就加上,没有就当做那天不开市
        for stock in stocks:
            sql = 'SELECT {date}, {pe}, {pb} FROM {table} WHERE {date} BETWEEN "{begin_date}" AND "{end_date}";'.format(
                date=StockQuotation.DATE_KEY, pe=StockQuotation.PE_TTM_KEY, pb=StockQuotation.PB_KEY, table=StockCollector._stock_tablename(stock), begin_date=begin_date, end_date=end_date
            )
            result = self.db.execute(sql).fetchall()
            if result != None:
                for day_quotation in result:
                    pass
        return results


if __name__ == "__main__":

    av = [1,2,3]
    print av[LAST_ELEMENT_INDEX]
    aa = (1, [1,2,3])
    print aa
    aa[1].append(4)
    print aa
    a = StockAnalysis()
    # print a._query_stocks_pepb_in_range(['600000', '601766'], '2017-01-01', '2017-01-10')
    # print '{name} is {{aa'.format(name='xixi')