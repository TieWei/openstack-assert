import sys
from openstack import Openstack

def main():

    #testing codes
    openstack = Openstack()
    assert openstack.has_keystone()
    assert openstack.has_neutron()


if __name__ == '__main__':
    sys.exit(main())