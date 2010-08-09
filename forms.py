from django import forms
from django.forms.util import ValidationError
import socket
from django.core.mail import mail_admins


class FriendImportForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
    
    def clean_email(self):
        from django_open_inviter import exceptions as invite_exceptions
        from django_open_inviter.open_inviter import OpenInviter

        self.importer = OpenInviter()
        
        try:
            self.contacts = self.importer.contacts(self.data.get('email'), self.data.get('password'))
        except invite_exceptions.OpenInviterException, e:
            message = unicode(e.message)
            raise ValidationError(message)
        except socket.timeout:
            mail_admins('timeout', 'Connecting to email %s timed out' % self.data.get('email'))
            raise ValidationError('Your email provider is currently not responding. Please try again later.')

        
        return self.cleaned_data['email']
    
