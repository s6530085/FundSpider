# -*- coding: utf-8 -*-
import re
from lxml import etree
from spider_base.convenient import safe_to_float
from entity import FundInfo
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class FundParser(object):

    #解析首页主要是获取每个基金的一些基础信息,如基金名,id
    def parse_home(self, home_content):
        if home_content is None:
            return None
        home_content = home_content.encode('ISO-8859-1').decode('gbk')
        html = etree.HTML(home_content, parser=etree.HTMLParser(encoding='utf-8'))
        alinks = html.xpath('//a[@href]')

        pattern_capture = re.compile(ur"（(\d{6})）(.+)")
        l = []
        for alink in alinks:
            aa = alink.text
            if aa != None:
                match = pattern_capture.match(aa)
                if match:
                    #名字没用,就只要编号即可
                    # l.append((match.group(1), match.group(2)))
                    l.append(match.group(1))
        return l

    #这里是解析每个基金的详情了,获得的东西很多,反正都在dict里,键可能会逐步增加,根据未来需要分析的东西扩展
    def parse_fund(self, basecontent, ratiocontent, statisticcontent, stockcontent, annualcontent, fundurl):
        fund_info = FundInfo()
        self.parse_base(fund_info, basecontent)
        self.parse_ratio(fund_info, ratiocontent)
        self.parse_statistic(fund_info, statisticcontent)
        self.parse_stocks(fund_info, stockcontent)
        self.parse_annual(fund_info, annualcontent)
        fund_info.url = fundurl
        return fund_info


    #解析基础数据f10
    def parse_base(self, info, content):
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

            if key == FundInfo.CODE_CHINESE_KEY:
                #code也分前后端等,懒得管了,就取第一个
                value = value[:6]
                info.code = value
            elif key == FundInfo.SHORTNAME_CHINESE_KEY:
                info.shortname = value
            elif key == FundInfo.NAME_CHINESE_KEY:
                info.name = value
            elif key == FundInfo.TYPE_CHINESE_KEY:
                info.type = value
            elif key.startswith(FundInfo.RELEASETIME_CHINESE_KEY):
                if len(value) > 0:
                    value = value.split(u'/')[0].strip()
                    #原始格式是YYYY年MM月dd日
                    value = reduce(lambda a, kv: a.replace(*kv), {u"年":u"-",u"月":u"-",u"日":u""}.iteritems(), value)
                    info.releasetime = value
            #去掉后面单位和描述只保留数字
            elif key == FundInfo.SIZE_CHINESE_KEY:
                #某些基金新开或者其他原因没有规模
                if len(value.split(u'亿')) > 0:
                    value = value.split(u'亿')[0]
                info.size = safe_to_float(value)
            #这里是个超链接
            elif key == FundInfo.COMPANY_CHINESE_KEY:
                info.company = value
            elif key == FundInfo.MANAGER_CHINESE_KEY:
                value = []
                #特别处理下基金经理这块,因为可能是多人,其实还可能有重名的情况,不过暂且相信一个基金公司下的基金经理不会重名吧
                managers = tds[index].xpath('./a')
                for managerName in managers:
                    value.append(managerName.text.strip())
                info.manager = value
            elif key == FundInfo.COMPARE_CHINESE_KEY:
                info.compare = value
            elif key == FundInfo.TRACK_CHINESE_KEY:
                info.track = value
            elif key == FundInfo.MANAGE_FEE_CHINESE_KEY:
                if len(value.split("%")) > 0:
                    info.fee += safe_to_float(value.split('%')[0])
            elif key == FundInfo.COSTODY_FEE_CHINESE_KEY:
                if len(value.split("%")) > 0:
                    info.fee += safe_to_float(value.split('%')[0])
            elif key == FundInfo.BUY_FEE_CHINESE_KEY:
                #这里比较复杂,可能有天天基金的打折信息,先看看有没有打折吧
                spans = tds[index].xpath('.//span')
                if len(spans) == 3:
                    info.fee += safe_to_float(spans[2].text.split("%")[0])
                elif len(spans) == 0:
                    if len(value.split("%")) > 0:
                        info.fee += safe_to_float(value.split('%')[0])

            elif key == FundInfo.SELL_FEE_CHINESE_KEY:
                if len(value.split("%")) > 0:
                    info.fee += safe_to_float(value.split('%')[0])

        #然后是几个大的
        divs = html.xpath(u'//div[@class="boxitem w790"]//h4//label[@class="left" and text() != "基金分级信息"]')
        ps = html.xpath('//div[@class="boxitem w790"]//p')
        for (index, div) in enumerate(divs):
            key = div.text.strip()
            value = ps[index].text.strip()
            # if key == FundInfo.TACTICS_CHINESE_KEY:
            #     self.tactics = value
            if key == FundInfo.LIMITS_CHINESE_KEY:
                #很不爽的，字符串里有单引号也有双引号，导入到数据库里会冲突，所以把所有引号转为-，反正意思能懂就行，中文引号不需要转
                info.limits = value.replace('"', '--').replace("'", "--")

    #解析持有人结构,优先选择机构持有比例高的,这个似乎在源代码中不能直接获得
    def parse_ratio(self, info, content):
        # content = content.split('"')[1]
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        tds = html.xpath('//td[@class="tor"]')
        if len(tds) > 2:
            #取最新的即可,不过可能是---哦
            #这里有点疑问，我以为机构持有人里是包含内部持有人的，但目前发现一个基金http://fund.eastmoney.com/f10/cyrjg_510090.html内部持有人>机构持有人，但大部分基金是机构+个人=100%，且内部<=基金，不知道哪里出了问题
            insito = tds[0].text
            if insito != '---':
                info.inratio += safe_to_float(insito.split("%")[0])
            # innerto = tds[2].text
            # if innerto != '---':
            #     self.inratio += safe_to_float(innerto.split("%")[0])
            # self.inratio = safe_to_float(.split('%')[0]) + safe_to_float(tds[2].text.split('%')[0])

    #解析标准差夏普率等,当然可能是没有的
    def parse_statistic(self, info, content):
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        nums = html.xpath(u'//table[@class="fxtb"]//td')
        length = len(nums)
        if length % 4 == 3:
            nums = nums[0:length - 3]
            length -= 3
        if (length > 0 and length%4==0):
            for i in range(0, length/4):
                tds = nums[i*4:(i+1)*4]
                #有可能只有若干个指标,只能分别判断
                if tds[0].text == FundInfo.STD_CHINESE_KEY:
                    stds = reversed(tds[1:4])
                    for stdnum in stds:
                        #只有1,2,3年的数值,而且可能新基金连1年的都没有,需要判断下,以最多年的数据为准,下同
                        if stdnum.text != '--':
                            info.std = safe_to_float(stdnum.text.split('%')[0])
                            break
                elif tds[0].text == FundInfo.SHARPERATIO_CHINESE_KEY:
                    sharpes = reversed(tds[1:4])
                    for sharpenum in sharpes:
                        if sharpenum.text != '--':
                            info.sharperatio = safe_to_float(sharpenum.text)
                            break
                elif tds[0].text == FundInfo.INFORATIO_CHINESE_KEY:
                    infos = reversed(tds[1:4])
                    for infonum in infos:
                        if infonum.text != '--':
                            info.inforatio = safe_to_float(infonum.text)
                            break

        #只有指数基金才有追踪误差哦
        trackbias = html.xpath(u'//div[@id="jjzsfj"]//table[@class="fxtb"]//td')
        if len(trackbias) == 3:
            info.bias = safe_to_float(trackbias[1].text.split('%')[0])

        #投资风格,当然也可能没有
        styles = html.xpath('//table[@class="fgtb"]//td')
        if len(styles) >= 2:
            #自然是取最近的就行了
            info.style = styles[1].text.strip()

    def parse_stocks(self, info, content):
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        #只记录最新的一次持仓即可,老持仓暂时对我没有参考意义
        tbs = html.xpath('//table[@class="w782 comm tzxq"]')
        # pers = html.xpath('//table[@class="w782 comm tzxq"]')
        if len(tbs) > 0:
            #懒得记录编号了,直接用名字
            stocktds = tbs[0].xpath('.//td[@class="tol"]/a')
            pers = tbs[0].xpath('.//td[@class="tor"]')
            # 新基金没有成分股的变动,缺少元素,不能直接用5做间隔
            front, interval = 2, 5
            if not '最新价' in content:
                front, interval = 0, 3
            for (index, stocked) in enumerate(stocktds):
                # info.stocks.append(stocked.text)
                # tor的太多了,我只需要其中第三个
                per = pers[index*interval+front]
                # 有这种奇葩的可能 "进入上市公司的十大流通股东却没有进入单只基金前十大重仓股的个股" 没办法只好去掉了
                if per == '---':
                    continue
                # 懒得再做一个字段了,就用[国投电力-3.6%,川投能源-4.1%]这种形式了
                # 不过网站有时候有bug,会没有文本,只好防范一下
                stockname = stocked.text
                if not stockname is None and len(stockname) > 0:
                    info.stocks.append(stockname + '-' + per.text)


    def parse_annual(self, info, content):
        #需要小心的是,收益算年化,排名则是算术平均值,以及没有数值不能简单地以0替代,否则会有偏差
        #目前只能获得最多八年的记录
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        trs = html.xpath('//table/tbody/tr')
        #第一个是收益,第四个是排名
        if len(trs)==5:
            yieldtds = trs[0].xpath('./td')
            #第一个是标题
            yieldvalue = 1.0
            yieldpow = 0.0
            #其实反了,不过就数学上没差别
            for yearyield in yieldtds[1:]:
                y = yearyield.text
                if y != '---':
                    yieldvalue *= (1 + safe_to_float(y.split('%')[0]) / 100)
                    yieldpow += 1
            #如果一个都没有就别算了
            if yieldpow != 0.0:
                info.annualyield = yieldvalue ** (1.0/yieldpow) - 1

            ranktds = trs[3].xpath('./td')
            rankcount = 0
            rankvalue = 0.0
            for ranktd in ranktds[1:]:
                r = ''.join(ranktd.itertext()).strip()
                if r != '---':
                    rankvalue += safe_to_float(r.split('|')[0]) / safe_to_float(r.split('|')[1])
                    rankcount += 1
            if rankcount > 0:
                info.annualrank = rankvalue / rankcount

if __name__ == "__main__":
    pass