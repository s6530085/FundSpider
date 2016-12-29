# -*- coding: utf-8 -*-

class IndexCompareOutputer(object):

    def collect_data(self, data):
        self.raw_data = data

    def output_result(self):
        print self.raw_data

