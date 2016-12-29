# -*- coding: utf-8 -*-
import urllib2

# 目前看来下载器是比较泛用的,毕竟只是单纯的下载静态网页,没有什么动态处理
class IndexCompareDownloader(object):

    def download(self, url):
        if url is None:
            return None

        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None

        # 不好直接在这里设置编码,谁知道这个网页到底是什么编码呢
        return response.read()