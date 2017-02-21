# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SBObject(object):

    @classmethod
    def all_keys(self):
        return []

    @classmethod
    def all_desc_keys(self):
        return []

    #短描述肯定自己写咯
    def short_desc(self):
        return ''

    def full_desc(self):
        format = u''
        for i, key in enumerate(self.all_keys()):
            v = getattr(self, key)
            if isinstance(v, float):
                v = str(v)
            elif isinstance(v, int):
                v = str(v)
            elif isinstance(v, list):
                v = ','.join(v)
            format += self.all_desc_keys()[i] + ' : ' + v + ' \n'
        return format

    def __str__(self):
        return self.full_desc()


class Fuck(SBObject):
    @classmethod
    def all_keys(self):
        return ['position', 'count']

    @classmethod
    def all_desc_keys(self):
        return ['位置', '次数']

    def __init__(self):
        self.position = '前面'
        self.count = 100

def xixi(o):
    o.count = 200

if __name__ == "__main__":
    b = Fuck()
    xixi(b)
    print b