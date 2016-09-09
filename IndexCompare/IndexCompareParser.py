# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

class FundInfo:
    #一些我比较感兴趣的资讯参数
    code = ''
    CODE_KEY = '基金代码'

    short_name = ''
    SHORT_NAME_KEY = '基金简称'

    full_name = ''
    FULL_NAME_KEY = '基金全称'

    type = ''
    TYPE_KEY = '基金类型'

    release_time = ''
    RELEASE_TIME_KEY = '发行日期'

    capacity = ''
    CAPACITY_KEY = '资产规模'

    company = ''
    COMPANY_KEY = '基金管理人'

    manager = []
    MANAGER_KEY = '基金经理人'

    compare_target = ''
    COMPARE_TARGET_KEY = '业绩比较基准'

    trace_target = ''
    TARCE_TARGET_KEY = '跟踪标的'

    policy = ''
    POLICY_KEY = '投资策略'

    #所有资讯都放在里面,键也是直接使用资讯的中文了嘻嘻
    raw_info = dict()

    def __init__(self, content):
        content = '<table class="info w790"><tr><th>基金全称</th><td style=\'width:300px;padding-right:10px;\'>华夏成长证券投资基金</td><th>基金简称</th><td>华夏成长</td></tr><tr><th>基金代码</th><td>000001（前端）、000002（后端）<th>基金类型</th><td>混合型</td></tr><tr><th>发行日期</th><td>2001年11月28日</td><th>成立日期/规模</th><td>2001年12月18日 / 32.368亿份</td></tr><tr><th>资产规模</th><td>51.27亿元（截止至：2016年06月30日）<th>份额规模</th><td><a href="gmbd_000001.html">46.0327亿份</a>（截止至：2016年06月30日）</td></tr><tr><th>基金管理人</th><td><a href="http://fund.eastmoney.com/company/80000222.html">华夏基金</a></td><th>基金托管人</th><td><a href="http://fund.eastmoney.com/bank/80001068.html">建设银行</a></td></tr><tr><th>基金经理人</th><td><a href="http://fund.eastmoney.com/manager/30282939.html">李铧汶</a>、<a href="http://fund.eastmoney.com/manager/30198442.html">董阳阳</a>、<a href="http://fund.eastmoney.com/manager/30039046.html">许利明</a></td><th>成立来分红</th><td><a href="fhsp_000001.html">每份累计2.30元（18次）</a></td></tr><tr><th>管理费率</th><td>1.50%（每年）</td><th>托管费率</th><td>0.25%（每年）</td></tr><tr><th>销售服务费率</th><td>---（每年）</td><th>最高认购费率</th><td>1.00%（前端）</td></tr><th>最高申购费率</th><td><span style="text-decoration:line-through;color:#666666">1.50%（前端）</span><br><span>天天基金优惠费率：<span style="Color:#ff0000">0.15%（前端）</span></span></td><th>最高赎回费率</th><td>0.50%（前端）</td></tr><tr><th>业绩比较基准</th><td style="color: #808080;">该基金暂未披露业绩比较基准</td><th>跟踪标的</th><td style="color: #808080;">该基金无跟踪标的</td></tr></table>'
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
        table = soup.find('table', _class='info w790')
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        for tr in trs:
            ths = tr.find_all('th')
            tds = tr.find_all('td')
            for index, th in enumerate(ths):
                key = th.text
                value = tds[index].text
                self.raw_info[key] = value

                if key == self.CODE_KEY:
                    #code也分前后端等,懒得管了,就取第一个
                    value = value[:6]
                    self.code = value
                    self.raw_info[key] = value
                elif key == self.SHORT_NAME_KEY:
                    self.short_name = value
                elif key == self.FULL_NAME_KEY:
                    self.full_name = value
                elif key == self.TYPE_KEY:
                    self.type = value
                elif key == self.RELEASE_TIME_KEY:
                    self.release_time = value
                #去掉后面单位和描述只保留数字
                elif key == self.CAPACITY_KEY:
                    value = value.split('亿')[0]
                    self.capacity = value
                    self.raw_info[key] = value
                #这里是个超链接
                elif key == self.COMPANY_KEY:
                    self.company = value
                elif key == self.MANAGER_KEY:
                    value = []
                    #特别处理下基金经理这块,因为可能是多人
                    managers = tds[index].find_all('a')
                    for managerName in managers:
                        value.append(managerName.text)
                    self.raw_info[key] = value
                    self.manager = value
                elif key == self.COMPARE_TARGET_KEY:
                    self.compare_target = value
                elif key == self.TARCE_TARGET_KEY:
                    self.trace_target = value
        #然后是几个大的
        large_divs = soup.find_all('div', _class='boxitem w790')
        for large_div in large_divs:
            key = large_div.find('label', _class='left').text
            value = large_div.find('p').text
            self.raw_info[key] = value
            if key == self.POLICY_KEY:
                self.policy = value


class IndexCompareParser:

    #解析首页主要是获取每个基金的一些基础信息,如基金名,id
    def parse_home(self, home_content):
        if home_content is None:
            return None
        pattern_match = re.compile(ur"（\d{6}）.+")
        pattern_capture = re.compile(ur"（(\d{6})）(.+)")
        # soup = BeautifulSoup(home_content, 'html.parser', from_encoding='gb2312')
        soup = BeautifulSoup(home_content, 'html.parser', from_encoding='utf-8')
        funds = soup.find_all('a', text=pattern_match)
        l = []
        for fund in funds:
            match = pattern_capture.match(fund.text)
            if match:
                l.append((match.group(1), match.group(2)))

        return l

    #这里是解析每个基金的详情了,获得的东西很多,反正都在dict里,键可能会逐步增加,根据未来需要分析的东西扩展
    def parse_fund(self, fund_content, fund_url):
        if fund_content is None or fund_url is None:
            return None

        fund_info = FundInfo(fund_content)
        return fund_info