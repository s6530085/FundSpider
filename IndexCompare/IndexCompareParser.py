# -*- coding: utf-8 -*-
import re
from lxml import etree
from SpiderBase.SBConvenient import safetofloat
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class FundInfo(object):

    DATABASE_TABLE_NAME = u'fundinfo'
    #一些我比较感兴趣的资讯参数,默认大写的是类变量,小写的是成员变量
    CODE_KEY = u'code'
    CODE_CHINESE_KEY = u'基金代码'

    NAME_KEY = u'name'
    NAME_CHINESE_KEY = u'基金全称'

    SHORTNAME_KEY = u'shortname'
    SHORTNAME_CHINESE_KEY = u'基金简称'

    TYPE_KEY = u'type'
    TYPE_CHINESE_KEY = u'基金类型'

    RELEASETIME_KEY = u'releasetime'
    RELEASETIME_CHINESE_KEY = u'发行日期'

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

    #十大持仓,懒得写也是和经理人一样用逗号分割了,而且如果有半年/年报的话,最多是20大持仓

    STOCKS_KEY = u'stocks'
    STOCKS_CHINESE_KEY = u'股票投资明细'

    #年度收益率,太细的没必要看,直接转化为年化收益
    ANNUALYIELD_KEY = u'annualyield'
    ANNUALYIELD_CHINESE_KEY = u'年度涨幅'

    #年度收益的同列排行,原始数据是 99|200, 2|201, 最后以算术平均值,按理说同类中越小越好,可能会有更好的统计方式,但我还没想到
    ANNUALRANK_KEY = u'annualrank'
    ANNUALRANK_CHINESE_KEY = u'同类排名'

    ALL_KEYS = [CODE_KEY, NAME_KEY, SHORTNAME_KEY, TYPE_KEY, RELEASETIME_KEY, SIZE_KEY, COMPANY_KEY, MANAGER_KEY, COMPARE_KEY, TRACK_KEY, URL_KEY, INRATIO_KEY, STD_KEY, SHARPERATIO_KEY, INFORATIO_KEY, BIAS_KEY, STOCKS_KEY, ANNUALYIELD_KEY ,ANNUALRANK_KEY]
    ALL_CHINESE_KEYS = [CODE_CHINESE_KEY, NAME_CHINESE_KEY, SHORTNAME_CHINESE_KEY, TYPE_CHINESE_KEY, RELEASETIME_CHINESE_KEY, SIZE_CHINESE_KEY, COMPANY_CHINESE_KEY, MANAGER_CHINESE_KEY, COMPARE_CHINESE_KEY, TRACK_CHINESE_KEY, URL_CHINESE_KEY, INRATIO_CHINESE_KEY, STD_CHINESE_KEY, SHARPERATIO_CHINESE_KEY, INFORATIO_CHINESE_KEY, BIAS_CHINESE_KEY, STOCKS_CHINESE_KEY, ANNUALYIELD_CHINESE_KEY ,ANNUALRANK_CHINESE_KEY]

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
        self.url = u""
        self.inratio = 0
        self.std = 0.0
        self.sharperatio = 0.0
        self.inforatio = 0.0
        self.bias = 0.0
        self.stocks = []
        self.annualyield = -1.0  # 这里用0也不一定妥当,因为可能会有负的收益,那么0反而是不亏的,所以就设置为一个负值,因为是年化,所以不可能低于-1
        self.annualrank = 1.0  # 为什么默认值为1呢,因为这个数值是越小越好,结果默认就是0的话,在排序时就可能搞的没数据的反而排最前面了
        # 所有资讯都放在里面,键也是直接使用资讯的中文了嘻嘻
        self.raw_info = dict()

    def __str__(self):
        return self.full_desc()

    #简单的就只打印编号,简称和url
    def short_desc(self):
        return u'{}: {} {}: {} {}: {} '.format(FundInfo.CODE_CHINESE_KEY, self.code, FundInfo.NAME_CHINESE_KEY, FundInfo.name, FundInfo.URL_CHINESE_KEY, FundInfo.url)

    def middle_desc(self):
        return ''

    #全称吗自然全打印咯
    def full_desc(self):
        format = u''
        for i, key in enumerate(FundInfo.ALL_KEYS):
            format += FundInfo.ALL_CHINESE_KEYS[i] + ' : ' + getattr(self, key) + ' \n'
        return format()
        # return u'{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n'.format\
        #     (FundInfo.CODE_KEY, self.code, FundInfo.NAME_KEY, self.name, FundInfo.SHORTNAME_KEY, self.shortname,\
        #      FundInfo.SIZE_KEY, self.size, FundInfo.COMPANY_KEY, self.company, FundInfo.MANAGER_KEY, u",".join(self.manager),\
        #      FundInfo.COMPARE_KEY, self.compare, FundInfo.TRACK_KEY, self.track,\
        #      FundInfo.LIMITS_KEY, self.limits, FundInfo.TACTICS_KEY, self.tactics, FundInfo.URL_KEY, self.url)

    def parse_sqlresult(self, sqlresult):
        self.code = sqlresult[0]
        self.name = sqlresult[1]
        self.shortname = sqlresult[2]
        self.type = sqlresult[3]
        self.size = sqlresult[4]
        self.company = sqlresult[5]
        self.manager = sqlresult[6].split(u',')
        self.compare = sqlresult[7]
        self.track = sqlresult[8]
        self.limits = sqlresult[9]
        self.url = sqlresult[10]
        self.inratio = sqlresult[11]
        self.std = sqlresult[12]
        self.sharperatio = sqlresult[13]
        self.inforatio = sqlresult[14]
        self.bias = sqlresult[15]
        self.stocks = sqlresult[16].split(u',')
        self.annualyield = sqlresult[17]
        self.annualrank = sqlresult[18]

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

            if key == FundInfo.CODE_CHINESE_KEY:
                #code也分前后端等,懒得管了,就取第一个
                value = value[:6]
                self.code = value
                self.raw_info[key] = value
            elif key == FundInfo.SHORTNAME_CHINESE_KEY:
                self.shortname = value
            elif key == FundInfo.NAME_CHINESE_KEY:
                self.name = value
            elif key == FundInfo.TYPE_CHINESE_KEY:
                self.type = value
            elif key == FundInfo.RELEASETIME_CHINESE_KEY:
                self.releasetime = value
            #去掉后面单位和描述只保留数字
            elif key == FundInfo.SIZE_CHINESE_KEY:
                #某些基金新开或者其他原因没有规模
                if len(value.split(u'亿')) > 0:
                    value = value.split(u'亿')[0]
                self.size = safetofloat(value)
                self.raw_info[key] = safetofloat(value)
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
            # if key == FundInfo.TACTICS_CHINESE_KEY:
            #     self.tactics = value
            if key == FundInfo.LIMITS_CHINESE_KEY:
                #很不爽的，字符串里有单引号也有双引号，导入到数据库里会冲突，所以把所有引号转为-，反正意思能懂就行，中文引号不需要转
                self.limits = value.replace('"', '--').replace("'", "--")

    #解析持有人结构,优先选择机构持有比例高的,这个似乎在源代码中不能直接获得
    def parse_ratio(self, content):
        # content = content.split('"')[1]
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        tds = html.xpath('//td[@class="tor"]')
        if len(tds) > 2:
            #取最新的即可,不过可能是---哦
            #这里有点疑问，我以为机构持有人里是包含内部持有人的，但目前发现一个基金http://fund.eastmoney.com/f10/cyrjg_510090.html内部持有人>机构持有人，但大部分基金是机构+个人=100%，且内部<=基金，不知道哪里出了问题
            insito = tds[0].text
            if insito != '---':
                self.inratio += safetofloat(insito.split("%")[0])
            # innerto = tds[2].text
            # if innerto != '---':
            #     self.inratio += safetofloat(innerto.split("%")[0])
            # self.inratio = safetofloat(.split('%')[0]) + safetofloat(tds[2].text.split('%')[0])

    #解析标准差夏普率等,当然可能是没有的
    def parse_statistic(self, content):
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
                            self.std = safetofloat(stdnum.text.split('%')[0])
                            break
                elif tds[0].text == FundInfo.SHARPERATIO_CHINESE_KEY:
                    sharpes = reversed(tds[1:4])
                    for sharpenum in sharpes:
                        if sharpenum.text != '--':
                            self.sharperatio = safetofloat(sharpenum.text)
                            break
                elif tds[0].text == FundInfo.INFORATIO_CHINESE_KEY:
                    infos = reversed(tds[1:4])
                    for infonum in infos:
                        if infonum.text != '--':
                            self.inforatio = safetofloat(infonum.text)
                            break

        #只有指数基金才有追踪误差哦
        trackbias = html.xpath(u'//div[@id="jjzsfj"]//table[@class="fxtb"]//td')
        if len(trackbias) == 3:
            self.bias = safetofloat(trackbias[1].text.split('%')[0])

    def parse_stocks(self, content):
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        #只记录最新的一次持仓即可,老持仓暂时对我没有参考意义
        tbs = html.xpath('//table[@class="w782 comm tzxq"]')
        if len(tbs) > 0:
            #懒得记录编号了,直接用名字
            stocktds = tbs[0].xpath('.//td[@class="tol"]/a')
            for stocked in stocktds:
                self.stocks.append(stocked.text)

    def parse_annual(self, content):
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
                    yieldvalue *= (1 + safetofloat(y.split('%')[0])/100)
                    yieldpow += 1
            #如果一个都没有就别算了
            if yieldpow != 0.0:
                self.annualyield = yieldvalue ** (1.0/yieldpow) - 1

            ranktds = trs[3].xpath('./td')
            rankcount = 0
            rankvalue = 0.0
            for ranktd in ranktds[1:]:
                r = ''.join(ranktd.itertext()).strip()
                if r != '---':
                    rankvalue += safetofloat(r.split('|')[0]) / safetofloat(r.split('|')[1])
                    rankcount += 1
            if rankcount > 0:
                self.annualrank = rankvalue / rankcount

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
    def parse_fund(self, basecontent, ratiocontent, statisticcontent, stockcontent, annualcontent, fundurl):
        fund_info = FundInfo()
        fund_info.parse_base(basecontent)
        fund_info.parse_ratio(ratiocontent)
        fund_info.parse_statistic(statisticcontent)
        fund_info.parse_stocks(stockcontent)
        fund_info.parse_annual(annualcontent)
        fund_info.url = fundurl
        return fund_info

if __name__ == "__main__":
    print ','.join([1,2,3,4,5])