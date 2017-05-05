# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import sqlite3
import re

class SBAnalysis(object):

    def __init__(self, db_name=''):
        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.search(item) is not None

        self.db = sqlite3.connect(db_name)
        #关于正则函数是看这里的 http://stackoverflow.com/questions/5365451/problem-with-regexp-python-and-sqlite
        self.db.create_function("REGEXP", 2, regexp)

    def __del__( self ):
        if self.db != None:
            self.db.close()

    def raw_query(self, sql):
        return self.db.cursor().execute(sql)