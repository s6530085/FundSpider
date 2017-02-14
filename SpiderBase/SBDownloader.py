# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import urllib2
import requests

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class SBDownloader(object):

    def download(self, url):
        if url is None:
            return None

        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None

        # 不好直接在这里设置编码,谁知道这个网页到底是什么编码呢
        return response.read()