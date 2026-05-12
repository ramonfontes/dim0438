#!/usr/bin/env python

"""
A: 192.168.254.0/24
B: 200.90.50.0/24

h1 ---    --- s1 -(A)- r1 --- (B) --- h3
               |
h2-------------|

"""

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.term import makeTerm


def topology():
    "Create a network."
    net = Mininet_wifi()

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    r1 = net.addHost('r1')
    s1 = net.addSwitch('s1', failMode='standalone')

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(r1, s1)
    net.addLink(h3, r1)

    info("*** Starting network\n")
    net.build()
    s1.start([])

    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r1.cmd('iptables -t nat -A POSTROUTING -o r1-eth1 -j MASQUERADE')
    r1.cmd('iptables -A FORWARD -i r1-eth1 -o r1-eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT')
    r1.cmd('iptables -A FORWARD -i r1-eth0 -o r1-eth1 -j ACCEPT')

    r1.cmd("ifconfig r1-eth0 192.168.254.254/24")
    r1.cmd("ifconfig r1-eth1 200.90.50.49/24")

    h3.cmd("ifconfig h3-eth0 200.90.50.1/24")
    h3.cmd("route add default gw 200.90.50.49")

    h1.cmd("ifconfig h1-eth0 192.168.254.1/24")
    h2.cmd("ifconfig h2-eth0 192.168.254.2/24")

    h1.cmd("route add default gw 192.168.254.254")
    h2.cmd("route add default gw 192.168.254.254")

    makeTerm(h1, title='client1', cmd=f"bash -c 'sleep 10 && wget http://200.90.50.1:8000'")
    makeTerm(h2, title='client2', cmd=f"bash -c 'sleep 10 && wget http://200.90.50.1:8000'")
    makeTerm(h3, title='web server', cmd=f"bash -c 'python3 -m http.server'")
    makeTerm(r1, title='nat', cmd=f"bash -c 'watch -n 1 \"conntrack -L -n\"'")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
