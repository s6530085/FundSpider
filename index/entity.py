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

    FULL_CODE_KEY = u'full_code'
    FULL_CODE_CHINESE_KEY = u'指数代码'

    NAME_KEY = u'name'
    NAME_CHINESE_KEY = u'指数名称'

    SHORT_NAME_KEY = u'short_name'
    SHORT_NAME_CHINESE_KEY = u'指数简写'

    BEGIN_TIME_KEY = u'begin_time'
    BEGIN_TIME_CHINESE_KEY = u'启用日期'

    WEAVE_KEY = u'weave'
    WEAVE_CHINESE_KEY = u'编制方案'


    def __init__(self):
        self.code = u'' #就是 399978
        self.full_code = u'' #形如000001.XSHG,有的地方接口非要这个
        self.name = u''
        self.short_name = u''
        self.begin_time = u''
        self.weave = u'' #编制方式,一般是个url

    def parse_sqlresult(self, sql_result):
        self.code = sql_result[0]
        self.full_code = sql_result[1]
        self.name = sql_result[2]
        self.short_name = sql_result[3]
        self.begin_time = sql_result[4]
        self.weave = sql_result[5]


    @classmethod
    def all_keys(cls):
        return [IndexInfo.CODE_KEY, IndexInfo.FULL_CODE_KEY, IndexInfo.NAME_KEY, IndexInfo.SHORT_NAME_KEY, IndexInfo.BEGIN_TIME_KEY, IndexInfo.WEAVE_KEY]

    @classmethod
    def all_desc_keys(cls):
        return [IndexInfo.CODE_CHINESE_KEY, IndexInfo.FULL_CODE_CHINESE_KEY, IndexInfo.NAME_CHINESE_KEY, IndexInfo.SHORT_NAME_CHINESE_KEY, IndexInfo.BEGIN_TIME_CHINESE_KEY, IndexInfo.WEAVE_CHINESE_KEY]


#指数成分股,处于合理性考虑,不可能将一个指数的每日的成分股都记录下来,过于冗余了,目前的想法有两个,一种是记录每个成分股的纳入和剔除日期
#一种是记录成分股变化日及所有的成分股
class IndexConstituent(SBObject):

    DATE_KEY = u'c_date'
    DATE_CHINESE_KEY = u''

    CONSTITUENTS_KEY = u'constituents'
    CONSTITUENTS_CHINESE_KEY = u'成分股列表'

    def __init__(self):
        self.c_date = ''
        self.constituents = []

    def parse_sqlresult(self, sql_result):
        self.c_date = sql_result[0]
        self.constituents = sql_result[1]

    @classmethod
    def all_keys(cls):
        return [IndexConstituent.DATE_KEY, IndexConstituent.CONSTITUENTS_KEY]

    @classmethod
    def all_desc_keys(cls):
        return [IndexConstituent.DATE_CHINESE_KEY, IndexConstituent.CONSTITUENTS_CHINESE_KEY]


