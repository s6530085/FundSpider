# -*- coding: utf-8 -*-
__author__ = 'study_sun'

__all__ = ["safetofloat", "now_day", "print_container", "next_day", "days_in_range", "LAST_ELEMENT_INDEX",
           "STAND_DATE_FORMAT", "to_container", "median", "rounded_to"]

import sys
from datetime import datetime, timedelta, date
import time
import collections

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

# 懒得判断参数是单个还是集合,直接强转为集合好了
def to_container(parameter):
    if isinstance(parameter, collections.Iterable):
        return parameter
    else:
        return [parameter]

# 获取中位数,前提这个list已经是有序的啦,我就不重复排序了
def median(l):
    l = to_container(l)
    length = len(l)
    if length%2==0:
        return (l[length/2-1]+l[length/2])/2
    else:
        return l[length/2]

# 把字符串或数字保留相应位数的小数点,最后返回str
def rounded_to(number, digit=3):
    if not isinstance(number, float):
        number = float(number)
    return ('%.'+str(digit)+'f') % number

if __name__ == "__main__":
    print days_in_range('2011-01-28', '2011-02-03')
    print rounded_to(1.2345, 3)