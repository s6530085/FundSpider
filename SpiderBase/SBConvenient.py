# -*- coding: utf-8 -*-
__author__ = 'study_sun'

__all__ = ["safetofloat"]

def safetofloat(s, df=0.0):
    try:
        return float(s)
    except:
        return df


def testhehe():
    print 'hehe'


if __name__ == "__main__":
    print safetofloat('123')