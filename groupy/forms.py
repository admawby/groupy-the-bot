import re

from kay.utils import forms
from kay.utils.forms.modelform import ModelForm
from kay.utils.validators import ValidationError
from kay.i18n import lazy_gettext as _

import babel

from models import Group

name_pattern = re.compile(r'^[\w\-_]+$')

def construct_lang_choices(data):
  choices = []
  choices.append(('', '-----'))
  for key in sorted(data.keys()):
    val = data[key]
    choices.append((key, '%s: %s' % (key, val)))
  return choices

class I18nLanguageSelectMixin(object):
  def __init__(self, instance=None, initial=None):
    ModelForm.__init__(self, instance, initial)
    from kay.utils import local
    import babel
    languages = local.app.active_translations.locale.languages
    self.language.choices = construct_lang_choices(languages)

class AddGroupForm(I18nLanguageSelectMixin, ModelForm):
  class Meta:
    model = Group
    exclude = ("owner", "applications", "banned_addresses", "updated",
               "created")
    help_texts = {"members": _("Input mail addresses(wave account) separated "
                               "by new lines."),
                  "name": _("Input the name of the group."),
                  "language": _("Main language of this group."),
                  "description": _("This description helps people to know "
                                   "this group better.")}
  def validate_name(self, value):
    if not name_pattern.match(value):
      raise ValidationError("Name must have only alnum, -, _")
    

class EditGroupForm(I18nLanguageSelectMixin, ModelForm):
  hidden_key_name = forms.TextField(widget=forms.HiddenInput)
  hidden_updated = forms.TextField(widget=forms.HiddenInput)
  class Meta:
    model = Group
    exclude = ("name", "owner", "updated", "created")
    help_texts = {"members": _("Input mail addresses separated by new lines."),
                  "name": _("Input the name of the group."),
                  "language": _("Main language of this group."),
                  "applications": _("People who want to join this group."),
                  "banned_addresses": _("People who are banned from this "
                                        "group"),
                  "description": _("This description helps people to know "
                                   "this group better.")}
