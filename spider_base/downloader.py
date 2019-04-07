# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import requests
import sys
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')

class SBDownloader(object):

    def download(self, url, cookie=None, headers=None):
        if url is None:
            return None
        if cookie == None:
            response = requests.get(url, headers=headers)
            if response.status_code != requests.codes.ok:
                return None
            return response.text
        else:
            response = requests.get(url, cookies=cookie, headers=headers)
            if response.status_code == requests.codes.ok or response.status_code == requests.codes.bad:
                #从雪球下载的时候,会有非200,但是并非下载失败的情况,这里特例一下
                return response.text
            else:
                return None

    def download_file(self, url):
        if url is None:
            return None
        filename = 'stock_list.xls'
        urllib.urlretrieve(url, filename)
        return filename
