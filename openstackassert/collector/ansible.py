import logging
import ansible.runner
import commands as cli
from excepton import AnsibleHostNotAccessable
from excepton import AnsibleBadReturnException

class AnsibleCollector(object):

    def __init__(self, *args, **kwargs):
        if 'timeout' in kwargs:
            self._timeout = kwargs['timeout']
        else:
            self._timeout = 5

    def _run(hosts, cmd, module='shell'):
        hosts = hosts if isinstance(hosts, list) else [hosts]
        results = ansible.runner.Runner(
            run_hosts=hosts,
            module_name=module, 
            module_args=cmd,
            timeout=self._timeout,
            forks=len(hosts)
        ).run()
        return results['contacted']

    def validate_netns(self, hosts, namespaces):
        if len(namespaces) == 1:
            cmd = cli.has_netns(namespaces[0])
        else:
            cmd = cli.list_netns()
        def verify_netns(host_data):
            if len(namespaces) == 1:
                return {namespaces[0]: host_data['rc'] == 0}
            else:
                all_ns = host_data['stdout'].split('\n')
                results = {}
                for ns in namespaces:
                    results[ns] = ns in all_ns
                return results

        return self._validate_via_shell(hosts, cmd, verify_netns)

    def validate_nic_in_netns(self, hosts, namespace, nics):
        if len(nics) == 1:
            cmd = cli.has_nic_in_netns(namespace, nics[0])
        else:
            cmd = cli.list_nic_in_netns(namespace)

        def verify_nic_in_netns(host_data):
            if len(nics) == 1:
                return {nics[0]: host_data['rc'] == 0}
            else:
                all_nic = host_data['stdout'].split('\n')
                results = {}
                for port in nics:
                    results[port] = port in all_nic
                return results
        
        return self._validate_via_shell(hosts, cmd, verify_nic_in_netns)


    def validate_ovs_ports(self, hosts, bridge, ports):
        if len(ports) == 1:
            cmd = cli.has_ovs_port(ports[0])
        else:
            cmd = cli.list_ovs_ports()

        def verify_ovs_ports(host_data):
            if host_data['rc'] == 0:
                if len(ports) == 1:
                    return {ports[0]: (details[host]['stdout'] == bridge)}
                else:
                    host_ports = host_data['stdout'].split('\n')
                    results = {}
                    for port in ports:
                      results[port] = (port in host_ports)
                    return results
            else:
                return {port : None for port in ports}
        
        return self._validate_via_shell(hosts, cmd, verify_ovs_ports)

    def validate_ovs_flow(self, host, ports):
        pass


    def _validate_via_shell(hosts, cmd, builder_func):
        return self._validate(hosts, cmd, self._shell_filter, builder_func)

    def _validate(hosts, cmd, filter_func, builder_func):
        details = self._run(hosts, cmd)
        results = {}
        for host in hosts:
            if host in details and filter_func(details[host]):
                results[host] = builder_func(results[host])
            else:       
                if host not in results:
                    excepton = AnsibleHostNotAccessable(host=host)
                else:
                    excepton = AnsibleBadReturnException(host=host, cmd=cmd)
                if config.stop:
                    raise excepton
                else:
                    logging.warning(excepton.message)
                    results[host] = None
        return results

    def _shell_filter(self, per_host_result):
        if'rc' in per_host_result and 'stdout' in per_host_result:
            return True
        else:
            return False

