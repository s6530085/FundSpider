# -*- coding: utf-8 -*-
__author__ = 'study_sun'

__all__ = ["safetofloat", "now_day"]

import sys
import datetime


reload(sys)
sys.setdefaultencoding('utf-8')

def safetofloat(s, df=0.0):
    try:
        return float(s)
    except:
        return df

#除了普通的trip，顺便把头尾的斜杠去掉，只是用在本项目而已
def sbtrip(s):
    pass

def testhehe():
    print 'hehe'

#返回2017-12-02这样的字符串
def now_day():
    return datetime.datetime.now().strftime('%Y-%m-%d')


if __name__ == "__main__":
    print safetofloat('123')