#!/usr/bin/env python

"""
A: 192.168.0.0/24
B: 192.168.1.0/30
C: 192.168.2.0/24
h1 --- (A) --- r1 --- (B) --- r2 --- (C) --- h2
"""

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology():
    "Create a network."
    net = Mininet_wifi()

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    r1 = net.addHost('r1')
    r2 = net.addHost('r2')

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    net.addLink(h1, r1)
    net.addLink(h2, r2)
    net.addLink(r1, r2)

    info("*** Starting network\n")
    net.build()

    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
