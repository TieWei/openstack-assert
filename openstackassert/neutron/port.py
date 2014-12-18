from resource import Resource
from resource import detectable
from resource import validatable
import re

class Port(Resource):

    def __init__(self, uuid, details=None):
        self._id = uuid
        super(Port,self).__init__(details)

    def id(self):
        return self._id

    def _fetch_api(self):
        try:
            port = self._neutron.show_port(self._id).get('port')
            self._details = port
        except NeutronClientException as e:
            status_code = getattr(e,'status_code', 0)
            if status_code == 404:
                self.info = {}
            else:
                logging.exception(e.message)
                raise e

    def _fetch_binding(self):
        if self._details and isinstance(self._details, dict) and \
            'binding' not in self._details:
            binding = {}
            for key, value in self._details.iteritems():
                match = re.match('binding:(\w+)', key)
                if match:
                    binding[match.group(1)] = value
                else:
                    continue
            self._details['binding'] = binding
        else:
            self._fetch_api()
            self._fetch_binding()

    @detectable
    def status(self):
        return self._return_or_fetch(self._fetch_api, "status")

    @detectable
    def binding(self):
        return self._return_or_fetch(self._fetch_binding, "binding")

    @detectable
    def name(self):
        return self._return_or_fetch(self._fetch_api, "name")

    @detectable
    def allowed_address_pairs(self):
        return self._return_or_fetch(self._fetch_api, "allowed_address_pairs")

    @detectable
    def admin_state_up(self):
        return self._return_or_fetch(self._fetch_api, "admin_state_up")

    @detectable
    def network_id(self):
        return self._return_or_fetch(self._fetch_api, "network_id")

    @detectable
    def tenant_id(self):
        return self._return_or_fetch(self._fetch_api, "tenant_id")

    @detectable
    def extra_dhcp_opts(self):
        return self._return_or_fetch(self._fetch_api, "extra_dhcp_opts")

    @detectable
    def device_owner(self):
        return self._return_or_fetch(self._fetch_api, "device_owner")

    @detectable
    def device_id(self):
        return self._return_or_fetch(self._fetch_api, "device_id")

    @detectable
    def mac_address(self):
        return self._return_or_fetch(self._fetch_api, "mac_address")

    @detectable
    def fixed_ips(self):
        return self._return_or_fetch(self._fetch_api, "fixed_ips")

    @detectable
    def security_groups(self):
        return self._return_or_fetch(self._fetch_api, "security_groups")

    @validatable
    def ovs_port(self):
        pass


    @validatable
    def port_in_ns(self):
        pass