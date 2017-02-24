# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sys
from spider_base.entity import *
reload(sys)
sys.setdefaultencoding('utf-8')
#因为获取数据所限,指数没有太多数据结构

class IndexInfo(SBObject):

    CODE_KEY = u'code'
    CODE_CHINESE_KEY= u"指数编号"

    FULL_CODE_KEY = u''

    def __init__(self):
        self.code = u'' #就是 399978
        self.full_code = u'' #形如000001.XSHG,有的地方接口非要这个
        self.name = u''
        self.short_name = u''
        self.begin_time = u''
        self.weave = u'' #编制方式,一般是个url

    @classmethod
    def all_keys(cls):
        return []

    @classmethod
    def all_desc_keys(cls):
        return []


#指数成分股,处于合理性考虑,不可能将一个指数的每日的成分股都记录下来,过于冗余了,目前的想法有两个,一种是记录每个成分股的纳入和剔除日期
#一种是记录成分股变化日及所有的成分股
class IndexConstituent(SBObject):

    DATE_KEY = u'c_date'
    DATE_CHINESE_KEY = u''


    def __init__(self):
        self.c_date = ''

    @classmethod
    def all_keys(cls):
        return []

    @classmethod
    def all_desc_keys(cls):
        return []


