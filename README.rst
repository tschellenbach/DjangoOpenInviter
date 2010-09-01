DjangoOpenInviter
=================

Allows users of django and python to access the open inviter system.
`OpenInviter.com <http://openinviter.com/>`_ is a widely used contact
importer. It allows you to import your contacts from a wide scala of
email services and social networks.

by:
    thierryschellenbach at gmail.com

    http://www.mellowmorning.com/

Attempts to port the undocumented open inviter API to python :)


Understanding the PHP API
-------------------------

There are tons of files, but ``plugins/_hosted.plg.php`` overwrites almost
everything.


Hosted API
^^^^^^^^^^

- Post XML to http://hosted.openinviter.com/hosted/hosted.php.
- ::

    <import>
      <service>{{ service }}</service>
      <user>{$user}</user>
      <password>{$pass}</password>
    </import>

- Authentication by private key, used to sign the XML with an md5 hash.
- Supported services are requested and cached every now and then.


TODO
^^^^

- Can't get hosted services lookup to work (`services()` function)
- Contacts and services for a function name is ugly... import_contacts
  might be better
