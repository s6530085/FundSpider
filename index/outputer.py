# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
from spider_base.convenient import *
reload(sys)
sys.setdefaultencoding('utf-8')

from enum import Enum, unique
# 数据抹平策略:
# 0.常规:大于100的舍弃,小于0的舍弃
# 1.小于0的算0
# 2.过高的数据(暂定pe>100)抛弃
# 3.小于0的抛弃
# 默认是后两种的组合,注意1和3是不相容的,我也懒得交验
@unique
class StockDataFlatPolicy(Enum):
    RAW = 0
    ZERO_NEGATIVE = 1 << 0
    DISCARD_NEGATIVE = 1 << 1
    DISCARD_LARGE = 1 << 2
    NORMAL = (DISCARD_NEGATIVE | DISCARD_LARGE)

# 数据输出策略,不过有点尴尬的是,如果是中位数,其实就不需要抹平数据了
# 1.算数平均
# 2.中位数
@unique
class StockDataAveragePolicy(Enum):
    MEAN = 0
    MEDIAN = 1


class IndexQuotation:
    pass

# 这个输出当然是输出指数啦,放进来的都是原始数据,看输出要怎么处理
# 一般输入的形式都是
class IndexOutputer(object):

    def __init__(self):
        self.flat_policy = 0

    #对数组的数组取中位数,自然不需要什么抹平
    def _median(self, data):
        mids = []
        for one_list in data:
            one_list = sorted(one_list)
            mids.append(median(one_list))
        return mids

    # 暂时不知道什么策略,先留白吧,pe和pb可能策略也不一样,所以写了两个函数
    def _flat(self, pes, flat_policy = StockDataFlatPolicy.RAW.value):
        pes = to_container(pes)
        if flat_policy != StockDataFlatPolicy.RAW.value:
            for (index, value) in enumerate(pes):
                if flat_policy & StockDataFlatPolicy.DISCARD_NEGATIVE.value:
                    value = [i for i in value if i >= 0]
                if flat_policy & StockDataFlatPolicy.DISCARD_LARGE.value:
                    value = [i for i in value if i <= 100]
                if flat_policy & StockDataFlatPolicy.ZERO_NEGATIVE.value:
                    value = [max(i, 0) for i in value]
                pes[index] = value
        flat_pes = []
        for value in pes:
            flat_pes.append(sum(value)/len(value))
        return flat_pes

    def _flat_pb(selfself, pbs, flat_policy = StockDataFlatPolicy.RAW.value):
        pass

    # 纯粹按数据份数来百分比值,可能以后会有按年份分的
    # 数值请尽量多一些,不然我不好10%的取
    def _segment(self, data):
        sumed = sorted(data)
        length = len(sumed)
        r = range(0, 10)
        s = [sumed[int(float(length)/10*i)] for i in r]
        s.append(sumed[LAST_ELEMENT_INDEX])
        return s

    # 打印输入时间段内的估值百分比,入参还是一如analysis的结果
    # 结果大致是:
    # 数据时间段xxx天
    # 0%pe为9.2, 10%pe为10.2, 20%pe威武12, ... 100%pe为30
    # 0#pb为xx...
    def print_index_quotations(self, index_quotations, flat_policy=StockDataFlatPolicy.NORMAL.value, average_policy=StockDataAveragePolicy.MEAN.value,
                               today_pes=[], today_pbs=[]):
        index_quotations = to_container(index_quotations)
        for index_quotation in index_quotations:
            index_info = index_quotation[0]
            print index_info
            pes = []
            pbs = []
            for index_day_quotation in index_quotation[1]:
                pes.append(index_day_quotation[1])
                pbs.append(index_day_quotation[2])
            # 此时的pes和pbs是数组的数组,且未经处理
            # 请注意中位数不是指把他们加起来之后的中位数,而是每天的中位数哦
            mid_pes = self._median(pes)
            mid_pbs = self._median(pbs)
            # 再根据输出策略进行数据抹平,才好算平均数,pb就不抹平了吧
            flat_pes = self._flat(pes, flat_policy)
            flat_pbs = self._flat(pbs, StockDataFlatPolicy.RAW.value)
            mid_segmented_pes = self._segment(mid_pes)
            mid_segmented_pbs = self._segment(mid_pbs)
            flat_segmented_pes = self._segment(flat_pes)
            flat_segmented_pbs = self._segment(flat_pbs)

            print 'pe 平均数百分点位为 ' + ','.join([str(i) for i in flat_segmented_pes])
            print 'pe 中位数百分点位为 ' + ','.join([str(i) for i in mid_segmented_pes])
            print 'pb 平均数百分点位为 ' + ','.join([str(i) for i in flat_segmented_pbs])
            print 'pb 中位数百分点位为 ' + ','.join([str(i) for i in mid_segmented_pbs])
            # 最后应该再来个当天处于什么百分位比较好,就以最后一个行情为当天吧



    # 绘图形式输出,先占个位吧
    def draw_index_quotations(self, index_quotations):
        pass

    def xixi(self, s, b, c='hehe', d='zz'):
        print s, b, c, d

if __name__ == '__main__':
    a = IndexOutputer()