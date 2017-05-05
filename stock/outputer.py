# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
from spider_base.convenient import now_day, safe_mean
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

class StockOutputer(object):


    # 将原先analysis的数据转为更合适的结构,即([dates], [pes], [pbs]),如果哪天没数据就是nan,但个数一定是一一对应的
    # 因为这里已经填充好了date,而date大家都一样,所以只要一个就够了
    def _fill_quotations(self, quotations):
        begin_date = ''
        dates = []
        pes = []
        pbs = []
        for quotation in quotations:
            stock_begin_date = quotation[0][0]
            if len(begin_date) == 0 or begin_date > stock_begin_date:
                begin_date = stock_begin_date
                dates[:] = []
                for q in quotation:
                    dates.append(q[0])
            stock_pes = []
            stock_pbs = []
            # 这里确定传过来的数组只有一个元素
            for q in quotation:
                stock_pes.append(q[1][0])
                stock_pbs.append(q[2][0])
            pes.append(stock_pes)
            pbs.append(stock_pbs)
        # 最后以最长的dates来填充
        for (index, stock_pes) in enumerate(pes):
            if len(stock_pes) < len(dates):
                stock_pes = [float('nan')] * (len(dates)-len(stock_pes)) + stock_pes
                stock_pbs = [float('nan')] * (len(dates)-len(stock_pes)) + pbs[index]
                pes[index] = stock_pes
                pbs[index] = stock_pbs
        return (dates, pes, pbs)

    # 用于输出不定数量的个股历史pe,pb对比,建议不要超过两个,不然看起来很别扭,而且不做数据处理
    # 此数据只可远观不可亵玩,毕竟个股的数据变化实在是太大了,还有就是没法区分借壳啊等特殊情况,还是需要自己甄别
    # 感觉懒得看pb了,同样也的pb基本上毫无波澜,兴趣不大
    def output_stocks(self, stock_quotations, stock_names, display_mean=False, display_pb=False):
        # 两边的行情可能开始日期是不一样的哦,需要填充
        stocks_pes = stock_quotations[1]
        df = pd.DataFrame()
        dates = stock_quotations[0]
        for (index, stock_pes) in enumerate(stocks_pes):
            df[stock_names[index]+'PE'] = pd.Series(stock_pes, dates)
            # 尝试画一下均线
            if display_mean:
                df[stock_names[index]+'PE均值'] = pd.Series([safe_mean(stock_pes)]*len(stock_pes), dates)
            if display_pb:
                stock_pbs = stock_quotations[2][index]
                df[stock_names[index]+'PB'] = pd.Series(stock_pbs, dates)
                if display_mean:
                    df[stock_names[index]+'PB均值'] = pd.Series([safe_mean(stock_pbs)]*len(stock_pbs), dates)
        df.plot(figsize=(25,15))
        plt.show()


if __name__ == "__main__":
    attention_stocks = ['000651', '600276']
    from analysis import StockAnalysis
    analysis = StockAnalysis()
    stocks_quotation = []
    for stock in attention_stocks:
        quotation = analysis.query_stocks_pepb_in_range([stock], begin_date='2000-01-01')
        stocks_quotation.append(quotation)
    outputer = StockOutputer()
    outputer.output_stocks(outputer._fill_quotations(stocks_quotation), analysis.translate_codes(attention_stocks), display_mean=True)