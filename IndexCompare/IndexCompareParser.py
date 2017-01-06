# -*- coding: utf-8 -*-
import re
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class FundInfo(object):

    DATABASE_TABLE_NAME = u'fundinfo'
    #一些我比较感兴趣的资讯参数,默认大写的是类变量,小写的是成员变量
    code = u''
    CODE_KEY = u'code'
    CODE_CHINESE_KEY = u'基金代码'

    name = u''
    NAME_KEY = u'name'
    NAME_CHINESE_KEY = u'基金全称'

    shortname = u''
    SHORTNAME_KEY = u'shortname'
    SHORTNAME_CHINESE_KEY = u'基金简称'

    type = u''
    TYPE_KEY = u'type'
    TYPE_CHINESE_KEY = u'基金类型'

    releasetime = u''
    RELEASETIME_KEY = u'releasetime'
    RELEASETIME_CHINESE_KEY = u'发行日期'

    size = u''
    SIZE_KEY = u'size'
    SIZE_CHINESE_KEY = u'资产规模'

    company = u''
    COMPANY_KEY = u"company"
    COMPANY_CHINESE_KEY = u'基金管理人'

    manager = []
    MANAGER_KEY = u'manager'
    MANAGER_CHINESE_KEY = u'基金经理人'

    compare = u''
    COMPARE_KEY = u'compare'
    COMPARE_CHINESE_KEY = u'业绩比较基准'

    track = u''
    TRACK__KEY = u'track'
    TRACK_CHINESE_KEY = u'跟踪标的'

    limits = u''
    LIMITS_KEY = u'limits'
    LIMITS_CHINESE_KEY = u'投资范围'

    tactics = u''
    TACTICS_KEY = u'tactics'
    TACTICS_CHINESE_KEY = u'投资策略'

    url = u""
    URL_KEY = u'url'
    URL_CHINESE_KEY = u'天天基金介绍页'

    #持有比例分机构,个人,内部,我主要关心非个人的持有比例,那么就是机构+内部,而1-非个人自然就是个人了 http://fund.eastmoney.com/f10/cyrjg_000478.html
    inratio = 0
    INRATIO_KEY = u'inratio'
    INRATIO_CHINESE_KEY = u'机构持有比例'

    #标准差 夏普值和信息值,因为年份可能不同,我尽可能的取最长的 http://fund.eastmoney.com/f10/tsdata_000478.html
    std = 0
    STD_KEY = u'std'
    STD_CHINESE_KEY = u'标准差'

    sharp = 0
    SHARP_KEY = u'sharp'
    SHARP_CHINESE_KEY = u'夏普值'

    info = 0

    #这个是追踪指数的偏差,理论上是越低越好,但其实追根到底我们看的是收益
    bias = 0
    BIAS_KEY = u'bias'


    #所有资讯都放在里面,键也是直接使用资讯的中文了嘻嘻
    raw_info = dict()

    def __str__(self):
        return u'{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n'.format\
            (FundInfo.CODE_KEY, self.code, FundInfo.NAME_KEY, self.name, FundInfo.SHORTNAME_KEY, self.shortname,\
             FundInfo.SIZE_KEY, self.size, FundInfo.COMPANY_KEY, self.company, FundInfo.MANAGER_KEY, u",".join(self.manager),\
             FundInfo.COMPARE_KEY, self.compare, FundInfo.TRACK_KEY, self.track,\
             FundInfo.LIMITS_KEY, self.limits, FundInfo.TACTICS_KEY, self.tactics, FundInfo.URL_KEY, self.url)

    def parse_sqlresult(self, sqlresult):
        self.code = sqlresult[0]
        self.name = sqlresult[1]
        self.shortname = sqlresult[2]
        self.size = sqlresult[3]
        self.company = sqlresult[4]
        self.manager = sqlresult[5].split(u',')
        self.compare = sqlresult[6]
        self.track = sqlresult[7]
        self.limits = sqlresult[8]
        self.tactics = sqlresult[9]
        self.url = sqlresult[10]

    #解析基础数据f10
    def parse_base(self, content):
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        ths = html.xpath('//table//th')
        tds = html.xpath('//table//td')
        for index, th in enumerate(ths):
            key = th.text.strip()
            if len(key) == 0:
                continue
            if tds[index].text == None:
                alist = tds[index].xpath('./a')
                if len(alist) > 0:
                    if alist[0].text != None:
                        value = alist[0].text.strip()
                    else:
                        value = u""
                else:
                    #这里有些比如最高申购费什么的
                    spans = tds[index].xpath('./span')
                    if len(spans) > 0:
                        if spans[len(spans)-1].text != None:
                            value = spans[len(spans)-1].text.strip()
                        else:
                            value = u""
                    else:
                        value = u""
            else:
                value = tds[index].text.strip()
            self.raw_info[key] = value

            if key == FundInfo.CODE_KEY:
                #code也分前后端等,懒得管了,就取第一个
                value = value[:6]
                self.code = value
                self.raw_info[key] = value
            elif key == FundInfo.SHORTNAME_CHINESE_KEY:
                self.short_name = value
            elif key == FundInfo.NAME_CHINESE_KEY:
                self.full_name = value
            elif key == FundInfo.TYPE_KEY:
                self.type = value
            elif key == FundInfo.RELEASETIME_CHINESE_KEY:
                self.releasetime = value
            #去掉后面单位和描述只保留数字
            elif key == FundInfo.SIZE_KEY:
                #某些基金新开或者其他原因没有规模
                if len(value.split(u'亿')) > 0:
                    value = value.split(u'亿')[0]
                self.size = value
                self.raw_info[key] = value
            #这里是个超链接
            elif key == FundInfo.COMPANY_CHINESE_KEY:
                self.company = value
            elif key == FundInfo.MANAGER_CHINESE_KEY:
                value = []
                #特别处理下基金经理这块,因为可能是多人,其实还可能有重名的情况,不过暂且相信一个基金公司下的基金经理不会重名吧
                managers = tds[index].xpath('./a')
                for managerName in managers:
                    value.append(managerName.text.strip())
                self.raw_info[key] = value
                self.manager = value
            elif key == FundInfo.COMPARE_CHINESE_KEY:
                self.compare = value
            elif key == FundInfo.TRACK_CHINESE_KEY:
                self.track = value

        #然后是几个大的
        divs = html.xpath(u'//div[@class="boxitem w790"]//h4//label[@class="left" and text() != "基金分级信息"]')
        ps = html.xpath('//div[@class="boxitem w790"]//p')
        for (index, div) in enumerate(divs):
            key = div.text.strip()
            value = ps[index].text.strip()
            self.raw_info[key] = value
            if key == FundInfo.TACTICS_CHINESE_KEY:
                self.tactics = value
            elif key == FundInfo.LIMITS_CHINESE_KEY:
                self.limits = value

    #解析持有人结构,优先选择机构持有比例高的
    def parse_ratio(self, content):
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))



    #解析标准差夏普率等,当然可能是没有的
    def parse_statistic(self, content):
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))

class IndexCompareParser(object):

    #解析首页主要是获取每个基金的一些基础信息,如基金名,id
    def parse_home(self, home_content):
        if home_content is None:
            return None
        home_content = home_content.decode('gbk')
        html = etree.HTML(home_content, parser=etree.HTMLParser(encoding='utf-8'))
        alinks = html.xpath('//a[@href]')

        pattern_capture = re.compile(ur"（(\d{6})）(.+)")
        l = []
        for alink in alinks:
            aa = alink.text
            if aa != None:
                match = pattern_capture.match(aa)
                if match:
                    l.append((match.group(1), match.group(2)))

        return l

    #这里是解析每个基金的详情了,获得的东西很多,反正都在dict里,键可能会逐步增加,根据未来需要分析的东西扩展
    def parse_fund(self, basecontent, ratiocontent, statisticcontent, fundurl):
        fund_info = FundInfo()
        fund_info.parse_base(basecontent)
        fund_info.parse_ratio(ratiocontent)
        fund_info.parse_statistic(statisticcontent)
        fund_info.url = fundurl
        return fund_info

if __name__ == "__main__":
    s1 = set()
    s1.add(1)
    s1.add(2)
    s2 = set()
    s2.add(3)
    s2.add(4)
    s3 = s1.union(s2)
    print s3