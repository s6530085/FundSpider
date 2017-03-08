# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

STOCK_QUOTATION_NET = 'snowball'
STOCK_INFO_NET = 'eastmoney'

def _code_market(code):
    if code.startswith('60'):
        return 'sh'
    elif code.startswith('00'):
        return 'sz'
    elif code.startswith('30'):
        return 'sz'
    else:
        print 'hehe'
        return ''

#有code,返回东方财富以及搜狐的相关连接用代码
def joint_code(code, net):
    fix = _code_market(code)
    if net == STOCK_QUOTATION_NET:
        return fix + code
    elif net == STOCK_INFO_NET:
        return fix + code
    else:
        return ''

