import sys
from openstack import Openstack
from neutron.router import Router

def main():
    uuid = "9b13234f-1cc9-4403-a58b-3110373821db"
    router = Router(uuid)
    assert router.has_nics_in_netns()
    assert router.has_namespace()


if __name__ == '__main__':
    sys.exit(main())