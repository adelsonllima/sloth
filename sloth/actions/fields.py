from django import forms
from . import inputs


class QrCodeField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update(widget=inputs.QrCodeInput())
        super().__init__(*args, **kwargs)


class ModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        if 'username_lookup' in kwargs:
            self.username_lookup = kwargs.pop('username_lookup')
        super().__init__(*args, **kwargs)


class TextField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update(widget=forms.Textarea())
        super().__init__(*args, **kwargs)


class CurrentUserField(forms.ModelChoiceField):
    def __init__(self, **kwargs):
        from django.contrib.auth.models import User
        kwargs['username_lookup'] = 'username'
        super().__init__(User.objects, **kwargs)
