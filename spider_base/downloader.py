# -*- coding: utf-8 -*-
__author__ = 'study_sun'
# import urllib2
import requests

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class SBDownloader(object):

    def download(self, url, session=None, headers=None):
        if url is None:
            return None
        if session == None:
            response = requests.get(url, headers=headers)
            if response.status_code != requests.codes.ok:
                return None
            return response.text
        else:
            response = session.get(url, headers=headers)
            if response.status_code != requests.codes.ok:
                return None
            return response.text
        # response = urllib2.urlopen(url,timeout=10)

        # if response.getcode() != 200:
        #     return None

        # 不好直接在这里设置编码,谁知道这个网页到底是什么编码呢
        # return response.read()