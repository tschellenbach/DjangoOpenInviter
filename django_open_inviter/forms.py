import socket
from django.core.mail import mail_admins
from django import forms
from django.utils.translation import ugettext_lazy as _
from app_settings import MAIL_ADMINS
from exceptions import OpenInviterException
from open_inviter import OpenInviter


class FriendImportForm(forms.Form):
    email = forms.EmailField(_(u'email'))
    password = forms.CharField(_(u'password'),
                               widget=forms.PasswordInput(render_value=False))

    def clean_email(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        importer = OpenInviter()
        try:
            self.contacts = importer.contacts(email, password)
        except OpenInviterException, e:
            raise forms.ValidationError(e)
        except socket.timeout:
            if MAIL_ADMINS:
                mail_admins('OpenInviter Timeout',
                            'Connecting to email %s timed out.' % email)
            raise forms.ValidationError(_(u'Your email provider is currently not responding. Please try again later.'))
        return email
