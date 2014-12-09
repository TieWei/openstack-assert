from keystoneclient.v2_0 import client as keystone_client
from neutronclient.v2_0 import client as neutron_client


KEYSTONE = None
NEUTRON = None


def keystone(**kwargs):
    global KEYSTONE
    if not KEYSTONE:
        KEYSTONE = keystone_client.Client(**kwargs)
    return KEYSTONE

def neutron(**kwargs):
    global NEUTRON
    if not NEUTRON:
        NEUTRON = neutron_client.Client(**kwargs)
    return NEUTRON
