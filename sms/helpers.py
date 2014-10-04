# -*- coding: utf-8 -*-
__author__ = 'josip@lazic.info'


def ksort(d):
    """
    Emulate PHP's ksort function. In nature Pythons dictionaries are unordered.
    http://www.php2python.com/wiki/function.ksort/
    """
    return [(k,d[k]) for k in sorted(d.keys())]

