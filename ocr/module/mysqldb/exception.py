#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project:spider_v3
Name:exceptions
Desc:自定义异常处理类
Contant:zhangx@gzfsnet.com
Site:www.fengshen.com
Created by fs on 2018/6/22 - 15H
"""


class MyException(Exception):
    """"屏蔽掉自带的Exception"""

    def __init__(self):
        pass


class MySQLQueryException(MyException):
    def __init__(self, error, context):
        MyException.__init__(self)
        self.value = u"查询数据库出错\n " \
                     u"{error}\n" \
                     u"{context}".format(error=error, context=context)

    def __str__(self):
        return self.value


class MySQLException(MyException):
    def __init__(self, error, context):
        MyException.__init__(self)
        self.value = u"查询数据库出错\n " \
                     u"{error}\n" \
                     u"{context}".format(error=error, context=context)
        print(self.value)

    def __str__(self):
        return self.value


class IgnoreRequest(Exception):
    """Indicates a decision was made not to process a request"""


class DontCloseSpider(Exception):
    """Request the spider not to be closed yet"""
    pass


class CloseSpider(Exception):
    """Raise this from callbacks to request the spider to be closed"""

    def __init__(self, reason='cancelled'):
        super(CloseSpider, self).__init__()
        self.reason = reason


# Items

class DropItem(Exception):
    """Drop item from the item pipeline"""
    pass


class NotSupported(Exception):
    """Indicates a feature or method is not supported"""
    pass


# Commands

class UsageError(Exception):
    """To indicate a command-line usage error"""

    def __init__(self, *a, **kw):
        self.print_help = kw.pop('print_help', True)
        super(UsageError, self).__init__(*a, **kw)


class ScrapyDeprecationWarning(Warning):
    """Warning category for deprecated features, since the default
    DeprecationWarning is silenced on Python 2.7+
    """
    pass


class ContractFail(AssertionError):
    """Error raised in case of a failing contract"""
    pass
