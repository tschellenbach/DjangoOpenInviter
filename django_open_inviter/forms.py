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
                               widget = forms.PasswordInput(render_value = False))

    def is_valid(self, *args, **kwargs):
        if not super(FriendImportForm, self).is_valid(*args, **kwargs):
            return False

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        # this check is used in the case that a manual selection of the service 
        # is possible in the form. See FriendImportServiceForm for an example
        service = False
        if 'service' in self.cleaned_data:
            service = self.cleaned_data['service']

        importer = OpenInviter()
        try:
            self.contacts = importer.contacts(email, password, service = service)
        except OpenInviterException, e:
            raise forms.ValidationError(e)
        except socket.timeout:
            if MAIL_ADMINS:
                mail_admins('OpenInviter Timeout',
                            'Connecting to email %s timed out.' % email)
            raise forms.ValidationError(_(u'Your email provider is currently not responding. Please try again later.'))

        return True


class FriendImportServiceForm(FriendImportForm):
    service = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(FriendImportServiceForm, self).__init__(*args, **kwargs)

        importer = OpenInviter()
        services = importer.services()

        self.fields['service'].choices = []
        for service in services:
            self.fields['service'].choices.append([service, service])
