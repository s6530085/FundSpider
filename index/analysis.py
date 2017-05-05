# -*- coding: utf-8 -*-
__author__ = 'study_sun'

from stock.analysis import *
from collector import *
from spider_base.convenient import now_day
from outputer import *
from fund.analysis import *
import os

reload(sys)
sys.setdefaultencoding('utf-8')

#这里主要还是输出纯原始数据,图表交由output搞定,所以直接用的话可能会有比较夸张的数据,比如市盈率超过一万这种
class IndexAnalysis(SBAnalysis):

    def __init__(self, path='', db_name=IndexCollector.DATABASE_NAME):
        # 有点很烦的
        self.stock_analysis = StockAnalysis('..'+os.sep+'stock'+os.sep)
        self.fund_analysis = FundAnalysis('..'+os.sep+'fund'+os.sep)
        super(IndexAnalysis, self).__init__(path+db_name)

    # 虽然指数有启用日期,但是数据未必可以,所以获得的是实际有数据的起始日
    def _index_begin_date(self, index):
        result = self.db.execute('SELECT MIN({}) FROM {};'.format(IndexConstituent.DATE_KEY, IndexCollector._constituent_tablename(index))).fetchone()[0]
        return result

    # 明确要某一天某指数的成分股,不过如果当天还没有成立指数那自然也没有了
    def query_index_constituents_at_date(self, index, date=''):
        # 如果没写就取当天的
        if date == '':
            date = now_day()
        sql = 'SELECT {date}, {constituents} FROM {table} WHERE {date} = (SELECT MAX({date}) FROM {table} WHERE {date} <= "{input_date}");'.format(
            date=IndexConstituent.DATE_KEY, constituents=IndexConstituent.CONSTITUENTS_KEY, table=IndexCollector._constituent_tablename(index), input_date=date)
        result = self.db.execute(sql).fetchone()
        return result[1].split(',')

    # 获取一段时间内指数的成分股,这里有些疑问,首先是时间未必能全包含,比如请求的时间指数尚未开始,另外就是不可能返回每天的数据
    # 所以返回的数据是成分股变化,当然如果你非要,我也可以给你返回每天的数据,不过begin不能超过起始日就是了
    # 数据结构为[(change_date, constitunes), ],而包含的范围应该是begin_date<=real_begin<=real_end<=end_date
    # 最后一个需要注意的是,返回的第一条起始日期,不一定是传过来的日期
    def query_index_constituents_in_range(self, index, begin_date='', end_date=''):
        # 如果开始日期本身就比指数的启用日期还早,那么就以启用日期开始
        index_begin_date = self._index_begin_date(index)
        if begin_date < index_begin_date:
            begin_date = index_begin_date
        if end_date == '':
            end_date = now_day()
        # 实际开始时间应该要取到比开始日期小的最大的一个,然则我已经放弃使用一句sql获取
        sql = 'SELECT {date}, {constituents} FROM {table} WHERE {date} <= "{end_date}";'.format(
            date=IndexConstituent.DATE_KEY, constituents=IndexConstituent.CONSTITUENTS_KEY,table=IndexCollector._constituent_tablename(index), end_date=end_date)
        raw_results = self.db.execute(sql).fetchall()
        results = []
        last = None
        for raw_result in raw_results:
            if begin_date == raw_result[0]:
                last = None
                results.append(raw_result)
            elif begin_date < raw_result[0]:
                # 这里有个问题,就是需要加上第一次大于前的那个(如果有的话),情况很简单,假设数据库里的数据是
                # 2010-06-30, 2011-01-01, 2011-06-01 ,2012-01-01...
                # 而你的开始日期设为2011-03-01,那还得获得2011-01-01的数据哦
                if last != None:
                    # 修改为实际开始的日期
                    results.append((begin_date, last[1]))
                    last = None
                results.append(raw_result)
            else:
                last = raw_result
        # sql = 'SELECT {date}, {constituents} FROM {table} WHERE {date} >= "{begin_date}" AND {date} <= "{end_date}";'.format(
        #     date=IndexConstituent.DATE_KEY, constituents=IndexConstituent.CONSTITUENTS_KEY,table=IndexCollector._constituent_tablename(index), begin_date=begin_date, end_date=end_date)
        # result = self.db.execute(sql).fetchall()
        return results

    # 一般的对外使用接口,展示指数(一般是多个,比较方便对比)在指定日期内的估值走势和区间
    # 最后返回的数据格式是[(指数信息, [index_quotation]),],index_quotation的结构为(date, [pes], [pbs])pe,pb都是原始数据
    def query_indexs(self, indexs=IndexCollector.ATTENTION_INDEXS, begin_date='2004-01-01', end_date=''):
        indexs = to_container(indexs)
        # 虽然对外的接口都处理了这个情况,但是我接口间还是需要用到的
        if end_date == '':
            end_date = now_day()
        indexs_info = self.query_indexs_info(indexs)
        result = []
        for index_info in indexs_info:
            print 'start query index quotations ' + index_info.code + ' ' + index_info.name
            # 本身获取股票的历史行情是不一定要填起始日期的,但用于指数分析时成分股的begin_date不应超过指数的启用日期,不然无意义
            # 懒得考虑结束时间比开始早或者结束时间比指数启动还早的情况了哦
            real_begin_date = max(begin_date, index_info.begin_time)
            if real_begin_date > end_date:
                result.append((index_info, []))
                continue
            # 先获取指数的成分股哦
            constituents = self.query_index_constituents_in_range(index_info.code, begin_date, end_date)
            if len(constituents) == 0:
                result.append((index_info, []))
                continue
            index_quotation = []
            # 这里返回的是时间段+成分股,注意时间段都是成分股变化之时,包夹在开始和结束时间之内的
            for (index, constituent_info) in enumerate(constituents):
                (date, constituent_stocks) = constituent_info
                if index < len(constituents) - 1:
                    (next_date, _) = constituents[index+1]
                else:
                    next_date = end_date
                quotations = self.stock_analysis.query_stocks_pepb_in_range(constituent_stocks.split(','), date, next_date)
                index_quotation += quotations
            result.append((index_info, index_quotation))
        return result

    #通过代码查,返回IndexInfo形式数组
    def query_indexs_info(self, indexs):
        indexs = to_container(indexs)
        # 注意这里的sql
        sql = 'SELECT * FROM {table} WHERE {code} IN ({code_list});'.format(
            table=IndexCollector.DATABASE_TABLE_NAME, code=IndexInfo.CODE_KEY, code_list=', '.join('?' for _ in indexs))
        result = self.db.execute(sql, indexs).fetchall()
        infoes = ['a' for _ in indexs]
        # 其实in的搜索未必能都搜索到,但在这里应该是能保证的,所以就直接当作全有,然后按位替换,因为in的结果不是我输入的顺序
        for raw_info in result:
            info = IndexInfo()
            info.parse_sqlresult(raw_info)
            index = indexs.index(info.code)
            infoes[index] = info
        return infoes

    def raw_query_indexs_info(self, sql):
        result = self.db.execute(sql).fetchall()
        infoes = []

        for raw_info in result:
            info = IndexInfo()
            info.parse_sqlresult(raw_info)
            infoes.append(info)
        return infoes

    # 指数基金的持仓还好, 很多主题基金的持仓和其主题完全不符, 所以就有验证十大持仓是否是其主题指数的成分股
    def query_stocks_in_constituents(self, fund_codes, index_code):
        fund_codes = to_container(fund_codes)
        constituents = self.query_index_constituents_at_date(index_code, now_day())
        constituents = constituents.split(',')
        print '指数'+index_code+"成分股共"+str(len(constituents))+'只'
        for fund_code in fund_codes:
            fund_info = self.fund_analysis.querycode(fund_code)[0]
            stocks = self.stock_analysis.translate_names(fund_info.get_raw_stocks())
            contain_count= len(list((set(stocks).union(set(constituents)))^(set(stocks)^set(constituents))))
            print fund_info.shortname + str(len(stocks)) + '大持仓, ' + str(contain_count) + '在指数成分股中'

    # 看看两个指数的成分股重合度
    def query_index_intersection(self, index1, index2):
        constituents1 = self.query_index_constituents_at_date(index1, now_day())
        constituents2 = self.query_index_constituents_at_date(index2, now_day())
        intersection = list_intersection(constituents1, constituents2)
        print '指数' + index1 + '共有' + str(len(constituents1)) + '只成分股份 ' + '指数' + index2 + '共有' + str(len(constituents2)) + '只成分股份 ' + \
              '共有成分股为' + str(len(intersection)) + '只'


if __name__ == '__main__':
    a = IndexAnalysis()
    # print a.query_index_constituents_at_date('000827', now_day())
    # a.query_stocks_in_constituents(['002259'], '000827')
    # index_quotation = a.query_indexs(['000978'], '2010-01-01')
    # o = IndexOutputer()
    # o.print_index_quotations(index_quotation)
    # codes = a.query_index_constituents_at_date('000827')
    # print_container(a.stock_analysis.translate_codes(codes))
    # a.query_index_intersection('000300', '000827')