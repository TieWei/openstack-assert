from os import environ

from clients import keystone as ks_client
from clients import neutron as neutron_client
from resource import Resource
from resource import detectable
from resource import validatable

class Openstack(Resource):

    def __init__(self, details=None):
        super(Openstack,self).__init__(details)

    def _fetch_env(self):
        self._details['tenant_name'] = environ.get('OS_TENANT_NAME')
        self._details['username'] = environ.get('OS_USERNAME')
        self._details['password'] = environ.get('OS_PASSWORD')
        self._details['auth_url'] = environ.get('OS_AUTH_URL')


    @detectable
    def tenant_name(self):
        return self._return_or_fetch(self._fetch_env, 'tenant_name')

    @detectable
    def username(self):
        return self._return_or_fetch(self._fetch_env, 'username')

    @detectable
    def password(self):
        return self._return_or_fetch(self._fetch_env, 'password')

    @detectable
    def auth_url(self):
        return self._return_or_fetch(self._fetch_env, 'auth_url')


    @validatable
    def keystone(self):
        keystone = ks_client(tenant_name=self._tenant_name,
                                username=self._username,
                                password=self._password,
                                auth_url=self._auth_url)
        return keystone


    @validatable
    def neutron(self):
        neutron = neutron_client(tenant_name=self._tenant_name,
                                    username=self._username,
                                    password=self._password,
                                    auth_url=self._auth_url)
        return neutron
        



