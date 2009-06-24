"""Groupy robot"""

import logging
import re

from waveapi import events
from waveapi import model
from waveapi import robot

from kay.misc import get_appid

hostname = "%s.appspot.com" % get_appid()

class Command(object):
  def __init__(self, name, pattern, func):
    self.name = name
    self.pattern = pattern
    self.func = func
  def __call__(self, properties, context, user, **kwargs):
    return self.func(properties, context, user, **kwargs)

def add_request(properties, context, user, groupname=None):
  blip = context.GetBlipById(properties['blipId'])
  blip.CreateChild().GetDocument().SetText(
    "You(%s) requested adding you to the group: %s." % (user, groupname))


def group_list(properties, context, user, **kwargs):
  blip = context.GetBlipById(properties['blipId'])
  blip.CreateChild().GetDocument().SetText("You(%s) requested listing groups."
                                           % user)


def on_submitted(properties, context):
  """
  """
  commands = []
  commands.append(Command("add", r"^add me to (?P<groupname>[\w\-_]+)$",
                          add_request))
  commands.append(Command("list groups", r"^list groups$", group_list))
  blip = context.GetBlipById(properties['blipId'])
  user = blip.GetCreator()
  contributors = blip.GetContributors()
  logging.debug("user: %s" % user)
  logging.debug("contributors: %s" % str(contributors))
  if not len(contributors) == 1:
    blip.CreateChild().GetDocument().SetText(
      "I'm confusing about who said that. Sorry.")
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
      logging.debug(m.groupdict())
      command(properties, context, user, **m.groupdict())
      return
  blip.CreateChild().GetDocument().SetText(
    "I don't understand what you're saying. Sorry.")
  

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
