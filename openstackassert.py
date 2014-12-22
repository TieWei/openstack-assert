import sys
from openstackassert.openstack import Openstack
from openstackassert.neutron.router import Router

def main():
    uuid = "9b13234f-1cc9-4403-a58b-3110373821db"
    router = Router(uuid)
    openstack = Openstack()
    for router in openstack.neutron().list_routers().get('routers'):
        print "Checking Router %s" % router['id']
        router = Router(router['id'], router)  
        print "Name checking %s" %  router.has_namespace()
        print "NICs in namespace %s" % router.has_nics_in_netns()


if __name__ == '__main__':
    sys.exit(main())
