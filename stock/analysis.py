# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from spider_base.analysis import *
from spider_base.convenient import *
reload(sys)
sys.setdefaultencoding('utf-8')
from collector import StockCollector
from entity import StockQuotation, StockInfo

#提供个股信息,纯数据输出,可以自己用也可以指数模块用
class StockAnalysis(SBAnalysis):

    def __init__(self, path='', db_name=StockCollector.DATABASE_NAME):
         super(StockAnalysis, self).__init__(path + db_name)

    #这个只有一个哦
    def querybycode(self, stock_code):
        sql = 'SELECT * FROM {table_name} WHERE {code_key} = "{code}"'.format(
            table_name=StockCollector.MAIN_TABLE_NAME,code_key=StockInfo.CODE_KEY,code=stock_code)
        raw_result = self.db.execute(sql).fetchone()
        stock_info = StockInfo()
        stock_info.parse_sqlresult(raw_result)
        return stock_info

    # 这个返回的是数组,毕竟我可能回去搜索"中国xx"等股票呢不是吗嘻嘻,连全名,曾用名也一起搜索了啊嘻嘻
    def querybyname(self, stock_name):
        sql = 'SELECT * FROM {table_name} WHERE {name_key} LIKE "%{name}%" OR {usedname_key} LIKE "%{name}%" OR {fullname_key} LIKE "%{name}%"'.format(
            table_name=StockCollector.MAIN_TABLE_NAME,name_key=StockInfo.SHORT_NAME_KEY,name=stock_name,usedname_key=StockInfo.USED_NAME_KEY,fullname_key=StockInfo.FULL_NAME_KEY)
        raw_results = self.db.execute(sql).fetchall()
        results = []
        for raw_result in raw_results:
            stock_info = StockInfo()
            stock_info.parse_sqlresult(raw_result)
            results.append(stock_info)
        return results

    # 查询单个股票的pe和pb,开始结束日期是[]的范围哦,如果不写就从最久到最新
    # 本来是想把处理抹平数据放函数里,输出数据放别的地方,后来发现处理数据也不能放函数里,不然中位数就不准了,故而本函数输出的都是原始数据
    def query_pepb(self, stock_code, begin_date='', end_date=''):
        if begin_date == '' or end_date == '':
            sql = 'SELECT MIN({date}), MAX({date}) FROM {table};'.format(
                date=StockQuotation.DATE_KEY, table=StockCollector._stock_tablename(stock_code))
            result = self.db.execute(sql).fetchone()
            if begin_date == '':
                begin_date = result[0]
            if end_date == '':
                end_date = result[1]

        sql = 'SELECT {}, {}, {} FROM {} WHERE {} BETWEEN "{}" AND "{}";'.format(
            StockQuotation.DATE_KEY, StockQuotation.PE_TTM_KEY, StockQuotation.PB_KEY, StockCollector._stock_tablename(stock_code), StockQuotation.DATE_KEY, begin_date, end_date)
        result = self.db.execute(sql)
        raw_results = result.fetchall()
        results = []
        for raw_result in raw_results:
            quotation = StockQuotation()
            quotation.parse_sqlresult(raw_result)
            results.append(quotation)
        return results

    # 因为日期明确,所以返回也很简单,就是(pes,pbs)但也有可能当天并未开市,所以可能数据是空的
    def query_stocks_pepb_at_date(self, stocks, date):
        pes = []
        pbs = []
        for stock in stocks:
            sql = 'SELECT {pe}, {pb} FROM {table} WHERE {date_key} = "{date}";'.format(
                pe=StockQuotation.PE_TTM_KEY, pb=StockQuotation.PB_KEY, table=StockCollector._stock_tablename(stock),date_key=StockQuotation.DATE_KEY, date=date
            )
            result = self.db.execute(sql).fetchone()
            # 我大胆预测.有一个没有数据的话,肯定都没数据
            if result == None:
                break
            pes.append(result[0])
            pbs.append(result[1])
        return (pes, pbs)

    # 同样也是明确日期范围,不需要校验,但里面到底是不是天天有就不好说了,这里的时间区间是[),返回值形如[(date, [pes], [pbs]), ]
    # 放弃了对其中没有数据时的处理,就用作指数计算平均値的吧,如果非要确定哪天有数据,就只传一个代码好了
    def query_stocks_pepb_in_range(self, stocks, begin_date, end_date=''):
        if end_date == '':
            end_date = now_day()
        results = []
        pe_dict = dict()
        pb_dict = dict()
        # 这个date比较麻烦了,先按照工作日一个个去尝试搜索,如果有就加上,没有就当做那天不开市
        for (index, stock) in enumerate(stocks):
            sql = 'SELECT {date}, {pe}, {pb} FROM {table} WHERE {date} BETWEEN "{begin_date}" AND "{end_date}";'.format(
                date=StockQuotation.DATE_KEY, pe=StockQuotation.PE_TTM_KEY, pb=StockQuotation.PB_KEY, table=StockCollector._stock_tablename(stock), begin_date=begin_date, end_date=end_date
            )
            result = self.db.execute(sql).fetchall()
            if result != None:
                for (date, pe, pb) in result:
                    if date in pe_dict:
                        pes = pe_dict[date]
                        pes.append(pe)
                    else:
                        pes = [pe]
                        pe_dict[date] = pes
                    if date in pb_dict:
                        pbs = pb_dict[date]
                        pbs.append(pb)
                    else:
                        pbs = [pb]
                        pb_dict[date] = pbs
                # 没数据基本上肯定是最前面没有,万一出现中间没有的情况我也没办法

        sorted_dates = sorted(pe_dict.keys())
        for date in sorted_dates:
            # 或许存在pe和pb日期不对应哦
            results.append((date, pe_dict[date], pb_dict[date]))
        return results

    # 某些特殊需求,给你一串002211,223311翻译过来中文名,注意有个问题就是一旦你输入错号码,那么返回的结果数目就会对不上,而且我也不知道哪些是正确的
    # todo 需要修正
    def translate_codes(self, codes):
        names = []
        for code in codes:
            sql = 'SELECT {short_name_key} FROM {table_name} WHERE {code_key} = "{code}"'.format(
                short_name_key=StockInfo.SHORT_NAME_KEY, table_name=StockCollector.MAIN_TABLE_NAME,code_key=StockInfo.CODE_KEY, code=code)
            results = self.db.execute(sql).fetchall()
            if len(results) > 0:
                names.append(results[0][0])
            else:
                names.append("")
        return names

    # 相反的,把名字改为code
    def translate_names(self, names):
        sql = 'SELECT {code_key} FROM {table_name} WHERE {short_name_key} IN (%s)'.format(
            code_key=StockInfo.CODE_KEY, table_name=StockCollector.MAIN_TABLE_NAME,short_name_key=StockInfo.SHORT_NAME_KEY) % ','.join('?' for name in names)
        results = self.db.execute(sql, names).fetchone()
        return  [i[0] for i in results]

    def last_update_date(self):
        sql = 'SELECT MAX({date_key}) FROM {table_name};'.format(date_key=StockQuotation.DATE_KEY, table_name=StockCollector._stock_tablename('600000'))
        return self.db.execute(sql).fetchone()[0]

if __name__ == "__main__":
    a = StockAnalysis()
    # print_container(a.translate_codes(['600000', '000002']))
    # print a.translate_names([u'万科A', u'平安银行'])
    # print a.query_stocks_pepb_in_range(['600000'], '2017-05-01', '2019-01-10')
    # print (1, 2, None)
    # print '{name} is {{aa'.format(name='xixi')
    # print_container(a.querybyname(''))
    print a.last_update_date()