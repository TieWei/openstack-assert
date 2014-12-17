from keystoneclient.v2_0 import client as keystone_client
from neutronclient.v2_0 import client as neutron_client


_KEYSTONE = None
_NEUTRON = None


def keystone(**kwargs):
    global _KEYSTONE
    if not _KEYSTONE:
        _KEYSTONE = keystone_client.Client(**kwargs)
    return _KEYSTONE

def neutron(**kwargs):
    global _NEUTRON
    if not _NEUTRON:
        _NEUTRON = neutron_client.Client(**kwargs)
    return _NEUTRON
