# -*- coding: utf-8 -*-
import re
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class FundInfo(object):
    #一些我比较感兴趣的资讯参数,默认大写的是类变量,小写的是成员变量
    code = u''
    CODE_KEY = u'基金代码'

    short_name = u''
    SHORT_NAME_KEY = u'基金简称'

    full_name = u''
    FULL_NAME_KEY = u'基金全称'

    type = u''
    TYPE_KEY = u'基金类型'

    release_time = u''
    RELEASE_TIME_KEY = u'发行日期'

    size = u''
    SIZE_KEY = u'资产规模'

    company = u''
    COMPANY_KEY = u'基金管理人'

    manager = []
    MANAGER_KEY = u'基金经理人'

    compare_target = u''
    COMPARE_TARGET_KEY = u'业绩比较基准'

    track_target = u''
    TRACK_TARGET_KEY = u'跟踪标的'

    limits = u''
    LIMITS_KEY = u'投资范围'

    tactics = u''
    TACTICS_KEY = u'投资策略'

    url = u""

    #所有资讯都放在里面,键也是直接使用资讯的中文了嘻嘻
    raw_info = dict()

    #由数据构造
    # def __init__(self, info=()):
    #     self.code = info[0]

    def __str__(self):
        return u'{} is {}, {} is {}, {} is {}, {} is {}, {} is {}, {} is {}, {} is {}, {} is {}, {} is {}, {} is {}'.format(FundInfo.CODE_KEY, self.code, FundInfo.FULL_NAME_KEY, self.full_name)

    def __init__(self):
        pass


    def parse_content(self, content=""):
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
            elif key == FundInfo.SHORT_NAME_KEY:
                self.short_name = value
            elif key == FundInfo.FULL_NAME_KEY:
                self.full_name = value
            elif key == FundInfo.TYPE_KEY:
                self.type = value
            elif key == FundInfo.RELEASE_TIME_KEY:
                self.release_time = value
            #去掉后面单位和描述只保留数字
            elif key == FundInfo.SIZE_KEY:
                #某些基金新开或者其他原因没有规模
                if len(value.split(u'亿')) > 0:
                    value = value.split(u'亿')[0]
                self.size = value
                self.raw_info[key] = value
            #这里是个超链接
            elif key == FundInfo.COMPANY_KEY:
                self.company = value
            elif key == FundInfo.MANAGER_KEY:
                value = []
                #特别处理下基金经理这块,因为可能是多人,其实还可能有重名的情况,不过暂且相信一个基金公司下的基金经理不会重名吧
                managers = tds[index].xpath('./a')
                for managerName in managers:
                    value.append(managerName.text.strip())
                self.raw_info[key] = value
                self.manager = value
            elif key == FundInfo.COMPARE_TARGET_KEY:
                self.compare_target = value
            elif key == FundInfo.TRACK_TARGET_KEY:
                self.track_target = value

        #然后是几个大的
        divs = html.xpath(u'//div[@class="boitem w790"]//h4//label[@class="left" and text() != "基金分级信息"]')
        ps = html.xpath('//div[@class="boxitem w790"]//p')
        for (index, div) in enumerate(divs):
            key = div.text.strip()
            #暂时跳过"基金分级信息"这块
            if key == u"基金分级信息":
                continue
            value = ps[index].text.strip()
            self.raw_info[key] = value
            if key == FundInfo.TACTICS_KEY:
                self.tactics = value
            elif key == FundInfo.LIMITS_KEY:
                self.limits = value


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
    def parse_fund(self, fund_content, fund_url):
        if fund_content is None or fund_url is None:
            return None

        fund_info = FundInfo(fund_content)
        fund_info.url = fund_url
        return fund_info