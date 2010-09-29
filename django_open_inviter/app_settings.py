from django.conf import settings


# OpenInviter credentials
USERNAME = getattr(settings, 'OPENINVITER_USERNAME', '')
PRIVATE_KEY = getattr(settings, 'OPENINVITER_PRIVATE_KEY', '')

# IF true emails the admins in case a user goes for an invalid service
MAIL_ADMINS = getattr(settings, 'OPENINVITER_MAIL_ADMINS', True)
