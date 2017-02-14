# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from SpiderBase import SBURLManager
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class StockURLManager(SBURLManager):

    def pop_url(self):
        url = self.feed_urls.pop()
        return ('http://f10.eastmoney.com/f10_v2/CompanySurvey.aspx?code=' + url, url)