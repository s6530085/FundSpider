# -*- coding: utf-8 -*-
__author__ = 'study_sun'

from spider_base.analysis import *
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

    # 一般的对外使用接口
    def query_indexs(self, indexs, begin_date='', end_date='', padding_policy=''):
        for index in indexs:
            # 先获取指数的成分股哦
            constituents = self.query_index_constituents_in_range(index, begin_date, end_date)

            pes = a.query_pe()

    #通过代码查,返回IndexInfo形式数组
    def query_indexs_info(self, indexs):
        # 注意这里的sql
        # sql = 'SELECT * FROM {table} WHERE {code} IN ({code_list});'.format(
        #     table=IndexCollector.DATABASE_TABLE_NAME, code=IndexInfo.CODE_KEY, code_list=', '.join('?' for _ in indexs))
        # result = self.db.execute(sql, indexs).fetchall()
        result = self.db.execute('select * from indexinfo;').fetchall()
        infoes = []

        for raw_info in result:
            info = IndexInfo()
            info.parse_sqlresult(raw_info)
            infoes.append(info)
        return infoes



if __name__ == '__main__':
    a = IndexAnalysis()
    print a.query_index_constituents_at_date('000016')
    print a.query_indexs_info(['000016', '000300'])
    #
    # print '{0} {1} {1}'.format(1, 3)