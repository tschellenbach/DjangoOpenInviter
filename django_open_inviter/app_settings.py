from django.conf import settings


# OpenInviter credentials
USERNAME = settings.getattr('OPENINVITER_USERNAME', '')
PRIVATE_KEY = settings.getattr('OPENINVITER_PRIVATE_KEY', '')

# IF true emails the admins in case a user goes for an invalid service
EMAIL_INVALID_SERVICES = settings.getattr('OPENINVITER_EMAIL_INVALID_SERVICES',
                                                                          True)
