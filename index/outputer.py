# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
from spider_base.convenient import *
reload(sys)
sys.setdefaultencoding('utf-8')

from enum import Enum, unique
# 数据抹平策略:
# 1.无视
# 2.小于0的按0算
# 3.小于0的抛弃
# 4.过高的数据(pe>100)抛弃
@unique
class StockDataFlatPolicy(Enum):
    pass

# 数据输出策略
# 1.算数平均
# 2.中位数
@unique
class XXX(Enum):
    pass

class IndexQuotation:
    pass

# 这个输出当然是输出指数啦,放进来的都是原始数据,看输出要怎么处理
# 一般输入的形式都是
class IndexOutputer(object):

    def __init__(self):
        self.flat_policy = 0

    # 暂时不知道什么策略,先留白吧,pe和pb可能策略也不一样,所以写了两个函数
    def _flat_pe(self, pes):
        pass

    def _flat_pb(selfself, pbs):
        pass

    # 纯粹按数据份数来百分比值,可能以后会有按年份分的
    # 数值请尽量多一些,不然我不好10%的取
    def _segment(self, data):
        sumed = []
        for one in data:
            sumed.append(sum(one)/len(one))
        sumed.sort()
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
    def print_index_quotations(self, index_quotations):
        for index_quotation in index_quotations:
            index_info = index_quotation[0]
            print index_info
            pes = []
            pbs = []
            for index_day_quotation in index_quotation[1]:
                pes.append(index_day_quotation[1])
                pbs.append(index_day_quotation[2])
            # 此时根据输出策略进行数据抹平
            self._flat_pe(pes)
            self._flat_pb(pbs)
            segmented_pes = self._segment(pes)
            segmented_pbs = self._segment(pbs)

            for (index, seg) in segmented_pes:
                pass
            print 'pe 百分点位为 ' + ','.join([str(i) for i in segmented_pes])
            print 'pb 百分点位为 ' + ','.join([str(i) for i in segmented_pbs])


if __name__ == '__main__':
    a = [1,2,3]
    print a
    print 'a is ' + a