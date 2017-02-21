# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sys
import xlrd

reload(sys)
sys.setdefaultencoding('utf-8')

class StocksAnalysis(object):
    pass

if __name__ == "__main__":
    # print ts.get_stock_basics()

    # d1 = ts.get_report_data(2008,4)
    # d2 = ts.get_report_data(2016,2)
    # d3 = ts.get_report_data(2016,3)
    # d4 = ts.get_report_data(2016,4)
    # d1.to_sql('testtable', sqlite3.connect('test.db'), flavor='sqlite')
    # a = 10
    # print ''
    # print d1
    # con = sqlite3.connect('test.db')
    # t = con.cursor().execute('select * from testtable')
    # for ti in t:
    #     print ti

    index_history = xlrd.open_workbook('constituent_change.xlsx')
    table_50 = index_history.sheet_by_name(u'上证50')
    row2 = table_50.col_values(2)
    # for row in row2:
        # print row.

    for i in range(table_50.nrows ):
      print table_50.row_values(i)