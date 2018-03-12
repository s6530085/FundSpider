# -*- coding: utf-8 -*-
__author__ = 'study_sun'
import requests
import sys
import hashlib
import re

reload(sys)
sys.setdefaultencoding('utf-8')

from spider_base import SBDownloader

class StockDownloader(SBDownloader):

    def __init__(self):
        super(StockDownloader, self).__init__()
        self.snowball_logined = False

    #代码来自https://github.com/xchaoinfo/fuck-login/blob/master/012%20xueqiu.com/xueqiu.py
    def login_snowball(self):

        def get_md5(password):
            md5 = hashlib.md5()
            md5.update(password.encode())
            return md5.hexdigest().upper()

        agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        headers = {'User-Agent': agent,
                   'Host': "xueqiu.com",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, sdch, br",
                   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
                   "Connection": "keep-alive"}
        self.snowball_session = requests.session()
        headers['Referer'] = "https://xueqiu.com/"
        login_url = "https://xueqiu.com/account/login"


        postdata = {"areacode": "86",
                    "password": get_md5('jisilu4daibi'),
                    "remember_me": "on",
                    "username": "s6530085@hotmail.com"}
        #先登录
        rl = self.snowball_session.post(login_url, data=postdata, headers=headers)
        #再看看登录成功了没
        log = self.snowball_session.get("https://xueqiu.com/setting/user", headers=headers)
        pa = r'"profile":"/(.*?)","screen_name":"(.*?)"'
        res = re.findall(pa, log.text)
        if res == []:
            print("登录失败，请检查你的手机号和密码输入是否正确")
            return False
        else:
            print('登录成功 你的雪球用户 id 是：%s, 你的用户名是：%s' % (res[0]))
            self.snowball_logined = True
            self.snowball_headers = headers
            return True


    def download(self, url):
        #如果是雪球的网址,还得先登录哦
        def url_is_snowball(url):
            return 'xueqiu.com' in url

        if url_is_snowball(url):
            if not self.snowball_logined:
                self.login_snowball()
            return super(StockDownloader, self).download(url, self.snowball_session, self.snowball_headers)
        else:
            return super(StockDownloader, self).download(url)


if __name__ == '__main__':
    a = StockDownloader()
    s = a.download('https://xueqiu.com/v4/stock/quote.json?code=SZ000002')
    print s
