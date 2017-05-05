# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
from spider_base.convenient import *
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
from termcolor import colored

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

    DISCARD_LARGE_STANDARD = 200

    def __init__(self):
        self.flat_policy = 0

    # 暂时不知道什么策略,先留白吧,pe和pb可能策略也不一样,所以写了两个函数
    def _flat(self, pes, flat_policy = StockDataFlatPolicy.RAW.value):
        pes = to_container(pes)
        if flat_policy != StockDataFlatPolicy.RAW.value:
            for (index, value) in enumerate(pes):
                if flat_policy & StockDataFlatPolicy.DISCARD_NEGATIVE.value:
                    value = [i for i in value if i >= 0]
                if flat_policy & StockDataFlatPolicy.DISCARD_LARGE.value:
                    value = [i for i in value if i <= IndexOutputer.DISCARD_LARGE_STANDARD]
                if flat_policy & StockDataFlatPolicy.ZERO_NEGATIVE.value:
                    value = [max(i, 0) for i in value]
                pes[index] = value
        flat_pes = []
        for value in pes:
            flat_pes.append(sum(value)/len(value))
        return flat_pes

    def _flat_pb(self, pbs, flat_policy = StockDataFlatPolicy.RAW.value):
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

    # 因为打印输出和图片输出很多数据时重复的,所以干脆并到里面吧
    def standard_output(self, index_quotations, begin_date='2004-01-01', direct_show=False, flat_policy=StockDataFlatPolicy.NORMAL.value, average_policy=StockDataAveragePolicy.MEAN.value):
        index_quotations = to_container(index_quotations)
        dfs = [pd.DataFrame() for _ in range(4)]
        [df_flat_pe, df_flat_pb, df_mid_pe, df_mid_pb] = dfs
        flat_pes = []
        flat_pbs = []
        mid_pes = []
        mid_pbs = []
        begin_dates = []
        indexs_info = []
        columns = []
        # 关于日期的index,应该做两件事,一个是从最开始找出最久的开始算,一个是把其中工作日但是没开市的也去掉,这样曲线更平滑
        # 最早的遍历一下即可 工作日没开市的应该全部指数都一样,所以一次性剔除就行
        longest_dates = []
        codes = []
        for index_quotation in index_quotations:
            index_info = index_quotation[0]
            indexs_info.append(index_info)
            codes.append(index_info.code)
            index_begin_date = index_quotation[1][0][0]
            begin_dates.append(index_begin_date)
            columns.append(index_info.name)
            raw_pe = []
            raw_pb = []
            if len(longest_dates) == 0 or longest_dates[0] > index_begin_date:
                longest_dates = []
                for quotation in index_quotation[1]:
                    longest_dates.append(quotation[0])
            for index_day_quotation in index_quotation[1]:
                raw_pe.append(index_day_quotation[1])
                raw_pb.append(index_day_quotation[2])
            mid_pe = _median(raw_pe)
            mid_pb = _median(raw_pb)
            flat_pe = self._flat(raw_pe, flat_policy)
            flat_pb = self._flat(raw_pb, StockDataFlatPolicy.RAW.value)
            flat_pes.append(flat_pe)
            flat_pbs.append(flat_pb)
            mid_pes.append(mid_pe)
            mid_pbs.append(mid_pb)

        self._print_index_quotation(indexs_info, begin_dates, flat_pes, flat_pbs, mid_pes, mid_pbs)

        for index, code in enumerate(codes):
            df_flat_pe[code] = _fill_series(flat_pes[index], longest_dates)
            df_flat_pb[code] = _fill_series(flat_pbs[index], longest_dates)
            df_mid_pe[code] = _fill_series(mid_pes[index], longest_dates)
            df_mid_pb[code] = _fill_series(mid_pbs[index], longest_dates)

        for df in dfs:
            df.columns = columns
        self._draw_index_quotation(dfs, direct_show)


    # 这里默认是刷四张图,平均pe,平均pb,中值pe和中值pb
    def _draw_index_quotation(self, dfs, direct_show):
        plt.interactive(False)
        titles = [u'PE平均数', u'PB平均数', u'PE中位数', u'PB中位数']
        for index, df in enumerate(dfs):
            df.plot(figsize=(25,15),title=titles[index])
        if direct_show:
            plt.show()


    def _print_index_quotation(self, indexs_info, begin_dates, flat_pes, flat_pbs, mid_pes, mid_pbs):
        for (index, index_info) in enumerate(indexs_info):
            print ''
            print index_info
            print '实际有数据的起始计算日期为' + begin_dates[index]

            segmented_flat_pe = self._segment(flat_pes[index])
            segmented_flat_pb = self._segment(flat_pbs[index])
            segmented_mid_pe = self._segment(mid_pes[index])
            segmented_mid_pb = self._segment(mid_pbs[index])
            today_flat_pe = flat_pes[index][LAST_ELEMENT_INDEX]
            today_flat_pb = flat_pbs[index][LAST_ELEMENT_INDEX]
            today_mid_pe = mid_pes[index][LAST_ELEMENT_INDEX]
            today_mid_pb = mid_pbs[index][LAST_ELEMENT_INDEX]

            # 平均値的偏差中值的基准我想了半天,还是用平均値的平均値来,影响的,中位值的偏差中值基准也是中位值的中位值
            print 'pe平均数百分点位为 ' + _print_percent(segmented_flat_pe)

            # 对于偏差中值小于10%的都加红显示
            tip_color = 'red'
            flat_pe_offset = _in_offset(sum(flat_pes[index])/len(flat_pes[index]), today_flat_pe)
            # 但是很烦的,一旦用了colored就没有正常黑色显示,只好写这么冗余的代码
            if flat_pe_offset < 0.1:
                print colored('当天pe平均数为' + rounded_to(today_flat_pe) + ' 百分位为' + rounded_to(_in_percent(flat_pes[index], today_flat_pe)*100) + '%', tip_color),
                print colored('偏差中值为 ' + rounded_to(flat_pe_offset) + "%", tip_color)
            else :
                print '当天pe平均数为' + rounded_to(today_flat_pe) + ' 百分位为' + rounded_to(_in_percent(flat_pes[index], today_flat_pe)*100) + '%',
                print '偏差中值为 ' + rounded_to(flat_pe_offset) + "%"

            print 'pe中位数百分点位为 ' + _print_percent(segmented_mid_pe)

            mid_pe_offset = _in_offset(median(sorted(mid_pes[index])), today_mid_pe)
            if mid_pe_offset < 0.1:
                print colored('当天pe中位数为' + rounded_to(today_mid_pe) + ' 中位数百分位为' + rounded_to(_in_percent(mid_pes[index], today_mid_pe)*100) + '%', tip_color),
                print colored('偏差中值为 ' + rounded_to(mid_pe_offset) + '%', tip_color)
            else:
                print '当天pe中位数为' + rounded_to(today_mid_pe) + ' 中位数百分位为' + rounded_to(_in_percent(mid_pes[index], today_mid_pe)*100) + '%',
                print '偏差中值为 ' + rounded_to(mid_pe_offset) + '%'

            print 'pb平均数百分点位为 ' + _print_percent(segmented_flat_pb)

            flat_pb_offset = _in_offset(sum(flat_pbs[index])/len(flat_pbs[index]), today_flat_pb)
            if flat_pb_offset < 0.1:
                print colored('当天pb平均数为' + rounded_to(today_flat_pb) + ' 平均数百分位为' + rounded_to(_in_percent(flat_pbs[index], today_flat_pb)*100) + '%', tip_color),
                print colored('偏差中值为 ' + rounded_to(flat_pb_offset) + '%', tip_color)
            else:
                print '当天pb平均数为' + rounded_to(today_flat_pb) + ' 平均数百分位为' + rounded_to(_in_percent(flat_pbs[index], today_flat_pb)*100) + '%',
                print '偏差中值为 ' + rounded_to(flat_pb_offset) + '%'

            print 'pb中位数百分点位为 ' + _print_percent(segmented_mid_pb)

            mid_pb_offset = median(sorted(mid_pbs[index]))
            if mid_pb_offset < 0.1:
                print colored('当天pb中位数为' + rounded_to(today_mid_pb) + ' 中位数百分位为' + rounded_to(_in_percent(mid_pbs[index], today_mid_pb)*100) + '%', tip_color),
                print colored('偏差中值为' + rounded_to(mid_pb_offset) + '%', tip_color)
            else:
                print '当天pb中位数为' + rounded_to(today_mid_pb) + ' 中位数百分位为' + rounded_to(_in_percent(mid_pbs[index], today_mid_pb)*100) + '%',
                print '偏差中值为' + rounded_to(mid_pb_offset) + '%'
            print ''


# 单条数据在整体数据里的百分比
def _in_percent(l, i):
    sl = sorted(l)
    return sl.index(i) / float(len(sl))


# 两个数据的偏差,前一个参数为基准
def _in_offset(s, i):
    return (i-s)/s*100

def _print_percent(l):
    return ', '.join([str(i*10) + '% : ' + str(l[i]) for i in range(len(l))])

# 因为DataFrame的特殊性,不得不把一个序列的日期里所有数据都填上,没有数据的用nan填充
def _fill_series(raw_list, all_dates):
    s = []
    diff = len(all_dates) - len(raw_list)
    for d in range(diff):
        s.append(float('nan'))
    s += raw_list
    return pd.Series(s, all_dates)

#对数组的数组取中位数,自然不需要什么抹平
def _median(data):
    mids = []
    for one_list in data:
        one_list = sorted(one_list)
        mids.append(median(one_list))
    return mids

if __name__ == '__main__':
    print '34.2' > '34.21'
    print '34.0' > '34'
    print '34.2' > '33.9'