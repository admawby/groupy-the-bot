"""Groupy robot"""

import logging
import re

from waveapi import events
from waveapi import model
from waveapi import robot

import kay
kay.setup()

from kay.misc import get_appid
from kay.conf import settings

from groupy.models import Group

hostname = "%s.appspot.com" % get_appid()

class Command(object):
  def __init__(self, name, pattern, func):
    self.name = name
    self.pattern = pattern
    self.func = func
  def __call__(self, properties, context, user, **kwargs):
    return self.func(properties, context, user, **kwargs)

def desc(properties, context, user, groupname=None):
  blip = context.GetBlipById(properties['blipId'])
  group = Group.get_by_key_name(Group.get_key_name(groupname))
  text = ("You(%s) requested the description of the group: %s.\n"
          % (user, groupname))
  if group:
    root_wavelet = context.GetRootWavelet()
    text += "Here are the description of the group: %s\n" % groupname
    text += "-------------------------------------------------\n"
    text += group.description
    text += "\n-------------------------------------------------\n"
  else:
    text += "However, there is no such group! Sorry."
  blip.CreateChild().GetDocument().SetText(text)

def invite_people(properties, context, user, groupname=None):
  blip = context.GetBlipById(properties['blipId'])
  group = Group.get_by_key_name(Group.get_key_name(groupname))
  text = ("You(%s) requested inviting people of the group: %s.\n"
          % (user, groupname))
  if group:
    root_wavelet = context.GetRootWavelet()
    current_participants = root_wavelet.GetParticipants()
    for member in group.members:
      if not member in current_participants:
        root_wavelet.AddParticipant(member)
    text += "Finished inviting all the people in the group: %s" % groupname
  else:
    text += "However, there is no such group! Sorry."
  blip.CreateChild().GetDocument().SetText(text)


def add_request(properties, context, user, groupname=None):
  blip = context.GetBlipById(properties['blipId'])
  group = Group.get_by_key_name(Group.get_key_name(groupname))
  text = "You(%s) requested adding you to the group: %s.\n" % (user, groupname)
  if group:
    if user in group.members:
      text += "You are already a member of the group: %s." % groupname
    elif user in group.applications:
      text += ("You have already applied to join the group: %s. "
               "Please wait for a moment." % groupname)
    elif user in group.banned_addresses:
      text += "You are banned from the group: %s." % groupname
    else:
      from google.appengine.api import mail
      from google.appengine.ext import db
      body = "%s has requested joining the group: %s.\n" % (user, groupname)
      body += "You can moderate this request on following URL:\n"
      body += "http://%s.appspot.com/edit_group?key_name=%s" \
          % (get_appid(), group.key().name().replace(":", "%3A"))
      mail.send_mail(sender=settings.ADMINS[0][1],
                     to=group.owner.email,
                     subject="Join request from %s has come" % user,
                     body=body)
      def txn():
        g = Group.get(group.key())
        g.applications.append(user)
        g.put()
      db.run_in_transaction(txn)
      text += "Request to join this group has been sent!"
  else:
    text += "However, there is no such group! Sorry."
  blip.CreateChild().GetDocument().SetText(text)


def group_list(properties, context, user, **kwargs):
  blip = context.GetBlipById(properties['blipId'])
  groups = Group.all().fetch(1000)
  text = "You(%s) requested listing groups.\n" % user
  for group in groups:
    text += "%s\n" % group.name
  blip.CreateChild().GetDocument().SetText(text)


def help(properties, context, user, **kwargs):
  blip = context.GetBlipById(properties['blipId'])
  text = "You(%s) requested help.\n" % user
  text += "Available commands:\n"
  text += "-----------------------------------------------------\n"
  text += "list groups\n"
  text += "    list available groups\n\n"
  text += "desc GROUPNAME\n"
  text += "    display the description of specified group\n\n"
  text += "add me to GROUPNAME\n"
  text += "    send a request for joining to the specified group\n\n"
  text += "invite people in GROUPNAME\n"
  text += "    invite all the people in the specified group\n"
  text += "-----------------------------------------------------\n"
  blip.CreateChild().GetDocument().SetText(text)  


def on_submitted(properties, context):
  """
  """
  commands = []
  commands.append(Command("add", r"^add me to (?P<groupname>[\w\-_]+)$",
                          add_request))
  commands.append(Command("invite",
                          r"^invite people in (?P<groupname>[\w\-_]+)$",
                          invite_people))
  commands.append(Command("desc", r"^desc (?P<groupname>[\w\-_]+)$",
                          desc))
  commands.append(Command("list groups", r"^list groups$", group_list))
  commands.append(Command("help", r"^[hH][eE][lL][pP]$", help))
  blip = context.GetBlipById(properties['blipId'])
  user = blip.GetCreator()
  contributors = blip.GetContributors()
  logging.debug("user: %s" % user)
  logging.debug("contributors: %s" % str(contributors))
  if not len(contributors) == 1:
    #blip.CreateChild().GetDocument().SetText(
    #  "I'm confusing about who said that. Sorry.")
    logging.debug("I'm confusing about who said that. Sorry.")
    return
  if not user == contributors.pop():
    blip.CreateChild().GetDocument().SetText(
      "Please say it by yourself. Sorry.")
    return
  words = blip.GetDocument().GetText()
  firstline = words.strip()
  for command in commands:
    pat = re.compile(command.pattern)
    m = pat.search(firstline)
    if m:
      logging.debug("groupdict: %s" % str(m.groupdict()))
      command(properties, context, user, **m.groupdict())
      return
  return
  #blip.CreateChild().GetDocument().SetText(
  #  "I don't understand what you're saying. Sorry.")
  

def on_self_added(properties, context):
  """Called when this robot is first added to the wave."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("I'm alive.")


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.DEBUG)
  dummy = robot.Robot('Groupy', '1.0',
                      image_url='http://%s/media/icon.png' % hostname,
                      profile_url='http://%s/_wave/robot/profile' % hostname)
  dummy.RegisterHandler(events.WAVELET_SELF_ADDED,
                        on_self_added)
  dummy.RegisterHandler(events.BLIP_SUBMITTED,
                        on_submitted)
  dummy.Run(debug=True)
