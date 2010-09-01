import os
from distutils.core import setup
from django_open_inviter import __version__, __maintainer__, __email__


license_text = open('LICENSE.txt').read()
long_description = open('README.rst').read()


setup(
    name = 'DjangoOpenInviter',
    version = __version__,
    url = 'http://github.com/tschellenbach/DjangoOpenInviter',
    author = __maintainer__,
    author_email = __email__,
    license = license_text,
    packages = ['django_open_inviter'],
    data_files=[('', ['LICENSE.txt',
                      'README.rst'])],
    description = 'Python implementation of the client to openinviter.com - the leading online contact importing solution',
    long_description=long_description,
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content']
)
