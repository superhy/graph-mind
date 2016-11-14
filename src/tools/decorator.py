# -*- coding: utf-8 -*-

'''
Created on 2016年11月14日

@author: superhy

'''

from __future__ import absolute_import, division, print_function

from inspect import isbuiltin
from logging import getLogger
import sys
import warnings

log = getLogger(__name__)


def deprecated(func):
    """
    warning that user has just called a deprecated function!
    """
    if callable(func):
        def new_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter
            warnings.warn("you just called to a deprecated function: {0}. it should be replaced by another one!".format(func.__name__),
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return func(*args, **kwargs)
        new_func.__name__ = func.__name__
        new_func.__doc__ = func.__doc__
        new_func.__dict__.update(func.__dict__)
    else:
        raise NotImplementedError()
    return new_func