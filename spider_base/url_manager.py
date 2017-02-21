# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class SBURLManager(object):

    def __init__(self):
        self.finished_urls = set()
        self.feed_urls = set()
        self.failed_urls = set()

    #吃进来的是code
    def add_url(self, url):
        if url not in self.finished_urls and url not in self.feed_urls:
            self.feed_urls.add(url)

    def add_urls(self, urls):
        for url in urls:
            self.add_url(url)

    # 加可以批量加,但移除肯定是一个个移除的
    def finish_url(self, url):
        self.feed_urls.discard(url)
        self.finished_urls.add(url)

    def fail_url(self, url):
        self.failed_urls.add(url)

    def is_empyt(self):
        return len(self.feed_urls) == 0

    def is_overflow(self):
        return False

    def pop_url(self):
        return self.feed_urls.pop()

    def output_faileds(self):
        for url in self.failed_urls:
            print url

    def transfer_url(self):
        self.feed_urls = self.feed_urls.union(self.failed_urls)