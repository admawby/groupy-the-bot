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
      Rule('/add_group', endpoint='add_group'),
      Rule('/edit_group', endpoint='edit_group'),
      Rule('/group_detail', endpoint='group_detail'),
    ]),
  ]

all_views = {
  'groupy/index': groupy.views.index,
  'groupy/add_group': groupy.views.add_group,
  'groupy/edit_group': groupy.views.edit_group,
  'groupy/group_detail': groupy.views.group_detail,
}
