# -*- coding: utf-8 -*-

class IndexCompareURLManager(object):

    def __init__(self):
        self.finished_urls = set()
        self.feed_urls = set()

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

    def is_empyt(self):
        return len(self.feed_urls) == 0

    def is_overflow(self):
        return False #len(self.finished_urls) >= 2

    def pop_url(self):
        return self.feed_urls.pop()
