# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os

DEFAULT_TIMEZONE = 'Asia/Tokyo'
DEBUG = True
PROFILE = False
SECRET_KEY = 'hogehoge'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SID'

ADD_APP_PREFIX_TO_KIND = False

ADMINS = (
  ['Takashi Matsuo', 'matsuo.takashi@gmail.com'],
)

TEMPLATE_DIRS = (
  'templates',
)

USE_I18N = True
DEFAULT_LANG = 'en'

INSTALLED_APPS = (
  'groupy',
)

MIDDLEWARE_CLASSES = (
  'kay.auth.middleware.GoogleAuthenticationMiddleware',
)

AUTH_USER_MODEL = 'groupy.models.GroupyUser'
