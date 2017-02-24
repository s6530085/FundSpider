# -*- coding: utf-8 -*-
__author__ = 'study_sun'
from lxml import etree
from entity import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class IndexParser(object):
    pass

    def parse_index_list(self, index_list_content):
        parsed_content = etree.HTML(index_list_content, parser=etree.HTMLParser(encoding='utf-8'))
        trs = parsed_content.xpath('//tbody/tr')
        indexs = []
        for tr in trs:
            tds = tr.xpath('./td')
            if len(tds) == 5:
                index = IndexInfo()
                code = tds[0].text.strip()
                if len(code.split('.')) == 2:
                    index.code = code.split('.')[0]
                    index.full_code = code
                index.name = tds[1].text.strip()
                index.begin_time = tds[2].text.strip()
                index.short_name = tds[3].text.strip()
                #大部分是url,偶尔是只有文字的
                weave = tds[4].xpath('./a')
                if len(weave) == 1:
                    index.weave = weave[0].attrib['href'].strip()
                else:
                    index.weave = tds[4].text.strip()
                indexs.append(index)
        return indexs