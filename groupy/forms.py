import re

from kay.utils import forms
from kay.utils.forms.modelform import ModelForm
from kay.utils.validators import ValidationError
from kay.i18n import lazy_gettext as _

from models import Group

name_pattern = re.compile(r'^[\w\-_]+$')

class AddGroupForm(ModelForm):
  class Meta:
    model = Group
    exclude = ("owner", "applications", "banned_addresses", "updated",
               "created")
    help_texts = {"members": _("Input mail addresses separated by new lines."),
                  "name": _("Input the name of the group."),
                  "description": _("This description helps people to know "
                                   "this group better.")}
  def validate_name(self, value):
    if not name_pattern.match(value):
      raise ValidationError("Name must have only alnum, -, _")

class EditGroupForm(ModelForm):
  hidden_key_name = forms.TextField(widget=forms.HiddenInput)
  class Meta:
    model = Group
    exclude = ("name", "owner", "updated", "created")
    help_texts = {"members": _("Input mail addresses separated by new lines."),
                  "name": _("Input the name of the group."),
                  "applications": _("People who want to join this group."),
                  "banned_addresses": _("People who are banned from this "
                                        "group"),
                  "description": _("This description helps people to know "
                                   "this group better.")}
  def validate_name(self, value):
    if not name_pattern.match(value):
      raise ValidationError("Name must have only alnum, -, _")
