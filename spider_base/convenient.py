# -*- coding: utf-8 -*-
__author__ = 'study_sun'

__all__ = ["safetofloat", "now_day", "print_container", "next_day", "days_in_range", "LAST_ELEMENT_INDEX", "STAND_DATE_FORMAT"]

import sys
from datetime import datetime, timedelta, date
import time

reload(sys)
sys.setdefaultencoding('utf-8')

STAND_DATE_FORMAT = '%Y-%m-%d'
FIRST_ELEMENT_INDEX = 0
LAST_ELEMENT_INDEX = -1 # 当然啦,如果没元素会异常哦

def safetofloat(s, df=0.0):
    try:
        return float(s)
    except:
        return df

# 除了普通的trip，顺便把头尾的斜杠去掉，只是用在本项目而已
def sbtrip(s):
    pass

def testhehe():
    print 'hehe'

# 返回2017-12-02这样的字符串
def now_day(format=STAND_DATE_FORMAT):
    return datetime.now().strftime(format)

# 输入一个2017-01-01的字符串,返回一个2017-01-02的字符串
def next_day(day, input_format=STAND_DATE_FORMAT, output_format=STAND_DATE_FORMAT):
    t = time.strptime(day, input_format)
    newdate = date(t.tm_year,t.tm_mon,t.tm_mday) + timedelta(1)
    return newdate.strftime(output_format)

# 返回[begin_date, end_date)的字符串数组哦
def days_in_range(begin_date, end_date, format=STAND_DATE_FORMAT):
    days = []
    if begin_date < end_date:
        day = begin_date
        days.append(day)
        while day < end_date:
            day = next_day(day, format, format)
            days.append(day)
    return days

def print_container(container):
    for item in container:
        print item

if __name__ == "__main__":
    print days_in_range('2011-01-28', '2011-02-03')