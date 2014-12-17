
def has_netns(netns):
    return 'test -f /var/run/netns/%s' % netns

def list_netns():
    return 'ip netns list'

def has_ovs_port(port):
    return 'ovs-vsctl port-to-br %s' % port

def list_ovs_ports(bridge=None):
    if bridge:
        return 'ovs-vsctl list-ports %s' % bridge
    else:
        return 'for br in $(ovs-vsctl list-br); do ovs-vsctl list-ports $br; done'


def _cmd_in_netns(netns, cmd):
    return "ip netns exec %(netns)s %(cmd)s" % dict(netns=netns, cmd=cmd)


def has_nic_in_netns(netns, nic):
    return _cmd_in_netns(netns=netns, cmd='test -d /sys/class/net/%s' % nic)


def list_nic_in_netns(netns):
    return _cmd_in_netns(netns=netns, cmd='ls -1 /sys/class/net/')

