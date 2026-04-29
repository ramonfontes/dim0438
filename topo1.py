#!/usr/bin/env python

"""O nó r1 é um roteador. Configure a 1a interface do 
roteador em uma subrede de classe B que permita apenas a alocação de 2 hosts
e a segunda subrede deve ser de classe C e deve possibilitar a alocação de 11 hosts"""

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

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    net.addLink(h1, r1)
    net.addLink(r1, h2)

    info("*** Starting network\n")
    net.build()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
