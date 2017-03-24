# -*- coding: utf-8 -*-
__author__ = 'study_sun'

from spider_base.analysis import *
from spider_base.convenient import *
import sys
from stock.analysis import *
from collector import *
from spider_base.convenient import now_day
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

#这里主要还是输出纯数据,图表交由output搞定
class IndexAnalysis(SBAnalysis):

    def __init__(self, db_name=IndexCollector.DATABASE_NAME):
        self.stock_analysis = StockAnalysis()
        super(IndexAnalysis, self).__init__(db_name)

    # 虽然指数有启用日期,但是数据未必可以,所以获得的是实际有数据的起始日
    def _index_begin_date(self, index):
        result = self.db.execute('SELECT MIN({}) FROM {};'.format(IndexConstituent.DATE_KEY, IndexCollector._constituent_tablename(index))).fetchone()[0]
        return result

    # 明确要某一天某指数的成分股,不过如果当天没有成立指数那只能没有了
    def query_index_constituents_at_date(self, index, date=''):
        # 如果没写就取当天的
        if date == '':
            date = now_day()
        sql = 'SELECT {date}, {constituents} FROM {table} WHERE {date} = (SELECT MAX({date}) FROM {table} WHERE {date} <= "{input_date}");'.format(
            date=IndexConstituent.DATE_KEY, constituents=IndexConstituent.CONSTITUENTS_KEY, table=IndexCollector._constituent_tablename(index), input_date=date)
        result = self.db.execute(sql).fetchone()
        return result

    # 获取一段时间内指数的成分股,这里有些疑问,首先是时间未必能全包含,比如请求的时间指数尚未开始,另外就是不可能返回每天的数据
    # 所以返回的数据和成分股变化,当然如果你非要,我也可以给你返回每天的数据,不过begin不能超过起始日就是了
    def query_index_constituents_in_range(self, index, begin_date='', end_date=''):
        index_begin_date = self._index_begin_date(index)
        if begin_date < index_begin_date:
            begin_date = index_begin_date
        if end_date == '':
            end_date = now_day()
        sql = 'SELECT {date}, {constituents} FROM {table} WHERE {date} >= "{begin_date}" AND {date} <= "{end_date}";'.format(
            date=IndexConstituent.DATE_KEY, constituents=IndexConstituent.CONSTITUENTS_KEY, begin_date=begin_date, end_date=end_date)
        result = self.db.execute(sql).fetchall()
        return result

    # 一般的对外使用接口,展示指数(一般是多个,比较方便对比)在指定日期内的估值走势和区间
    # 最后返回的数据格式是[(指数信息, [指数成分股估值]),]
    def query_indexs(self, indexs, begin_date='', end_date='', padding_policy=''):
        indexs_info = self.query_indexs_info(indexs)
        result = []
        for index_info in indexs_info:
            # 先获取指数的成分股哦
            constituents = self.query_index_constituents_in_range(index_info.code, begin_date, end_date)
            for constituent in constituents:
                # 本身获取股票的历史行情是不一定要填起始日期的,但用于指数分析时成分股的begin_date不应超过指数的启用日期,不然无意义
                # 懒得考虑结束时间比开始早或者结束时间比指数启动还早的情况了哦
                real_begin_date = max(begin_date, index_info.begin_date)
                if real_begin_date < end_date:
                    result.append((index_info, []))
                    continue
                # 一个指数里的所有成分股都是等权的,当然说实话我也没有权重可以用撒
                constituents_info = self.stock_analysis.query_pepb(constituent.code, real_begin_date, end_date)

            pes = a.query_pe()
        return result

    #通过代码查,返回IndexInfo形式数组
    def query_indexs_info(self, indexs):
        # 注意这里的sql
        sql = 'SELECT * FROM {table} WHERE {code} IN ({code_list});'.format(
            table=IndexCollector.DATABASE_TABLE_NAME, code=IndexInfo.CODE_KEY, code_list=', '.join('?' for _ in indexs))
        result = self.db.execute(sql, indexs).fetchall()
        infoes = []

        for raw_info in result:
            info = IndexInfo()
            info.parse_sqlresult(raw_info)
            infoes.append(info)
        return infoes

    def raw_query_indexs_info(self, sql):
        result = self.db.execute(sql).fetchall()
        infoes = []

        for raw_info in result:
            info = IndexInfo()
            info.parse_sqlresult(raw_info)
            infoes.append(info)
        return infoes


if __name__ == '__main__':
    a = IndexAnalysis()
    # a.query_indexs(['000016'])
    print max('', '1922-10-22')