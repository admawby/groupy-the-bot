# -*- coding: utf-8 -*-

"""
Kay URL dispatch setting.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)

from groupy import urls as groupy_urls

def make_url():
  return Map([
    Submount('/', groupy_urls.make_rules())
  ])

all_views = {
}
all_views.update(groupy_urls.all_views)
