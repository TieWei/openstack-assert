from os import environ

from clients import keystone as ks_client
from clients import neutron as neutron_client
from resource import Resource
from resource import detectable
from resource import validatable

class Openstack(Resource):

    def __init__(self):
        super(Openstack,self).__init__()

    @detectable
    def tenant_name(self):
        return environ.get('OS_TENANT_NAME')

    @detectable
    def username(self):
        return environ.get('OS_USERNAME')

    @detectable
    def password(self):
        return environ.get('OS_PASSWORD')

    @detectable
    def auth_url(self):
        return environ.get('OS_AUTH_URL')


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
        



