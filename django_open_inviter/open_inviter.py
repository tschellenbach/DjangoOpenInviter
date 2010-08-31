'''
Django Open Inviter
Allows users of django and python to access the open inviter system
OpenInviter.net is a widely used contact importer
It allows you to import your contacts from a wide scala of email services and social networks

by:
thierryschellenbach at gmail.com
http://www.mellowmorning.com/

Attempts to port the undocumented open inviter API
to python :)

Understanding the php api

There are tons of files, but plugins/_hosted.plg.php
overwrites almost everything

Hosted API
- Post XML to http://hosted.openinviter.com/hosted/hosted.php
- <import><service>{{ service }}</service><user>{$user}</user><password>{$pass}</password></import>
- Authentication by private key, used to sign the xml with an md5 hash
- Supported services are requested and cached every now and then

TODO
- cant get hosted services lookup to work (services function)
- contacts and services for a function name is ugly... import_contacts might be beter

'''

import hashlib
import httplib
import zlib
from django.core.exceptions import ImproperlyConfigured
from exceptions import LoginFailed, InvalidService, OpenInviterException
from app_settings import USERNAME, PRIVATE_KEY




class OpenInviter(object):
    '''
    Example usage:

    inviter = OpenInviter()
    contacts = inviter.contacts(email, password)
    '''
    _services = None

    def __init__(self,
                 api_domain='hosted.openinviter.com:80',
                 api_path='/hosted/hosted.php',
                 services_api_path='/hosted/services.php',
                 request_format='<import>' \
                                '<service>%(service)s</service>' \
                                '<user>%(user)s</user>' \
                                '<password>%(password)s</password>' \
                                '</import>'):
        self.api_domain = api_domain
        self.api_path = api_path
        self.services_api_path = services_api_path
        self.request_format = request_format
        self.api = self.api_domain + self.api_path

        # Not sure if this is the right place to check or we raise the
        # correct exception. But it beats sending a request with empty
        # credentials just to fail.
        if not USERNAME or not PRIVATE_KEY:
            raise ImproperlyConfigured('You must set OpenInviter ' \
                                       'credentials in order to use the API.')

    def contacts(self, email, password):
        '''
        Logs the user in
        Test:
        >>> o = OpenInviter()
        >>> o.contacts('example@example.com', 'test')
        dunno yet

        response
        error
        contacts
        - contact
        - - email
        - - name
        '''
        self.password = password
        self.email = email
        service = self._email_to_service(email)
        xml = self._format_request(service, email, password)
        signature = self._sign(xml)
        gzipped_xml = self._compress_xml(xml)
        parsed_data = self._request(self.api_path, signature, gzipped_xml)
        contact_list = self._xml_contacts_to_dict(parsed_data)

        return contact_list

    def services(self):
        '''
        Requests which hosted services are available at open importer
        >>> o = OpenInviter()
        >>> o.services()
        '''
        from django.core.cache import cache
        cache_key = 'open_inviter_services'
        services = getattr(self, '_services') or cache.get(cache_key)
        if not services:
            services = []
            signature = self._sign()
            data_decompressed = self._request(self.services_api_path, signature)

            cache.set(cache_key, services)
            self._services = services
        return services

    def _email_to_service(self, email):
        '''
        Converts thierrschellenbach@gmail.com to gmail
        its a guess for the service name
        would have preferred the service par not to be required
        '''
        domain = email.split('@')[1]
        service = domain.split('.')[0].lower()

        if service == 'live':
            service = 'hotmail'

        return service


    def _request(self, path, signature, params=None):
        '''
        Common request functionality for Services and Contacts

        - makes request
        - parses xml
        - handles errors
        '''
        headers = {'Content-type': 'application/xml','X_USER': USERNAME, 'X_SIGNATURE': signature}
        conn = httplib.HTTPConnection(self.api_domain)
        params_string = params or ''
        conn.request('POST', self.api_path, params_string, headers)
        response = conn.getresponse()
        data = response.read()
        data_decompressed = self._decompress_xml(data).decode('utf8')
        conn.close()
        parsed_data = self._parse_data(data_decompressed)

        if parsed_data.error != 'OK':
            self._handle_error(parsed_data.error)

        return parsed_data

    def _handle_error(self, error_message):
        from django.core.mail import mail_admins
        error_message = unicode(error_message)
        error_message_lower = error_message.lower()
        if 'login failed' in error_message_lower:
            exception_class = LoginFailed
        elif 'invalid service' in error_message_lower:
            exception_class = InvalidService
            error_message = 'This email provider is currently not support'
            mail_admins('invalid service','error message %s for email %s' % (error_message, self.email))
        else:
            exception_class = OpenInviterException
        raise exception_class(error_message)


    def _xml_contacts_to_dict(self, xmlnode):
        '''
        Takes our xml node and returns a nice format:

        [
        {'name': 'Thierry', 'emails': ['example@example.com', 'anotheremailhere.com']}
        {'name': 'Thierry', 'emails': ['example@example.com', 'anotheremailhere.com']}
        ]
        '''
        contacts = list(xmlnode.contacts.iterchildren())
        contact_list = []
        from collections import defaultdict
        user_accounts_dict = defaultdict(list)
        for contact in contacts:
            name = unicode(contact.name)
            email = unicode(contact.email)
            user_accounts_dict[name].append(email)

        for name, emails in user_accounts_dict.items():
            user_dict = dict(emails=emails, name=name)
            contact_list.append(user_dict)

        contact_list.sort(key=lambda x: x['name'])

        return contact_list


    def _format_request(self, service, user, password):
        '''
        Formats the xml command with the given parameters

        Test:
        >>> o = OpenInviter()
        >>> o._format_request('gmail', 'test', 'test')
        '<import><service>gmail</service><user>test</user><password>test</password></import>'
        '''
        formating_dict = locals()
        return self.request_format % formating_dict



    def _compress_xml(self, xml):
        return zlib.compress(xml, 9)

    def _decompress_xml(self, xml):
        return zlib.decompress(xml)

    def _parse_data(self, datastring):
        from lxml import objectify
        tree = objectify.fromstring(datastring)
        return tree

    def _sign(self, xml=None):
        '''
        Signs the xml with a double md5

        Based on this php example
        'X_SIGNATURE'=>md5(md5($this->settings['private_key']).$xml)
        'X_SIGNATURE'=>md5(md5($this->settings['private_key']).$this->settings['username'])
        '''
        private_key_hash = hashlib.md5(PRIVATE_KEY).hexdigest()
        if xml:
            additional_content = xml
        else:
            additional_content = USERNAME

        response_combined = private_key_hash + additional_content
        hash = hashlib.md5(response_combined).hexdigest()

        return hash



'''
    public function getHostedServices()
        {
        $path=$this->settings['cookie_path'].'/oi_hosted_services.txt';$services_cache=false;
        if (file_exists($path)) if (time()-filemtime($path)<=7200) $services_cache=true;
        if (!$services_cache)
            {
            if (!$this->init()) return array();
            $headers=array('X_USER'=>$this->settings['username'],'X_SIGNATURE'=>md5(md5($this->settings['private_key']).$this->settings['username']));
            $res=$this->post("http://hosted.openinviter.com/hosted/services.php",array(),false,false,false,$headers);
            if (empty($res)) { $this->internalError="Unable to connect to server.";return array(); }
            if (strpos($res,"ERROR: ")===0) { $this->internalError=substr($res,7);return array(); }
            file_put_contents($path,$res);
            }
        $plugins['email']=unserialize(file_get_contents($path));
        return $plugins;
        }
'''




if __name__ == '__main__':
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    import doctest
    doctest.testmod()
