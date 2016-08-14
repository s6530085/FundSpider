# -*- coding: <encoding name> -*-

class IndexCompareMain:
    def __init__(self):
        print 'init'
        pass

    def startWithHomeURL(self, homeURL):
        print 'startWithHomeURL' + homeURL
        pass


if __name__ == "__main__":
    icMain = IndexCompareMain()
    icMain.startWithHomeURL('http://fund.eastmoney.com/allfund.html')