from django.conf import settings


# OpenInviter accounts in the form of
# OPENINVITER_ACCOUNTS = [
    # ("account_name", "private_key"),
    # ("another_account_name", "another_private_key"),
# ]
ACCOUNTS = getattr(settings, 'OPENINVITER_ACCOUNTS', [])

# IF true emails the admins in case a user goes for an invalid service
MAIL_ADMINS = getattr(settings, 'OPENINVITER_MAIL_ADMINS', True)
