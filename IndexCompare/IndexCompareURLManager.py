# -*- coding: utf-8 -*-

class IndexCompareURLManager:

    def __init__(self):
        self._finished_urls = set()
        self._feed_urls = set()

    def add_url(self, url):
        if url not in self._finished_urls and url not in self._feed_urls:
            self._feed_urls.add(url)

    def add_urls(self, urls):
        for url in urls:
            self.add_url(url)

    # 加可以批量加,但移除肯定是一个个移除的
    def finish_url(self, url):
        self._feed_urls.remove(url)
        self._finished_urls.add(url)

    def is_empyt(self):
        return self._feed_urls