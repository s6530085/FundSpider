# -*- coding: UTF-8 -*-
__author__ = 'study_sun'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import xlrd


class Series(object):

    def loadFile(self, file):
        # 先读取基金的数据，可能会多次使用
        sheetFunds = file.sheet_by_name('基金池')
        fundDict = dict()
        for i in range(1, sheetFunds.nrows):  # 从1开始，不要最上面的表头
            code = sheetFunds.cell(i, 0).value
            if len(code) > 0:
                d = dict()
                d['name'] = sheetFunds.cell(i, 1).value
                stock = sheetFunds.cell(i, 13).value
                if isinstance(stock, unicode):
                    d['stock'] = 0.0
                else:
                    d['stock'] = stock
                bond = sheetFunds.cell(i, 14).value
                if isinstance(bond, unicode):
                    d['bond'] = 0.0
                else:
                    d['bond'] = bond
                cash = sheetFunds.cell(i, 15).value
                if isinstance(cash, unicode):
                    d['cash'] = 0.0
                else:
                    d['cash'] = cash
                commodity = sheetFunds.cell(i, 16).value
                if isinstance(commodity, unicode):
                    d['commodity'] = 0.0
                else:
                    d['commodity'] = commodity
                fundDict[code] = d
        # 手动塞一个现金的
        d = dict()
        d['name'] = '现金'
        d['cash'] = 1.0
        d['stock'] = 0.0
        d['bond'] = 0.0
        d['commodity'] = 0.0
        fundDict[u'000000'] = d

        return fundDict

    def series(self, file, fundDict, sheetname, forall):
        flows = file.sheet_by_name(sheetname)
        startCol = 2 if forall else flows.ncols - 1

        for j in range(startCol, flows.ncols):
            timeDate =  xlrd.xldate_as_tuple(flows.cell(0,j).value, 0)
            timeString = '{}/{}/{}'.format(timeDate[0], timeDate[1], timeDate[2])
            allMoney = 0.0
            allStock = 0.0
            allBond = 0.0
            allCash = 0.0
            allCommodity = 0.0
            for i in range(1, flows.nrows):
                code = flows.cell(i, 0).value
                if len(code) > 0:
                    fundInfo = fundDict.get(code, 0)
                    if fundInfo == 0:
                        print '{} 没找到对应基金信息, 名称为{}'.format(code, flows.cell(i, 1).value)
                        # 没信息就是股票
                        stock = flows.cell(i, j).value
                        if not isinstance(stock, unicode):
                            allStock += stock
                            allMoney += stock
                        continue
                    money = flows.cell(i, j).value
                    if isinstance(money, unicode):
                        continue
                    stock = money * fundInfo['stock']
                    bond = money * fundInfo['bond']
                    cash = money * fundInfo['cash']
                    commodity = money * fundInfo['commodity']
                    allMoney += money
                    allStock += stock
                    allBond += bond
                    allCash += cash
                    allCommodity += commodity
            print '{}中账户在{}共有{}, 股票占比{:.2f}%, 债券占比{:.2f}%, 现金占比{:.2f}%, 商品占比{:.2f}%'\
                .format(sheetname, timeString, allMoney, 100 * allStock / allMoney, 100 * allBond / allMoney, 100 * allCash / allMoney, 100 * allCommodity / allMoney)



if __name__ == "__main__":
    path = '/Users/xiaomin/Downloads/证券.xlsx'
    file = xlrd.open_workbook(path)
    if file is not None:
        t = Series()
        fundDict = t.loadFile(file)
        t.series(file, fundDict, '家庭账户时序表', 1)
        t.series(file, fundDict, '个人账户时序表', 0)