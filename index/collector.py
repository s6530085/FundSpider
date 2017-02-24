# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class IndexCollector(object):

    DATABASE_TABLE_NAME = u'indexinfo'
    DATABASE_NAME = 'index.db'

    def update_indexs(self, indexs):
        pass