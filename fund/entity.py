# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from spider_base.entity import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class FundInfo(SBObject):

    #一些我比较感兴趣的资讯参数,默认大写的是类变量,小写的是成员变量
    CODE_KEY = u'code'
    CODE_CHINESE_KEY = u'基金代码'

    NAME_KEY = u'name'
    NAME_CHINESE_KEY = u'基金全称'

    SHORTNAME_KEY = u'shortname'
    SHORTNAME_CHINESE_KEY = u'基金简称'

    #股票型,债券型,有混合型,理财型,货币型,QDII,股票指数,联接基金
    TYPE_KEY = u'type'
    TYPE_CHINESE_KEY = u'基金类型'

    RELEASETIME_KEY = u'releasetime'
    RELEASETIME_CHINESE_KEY = u'成立日期'

    SIZE_KEY = u'size'
    SIZE_CHINESE_KEY = u'资产规模'

    COMPANY_KEY = u"company"
    COMPANY_CHINESE_KEY = u'基金管理人'

    MANAGER_KEY = u'manager'
    MANAGER_CHINESE_KEY = u'基金经理人'

    COMPARE_KEY = u'compare'
    COMPARE_CHINESE_KEY = u'业绩比较基准'

    TRACK_KEY = u'track'
    TRACK_CHINESE_KEY = u'跟踪标的'

    LIMITS_KEY = u'limits'
    LIMITS_CHINESE_KEY = u'投资范围'

    #不在数据库里保存投资策略了,废话太多反而搜不出有用的东西,而且数据库会极度庞大
    # TACTICS_KEY = u'tactics'
    # TACTICS_CHINESE_KEY = u'投资策略'

    URL_KEY = u'url'
    URL_CHINESE_KEY = u'天天基金介绍页'

    #持有比例分机构,个人,内部,我主要关心非个人的持有比例,那么就是机构+内部,而1-非个人自然就是个人了 http://fund.eastmoney.com/f10/cyrjg_000478.html
    INRATIO_KEY = u'inratio'
    INRATIO_CHINESE_KEY = u'机构持有比例'

    #标准差 夏普值和信息值,因为年份可能不同,我尽可能的取最长的 http://fund.eastmoney.com/f10/tsdata_000478.html
    #反映基金收益率的波动程度。标准差越小，基金的历史阶段收益越稳定。
    STD_KEY = u'std'
    STD_CHINESE_KEY = u'标准差'

    #反映基金承担单位风险，所能获得的超过无风险收益的超额收益。夏普比率越大，基金的历史阶段绩效表现越佳。
    SHARPERATIO_KEY = u'sharperatio'
    SHARPERATIO_CHINESE_KEY = u'夏普比率'

    #表示单位主动风险所带来的超额收益，比率高说明超额收益高。
    INFORATIO_KEY = u'inforatio'
    INFORATIO_CHINESE_KEY = u'信息比率'

    #这个是指数基金追踪指数的偏差,一般来说，跟踪误差越小，基金经理的管理能力越强,但其实追根到底我们看的是收益
    BIAS_KEY = u'bias'
    BIAS_CHINESE_KEY = u'跟踪误差'

    #十大持仓,懒得写也是和经理人一样用逗号分割了,而且如果有半年/年报的话,最多是20大持仓,有些地方又未必有十大,所以不要预设长度
    STOCKS_KEY = u'stocks'
    STOCKS_CHINESE_KEY = u'股票投资明细'

    #年度收益率,太细的没必要看,直接转化为年化收益
    ANNUALYIELD_KEY = u'annualyield'
    ANNUALYIELD_CHINESE_KEY = u'年度涨幅'

    #年度收益的同列排行,原始数据是 99|200, 2|201, 最后以算术平均值,按理说同类中越小越好,可能会有更好的统计方式,但我还没想到
    ANNUALRANK_KEY = u'annualrank'
    ANNUALRANK_CHINESE_KEY = u'同类排名'

    #风格,可能是(大盘|中盘|小盘)(价值|平衡|成长)之类的
    STYLE_KEY = u'style'
    STYLE_CHINESE_KEY = u'基金投资风格'

    #管理费用合计,没必要把四个都列出来,但麻烦的是,管理用和托管费自然是雷打不动,但是申购费特别是股票型可能打折极大,如果不用折扣后的数值很不实际,可这
    #说到底是天天基金的折扣,有可能别的地方不一样,就凑合一下吧,另外就是赎回费用,很多开始n年后不收了,也只能凑合着记录最高赎回费了
    FEE_KEY = u'fee'
    FEE_CHINESE_KEY = u'管理费率合计'
    MANAGE_FEE_CHINESE_KEY= u'管理费率'
    COSTODY_FEE_CHINESE_KEY = u'托管费率'
    BUY_FEE_CHINESE_KEY = u'最高申购费率'
    SELL_FEE_CHINESE_KEY = u'最高赎回费率'

    #资产配置,即基金的股票债券和基金的占比,而我的主要目的用于观察整个市场的热度
    STOCK_RATIO_KEY = u'stockratio'
    STOCK_RATIO_CHINESE_KEY = u'股票占净比'
    BOND_RATIO_KEY = u'bondratio'
    BOND_RATIO_CHINESE_KEY = u'债券占净比'
    CASH_RATIO_KEY = u'cashratio'
    CASH_RATIO_CHINESE_KEY = u'现金占净比'

    @classmethod
    def all_keys(cls):
        return [FundInfo.CODE_KEY, FundInfo.NAME_KEY, FundInfo.SHORTNAME_KEY, FundInfo.TYPE_KEY, FundInfo.RELEASETIME_KEY,
                FundInfo.SIZE_KEY, FundInfo.COMPANY_KEY, FundInfo.MANAGER_KEY, FundInfo.COMPARE_KEY, FundInfo.TRACK_KEY,
                FundInfo.URL_KEY, FundInfo.INRATIO_KEY, FundInfo.STD_KEY, FundInfo.SHARPERATIO_KEY, FundInfo.INFORATIO_KEY,
                FundInfo.BIAS_KEY, FundInfo.STOCKS_KEY, FundInfo.ANNUALYIELD_KEY, FundInfo.ANNUALRANK_KEY, FundInfo.STYLE_KEY,
                FundInfo.FEE_KEY, FundInfo.STOCK_RATIO_KEY, FundInfo.BOND_RATIO_KEY, FundInfo.CASH_RATIO_KEY]

    @classmethod
    def all_desc_keys(cls):
        return [FundInfo.CODE_CHINESE_KEY, FundInfo.NAME_CHINESE_KEY, FundInfo.SHORTNAME_CHINESE_KEY, FundInfo.TYPE_CHINESE_KEY,
                FundInfo.RELEASETIME_CHINESE_KEY, FundInfo.SIZE_CHINESE_KEY, FundInfo.COMPANY_CHINESE_KEY, FundInfo.MANAGER_CHINESE_KEY,
                FundInfo.COMPARE_CHINESE_KEY, FundInfo.TRACK_CHINESE_KEY, FundInfo.URL_CHINESE_KEY, FundInfo.INRATIO_CHINESE_KEY,
                FundInfo.STD_CHINESE_KEY, FundInfo.SHARPERATIO_CHINESE_KEY, FundInfo.INFORATIO_CHINESE_KEY, FundInfo.BIAS_CHINESE_KEY,
                FundInfo.STOCKS_CHINESE_KEY, FundInfo.ANNUALYIELD_CHINESE_KEY, FundInfo.ANNUALRANK_CHINESE_KEY,
                FundInfo.STYLE_CHINESE_KEY, FundInfo.FEE_CHINESE_KEY, FundInfo.STOCK_RATIO_CHINESE_KEY, FundInfo.BOND_RATIO_CHINESE_KEY, FundInfo.CASH_RATIO_CHINESE_KEY]

    def __init__(self):
        self.code = u''
        self.name = u''
        self.shortname = u''
        self.type = u''
        self.releasetime = u''
        self.size = 0
        self.company = u''
        self.manager = []
        self.compare = u''
        self.track = u''
        self.limits = u''
        self.tactics = u''
        self.url = u''
        self.inratio = 0.0
        self.std = 0.0
        self.sharperatio = 0.0
        self.inforatio = 0.0
        self.bias = 0.0
        self.stocks = []
        self.annualyield = -1.0  # 这里用0也不一定妥当,因为可能会有负的收益,那么0反而是不亏的,所以就设置为一个负值,因为是年化,所以不可能低于-1
        self.annualrank = 1.0  # 为什么默认值为1呢,因为这个数值是越小越好,结果默认就是0的话,在排序时就可能搞的没数据的反而排最前面了
        self.style = u''
        self.fee = 0.0
        self.stockratio = 0.0
        self.bondratio = 0.0
        self.cashratio = 0.0

    #简单的就只打印编号,简称和url
    def short_desc(self):
        return u'{}: {} {}: {} {}: {} '.format(FundInfo.CODE_CHINESE_KEY, self.code, FundInfo.NAME_CHINESE_KEY, FundInfo.name, FundInfo.URL_CHINESE_KEY, FundInfo.url)


    def parse_sqlresult(self, sqlresult):
        self.code = sqlresult[0]
        self.name = sqlresult[1]
        self.shortname = sqlresult[2]
        self.type = sqlresult[3]
        self.releasetime = sqlresult[4]
        self.size = sqlresult[5]
        self.company = sqlresult[6]
        self.manager = sqlresult[7].split(u',')
        self.compare = sqlresult[8]
        self.track = sqlresult[9]
        self.limits = sqlresult[10]
        self.url = sqlresult[11]
        self.inratio = sqlresult[12]
        self.std = sqlresult[13]
        self.sharperatio = sqlresult[14]
        self.inforatio = sqlresult[15]
        self.bias = sqlresult[16]
        self.stocks = sqlresult[17].split(u',')
        self.annualyield = sqlresult[18]
        self.annualrank = sqlresult[19]
        self.style = sqlresult[20]
        self.fee = sqlresult[21]
        self.stockratio = sqlresult[22]
        self.bondratio = sqlresult[23]
        self.cashratio = sqlresult[24]

    # 现在的stocks 是 [华中科技-3.5%,]的形式,提供个纯粹名字数组的方法吧
    def get_raw_stocks(self):
        raw_stocks = []
        for stock in self.stocks:
            raw_stocks.append(stock.split('-')[0])
        return raw_stocks