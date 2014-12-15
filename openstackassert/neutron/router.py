import logging

from openstack import Openstack
from neutron.port import Port
from resource import Resource
from resource import detectable
from resource import validatable
from exception import ResourceNotReadyException
from neutronclient.common.exceptions import NeutronClientException

class Router(Resource):

    def __init__(self, uuid, details=None):
        self._id = uuid
        openstack = Openstack()
        if openstack.has_neutron():
            self._neutron = openstack.neutron()
        else:
            raise ResourceNotReadyException(resource="Router %s" % uuid,
                                            pre_resource="Openstack",
                                            pre_validate="neutron")
        super(Router,self).__init__(details)

    def id(self):
        return self._id

    def _fetch_api(self):
        try:
            router = self._neutron.show_router(self._id).get('router')
            self._details = router
        except NeutronClientException as e:
            status_code = getattr(e,'status_code', 0)
            if status_code == 404:
                self.info = {}
            else:
                logging.exception(e.message)
                raise e

    def _fetch_api_hosts(self):
        try:
            agents = self._neutron.list_l3_agent_hosting_routers(self._id)\
                                  .get('agents')
            for agent in agents:
                host = {}
                host['host'] = agent.get('host', None)
                host['agent_id'] = agent.get('id', None)
                if 'hosts' not in self._details:
                    self._details['hosts'] = []
                self._details['hosts'].append(host)
        except NeutronClientException as e:
            status_code = getattr(e,'status_code', 0)
            if status_code == 404:
                self.info = {}
            else:
                logging.exception(e.message)
                raise e

    def _fetch_api_ports(self):
        try:
            ports = self._neutron.list_ports(device_id=self._id).get('ports')
            self._details['ports'] = ports
        except NeutronClientException as e:
          status_code = getattr(e,'status_code', 0)
          if status_code == 404:
              self.info = {}
          else:
              logging.exception(e.message)
              raise e

    @detectable
    def name(self):
        return self._return_or_fetch(self._fetch_api, 'name')

    @detectable
    def admin_state_up(self):
        return self._return_or_fetch(self._fetch_api, 'admin_state_up')

    @detectable
    def status(self):
        return self._return_or_fetch(self._fetch_api, 'status')

    @detectable
    def tenant_id(self):
        return self._return_or_fetch(self._fetch_api, 'tenant_id')

    @detectable
    def external_gateway_info(self):
        return self._return_or_fetch(self._fetch_api, 'external_gateway_info')

    @detectable
    def routes(self):
        return self._return_or_fetch(self._fetch_api, 'routes')

    @detectable
    def hosts(self):
        return self._return_or_fetch(self._fetch_api_hosts, 'hosts')

    @detectable
    def ports(self):
        return self._return_or_fetch(self._fetch_api_ports, 'ports')

    @detectable
    def gateway(self):
        ports = self._return_or_fetch(self._fetch_api_ports, 'ports')
        for one_port in ports:
            if one_port['device_owner'] == 'network:router_gateway':
               return Port(one_port['id'], one_port)
        return None

    @detectable
    def interfaces(self):
        ports = self._return_or_fetch(self._fetch_api_ports, 'ports')
        return [ Port(one_port['id'], one_port) for one_port in ports 
                if one_port['device_owner'] == 'network:router_interface']

    @validatable
    def namespace(self):
        namespace = "qrouter-%s" % self._id
        pass

    @validatable
    def qr_devices(self):
        for nic in  self._interfaces:
            port = Port(nic['id'], nic)
            nic['assert'] = port.existed()
        return self._interfaces

    @validatable
    def qg_device(self):
        port = Port(self._gateway['id'], self._gateway)
        return port.existed()

    @validatable
    def ovs_flow(self):
        pass
