# -*- coding: utf-8 -*-
__author__ = 'study_sun'

def safetofloat(s, df=0):
    try:
        return float(s)
    except:
        return df

if __name__ == "__main__":
    print safetofloat('aaa')