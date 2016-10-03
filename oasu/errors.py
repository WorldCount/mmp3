#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

__author__ = 'WorldCount'


# Ошибка ОАСУ
class OasuError(Exception):

    def __init__(self, message=None):
        if message:
            self._message = message
        else:
            self._message = 'Ошибка ОАСУ'

    def error_message(self):
        return self._message


# Ошибка ожидания соединения с ОАСУ
class OasuTimeoutError(OasuError):

    def __init__(self, message=None):
        super(OasuTimeoutError, self).__init__(message or 'Ошибка ожидания соединения от ОАСУ')


# Ошибка авторизации на ОАСУ
class OasuAuthError(OasuError):

    def __init__(self, message=None):
        super(OasuAuthError, self).__init__(message or 'Ошибка авторизации на ОАСУ')
