import logging

from openstack import Openstack
from resource import Resource
from resource import detectable
from resource import validatable
from exception import ResourceNotReadyException
from neutronclient.common.exceptions import NeutronClientException

class Router(Resource):

    def __init__(self, uuid, details=None):
        self._id = uuid
        self._details = details if details else {}
        openstack = Openstack()
        if openstack.has_neutron():
            self._neutron = openstack.neutron()
        else:
            raise ResourceNotReadyException(resource="Router %s" % uuid,
                                            pre_resource="Openstack",
                                            pre_validate="neutron")
        super(Router,self).__init__()

    def id(self):
        return self._id

    def _fetch_base(self):
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

    def _fetch_hosts(self):
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

    def _fetch_ports(self):
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
        if 'name' not in self._details:
            self._fetch_base()
        return self._details.get("name", None)

    @detectable
    def admin_state_up(self):
        if 'admin_state_up' not in self._details:
            self._fetch_base()
        return self._details.get("admin_state_up", None)

    @detectable
    def status(self):
        if 'status' not in self._details:
            self._fetch_base()
        return self._details.get("status", None)

    @detectable
    def tenant_id(self):
        if 'tenant_id' not in self._details:
            self._fetch_base()
        return self._details.get("tenant_id", None)

    @detectable
    def external_gateway_info(self):
        if 'external_gateway_info' not in self._details:
            self._fetch_base()
        return self._details.get("external_gateway_info", None)

    @detectable
    def routes(self):
        if 'routes' not in self._details:
            self._fetch_base()
        return self._details.get("routes", None)

    @detectable
    def hosts(self):
        if 'hosts' not in self._details:
            self._fetch_hosts()
        return self._details.get("hosts", None)

    @detectable
    def ports(self):
        if 'ports' not in self._details:
            self._fetch_ports()
        return self._details.get("ports", None)

    @detectable
    def gateway(self):
        if 'ports' not in self._details:
            self._fetch_ports()
        for port in self._details['ports']:
            if port['device_owner'] == 'network:router_gateway':
               return port
        return None

    @detectable
    def interfaces(self):
        if 'ports' not in self._details:
            self._fetch_ports()
        return [ port for port in self._details['ports'] 
                if port['device_owner'] == 'network:router_interface']

    @validatable
    def namespace(self):
        namespace = "qrouter-%s" % self._uuid
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
