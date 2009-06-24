from kay.utils import forms
from kay.utils.forms.modelform import ModelForm
from kay.i18n import lazy_gettext as _

from models import Group

class AddGroupForm(ModelForm):
  class Meta:
    model = Group
    exclude = ("owner", "applications", "banned_addresses", "updated",
               "created")
    help_texts = {"members": _("Input mail addresses separated by new lines."),
                  "name": _("Input the name of the group."),
                  "description": _("This description helps people to know "
                                   "this group better.")}

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
