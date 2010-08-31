

USERNAME = 'tschellenbach'
#Your api username, get one by registering at openinviter.com
PRIVATE_KEY = '7718ee5308615645b3724c56d9075f38'
#the private key, find it in your dashboard

EMAIL_INVALID_SERVICES = True
#IF true emails the admins in case a user goes for an invalid service

try:
    #have the option of overriding these
    #great for when im working on fashiolista 
    #and dont want to share this data with the rest of the world
    from local_settings import *
except ImportError, e:
    pass