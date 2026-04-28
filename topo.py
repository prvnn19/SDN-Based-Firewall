#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def run_topo():
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)
    
    info('*** Adding POX Controller\n')
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    
    info('*** Adding Hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    
    info('*** Adding Switch\n')
    s1 = net.addSwitch('s1')
    
    info('*** Creating Links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    
    info('*** Starting Network\n')
    net.build()
    c0.start()
    s1.start([c0])
    
    info('*** Starting Mininet CLI\n')
    CLI(net)
    
    info('*** Stopping Network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_topo()