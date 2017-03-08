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
            if response.status_code == requests.codes.ok or response.status_code == requests.codes.bad:
                #从雪球下载的时候,会有非200,但是并非下载失败的情况,这里特例一下
                return response.text
            else:
                return None
