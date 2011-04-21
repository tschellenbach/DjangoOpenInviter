from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from django_open_inviter.open_inviter import OpenInviter
from django_open_inviter.forms import FriendImportForm, FriendImportServiceForm

def index(request):
    oi = OpenInviter()
    services = oi.services()

    contacts = False

    if request.method == 'POST': # If the form has been submitted...
        form = FriendImportServiceForm(request.POST)
        #print form.contacts
        if form.is_valid():
            contacts = form.contacts
    else:
        form = FriendImportServiceForm()

    return render_to_response('index.html', {
        'services': services,
        'contacts': contacts,
        'form': form
    }, context_instance = RequestContext(request))
