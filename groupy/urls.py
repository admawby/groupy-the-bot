# -*- coding: utf-8 -*-
# groupy.urls

"""
Bellow is an easy example to mount this groupy application.

------------------------------------
from groupy import urls as groupy_urls

def make_url():
  return Map([
    Submount('/groupy', groupy_urls.make_rules())
  ])

all_views = {
}
all_views.update(groupy_urls.all_views)

------------------------------------

"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)
import groupy.views

def make_rules():
  return [
    EndpointPrefix('groupy/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'groupy/index': groupy.views.index,
}
