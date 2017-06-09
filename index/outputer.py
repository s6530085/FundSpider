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
from collector import *


# 虽然之前想了很多抹平的算法,后来还是找了别人的实践做法,即所谓的四分法提出极端值,见https://www.lixinger.com/wiki/interquarter-calculation/
# 极大值自然会被剔除,实际上负值也会因为a股的国情而提出,故而不需要多个枚举值,要么原始值,要么就是经过四分法处理过的值,还有个好处就是pe,pb都可以共同使用了
# 因为仅可能用在这里,就不放到公共里面去了,唯一的问题是如果不能分成两组或者所谓的中间值不能正好取到的处理并未写明,当然我觉得如果数值足够多这都无所谓
def _inter_quartile(l):
    # 首先是有序的序列
    l = sort(l)
    # 将数组等量分为两组,当然如果是单数自然没办法
    front = l[:len(l)/2]
    rear = l[len(l)/2:]
    # 再取到前后的中位数
    front_median = median(front)
    rear_median = median(rear)
    diff = rear_median - front_median
    extre_low = front_median - diff * 0.5
    extre_high = rear_median + diff * 0.5
    return [i for i in l if i > extre_low and i < extre_high]

from enum import Enum, unique
# 数据抹平策略:
# 0.常规:大于DISCARD_LARGE_STANDARD的舍弃,小于0的舍弃
# 1.小于0的算0
# 2.过高的数据(暂定pe>100)抛弃
# 3.小于0的抛弃
# 默认是后两种的组合,注意1和3是不相容的,我也懒得交验
@unique
class StockDataFlatPolicy(Enum):
    RAW = 0
    QUARTER = 1

# 数据输出策略,不过有点尴尬的是,如果是中位数,其实就不需要抹平数据了
# 1.算数平均
# 2.中位数
@unique
class StockDataAveragePolicy(Enum):
    MEAN = 0
    MEDIAN = 1

# 这个输出当然是输出指数啦,放进来的都是原始数据,看输出要怎么处理
# 一般输入的形式都是
class IndexOutputer(object):

    def __init__(self):
        self.flat_policy = 0

    # 暂时不知道什么策略,先留白吧,pe和pb可能策略也不一样,所以写了两个函数
    def _flat(self, pes, flat_policy = StockDataFlatPolicy.QUARTER.value):
        pes = to_container(pes)
        if flat_policy != StockDataFlatPolicy.RAW.value:
            for (index, value) in enumerate(pes):
                flatted_value = _inter_quartile(value)
                pes[index] = flatted_value
        flat_pes = []
        for value in pes:
            flat_pes.append(sum(value)/len(value))
        return flat_pes

    # 本来我是不想对pb做操作的,因为其数值本身就比较小而且变化更小,但在一些st股上,其pb甚至能上万我也是醉了
    # def _flat_pb(self, pbs, flat_policy = StockDataFlatPolicy.RAW.value):
    #     pass

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
    def standard_output(self, index_quotations, show_mean=False, direct_show=False, flat_policy=StockDataFlatPolicy.QUARTER.value, average_policy=StockDataAveragePolicy.MEAN.value):
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
            if show_mean:
                columns.append(index_info.name+'历史均值')
            raw_pe = []
            raw_pb = []
            if len(longest_dates) == 0 or longest_dates[0] > index_begin_date:
                longest_dates = []
                for quotation in index_quotation[1]:
                    longest_dates.append(quotation[0])
            for index_day_quotation in index_quotation[1]:
                raw_pe.append(index_day_quotation[1])
                raw_pb.append(index_day_quotation[2])
            mid_pe = _list_median(raw_pe)
            mid_pb = _list_median(raw_pb)
            flat_pe = self._flat(raw_pe, flat_policy)
            flat_pb = self._flat(raw_pb, flat_policy)
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
            if show_mean:
                df_flat_pe[code+'mean'] = pd.Series([mean(flat_pes[index])]*len(longest_dates), longest_dates)
                df_flat_pb[code+'mean'] = pd.Series([mean(flat_pbs[index])]*len(longest_dates), longest_dates)
                df_mid_pe[code+'mean'] = pd.Series([mean(mid_pes[index])]*len(longest_dates), longest_dates)
                df_mid_pb[code+'mean'] = pd.Series([mean(mid_pbs[index])]*len(longest_dates), longest_dates)

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
def _list_median(data):
    mids = []
    for one_list in data:
        one_list = sorted(one_list)
        mids.append(median(one_list))
    return mids

if __name__ == '__main__':
    s0 =  [2, 1, 3, 5, 4, 6, 8, 7, 9, 25]
    s1 = [50, 100, -4, -3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] #-> [-3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    s2 = [50, 100, -40, -3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] #-> [-3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    s3 = [-50, 100, -40, -3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] #-> [-3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    s4 = [-50, 100, -40, -3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 120] #-> [-3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    s5 = [-5, 100, -40, -3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 120]# -> [-5, -3, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # print _inter_quartile(s0)
    print _inter_quartile(s1)
    print _inter_quartile(s2)
    print _inter_quartile(s3)
    print _inter_quartile(s4)
    print _inter_quartile(s5)
    # foo(1, 2,3,4,a=6,c=7,d=9)
    # df = pd.DataFrame()
    # line = [0,1,2]
    # df[1] = pd.Series([1,2,3], line)
    # df['a'] = pd.Series([2,3,4], line)
    # df[3] = pd.Series([3,4,5], line)
    # df.columns = [3,2,1]
    # df.plot()
    # plt.show()
    # print df[1].mean()