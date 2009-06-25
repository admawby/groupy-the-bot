# -*- coding: utf-8 -*-
# groupy.models

from google.appengine.ext import db
from kay.auth.models import GoogleUser
from kay.i18n import lazy_gettext as _

import babel

# Create your models here.

languages = sorted(babel.localedata.load('en')['languages'].keys())

class GroupyUser(GoogleUser):
  """
  """
  pass


class Group(db.Model):
  # key_name = name
  name = db.StringProperty(required=True, verbose_name=_("group name"))
  language = db.StringProperty(verbose_name=_("language"), default="en",
                               choices=languages)
  description = db.TextProperty(verbose_name=_("description"))
  owner = db.ReferenceProperty(GroupyUser, required=True)
  members = db.StringListProperty(verbose_name=_("members"))
  applications = db.StringListProperty(verbose_name=_("applications"))
  banned_addresses = db.StringListProperty(verbose_name=_("banned accounts"))
  updated = db.DateTimeProperty(auto_now=True)
  created = db.DateTimeProperty(auto_now_add=True)

  @classmethod
  def get_key_name(cls, name):
    return "g:%s" % name

  def is_owned_by(self, user):
    return self.owner.key() == user.key()
