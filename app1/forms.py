from django.contrib.admin import widgets
from django import forms


class lightForm(forms.Form):
    linetime = forms.DateTimeField(required=True,label='时间',widget=widgets.AdminDateWidget())

