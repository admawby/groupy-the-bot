# -*- coding: utf-8 -*-
# groupy.views

import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response, 
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest, Forbidden,
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

from models import Group
from forms import (
  AddGroupForm, EditGroupForm
)

# Create your views here.

@login_required
def index(request):
  groups = Group.all().filter("owner =", request.user).fetch(100)
  if len(groups) == 0:
    message = _("You don't own any group yet.")
  else:
    message = _("The groups you own.")
  return render_to_response('groupy/index.html',
                            {'message': message,
                             'groups': groups})

@login_required
def group_detail(request):
  if request.method == "GET":
    key_name = request.values.get("key_name", None)
    group = Group.get_by_key_name(key_name)
    if not group.is_owned_by(request.user):
      raise Forbidden()
    return render_to_response("groupy/group_detail.html",
                              {"message": _("The details of the group"),
                               "group": group})

def get_edit_form(group):
  return EditGroupForm(instance=group,
                       initial={'hidden_key_name': group.key().name(),
                                'hidden_updated': str(group.updated)})
  
@login_required
def edit_group(request):
  error_message = None
  if request.method == "GET":
    key_name = request.values.get("key_name", None)
    group = Group.get_by_key_name(key_name)
    if not group.is_owned_by(request.user):
      raise Forbidden()
    form = get_edit_form(group)

  elif request.method == "POST":
    key_name = request.form.get("hidden_key_name", None)
    group = Group.get_by_key_name(key_name)
    if not group.is_owned_by(request.user):
      raise Forbidden()
    form = get_edit_form(group)
    if form.validate(request.form):
      if str(group.updated) == form["hidden_updated"]:
        group.description = form["description"]
        group.members = form["members"]
        group.applications = form["applications"]
        group.banned_addresses = form["banned_addresses"]
        group.put()
        return redirect(url_for('groupy/group_detail',
                                key_name=group.key().name()))
      else:
        # re-init because of race condition
        form = get_edit_form(group)
        error_message = _("Sorry, It can not be saved because "
                          "a race condition happened. "
                          "Please try again from the start.")
    else:
      pass
  return render_to_response("groupy/edit_group.html",
                            {"message": _("Editing a group"),
                             "form": form.as_widget(),
                             "error_message": error_message,
                             "group": group})

@login_required
def add_group(request):
  form = AddGroupForm()
  if request.method == "POST":
    if form.validate(request.form):
      form['name']
      group = Group.get_or_insert(key_name=Group.get_key_name(form['name']),
                                  name=form['name'],
                                  description=unicode(form['description']),
                                  owner=request.user,
                                  members=form['members'])
      if group.owner.key() != request.user.key():
        form.errors.append("Group creation failed.")
      else:
        return redirect(url_for('groupy/group_detail',
                                key_name=group.key().name()))
    else:
      pass
  return render_to_response('groupy/edit_group.html',
                            {'form': form.as_widget(),
                             'message': _("Adding a new group")})
