from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController, Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from web_server import start_juice_shop, stop_juice_shop

class RetailNetwork(Topo):
    def build(self):
        # Add switches
        info("*** Adding switches\n")
        firewall = self.addSwitch('s1')  # Firewall
        dmz = self.addSwitch('s2')  # DMZ
        internal = self.addSwitch('s3')  # Internal Zone

        # Add hosts
        info("*** Adding hosts\n")
        attacker = self.addHost('h1', ip='10.0.0.1/24')  # Attacker Machine
        web_server = self.addHost('h2', ip='10.0.0.2/24')  # Web Server
        email_server = self.addHost('h3', ip='10.0.0.3/24')  # Email Server
        user_machine = self.addHost('h4', ip='10.0.1.1/24')  # User Machine
        siem = self.addHost('h5', ip='10.0.1.2/24')  # SIEM

        # Add links
        info("*** Creating links\n")
        self.addLink(attacker, firewall)  # Attacker -> Firewall
        self.addLink(firewall, dmz)  # Firewall -> DMZ
        self.addLink(web_server, dmz)  # Web Server in DMZ
        self.addLink(email_server, dmz)  # Email Server in DMZ 
        self.addLink(firewall, internal)  # Firewall -> Internal Zone
        self.addLink(user_machine, internal)  # User Machine in Internal Zone
        self.addLink(siem, internal)  # SIEM in Internal Zone

    # Function to start the services in the Mininet host
    def startServices(self, net):
        info("*** Starting services\n")
        web_server = net.get('h1')
        start_juice_shop(web_server)

    def stopServices(self, net):
        info("*** Stopping services\n")
        web_server = net.get('h1')
        stop_juice_shop(web_server)

def run():
    topo = RetailNetwork()
    info("*** Starting network\n")
    net = Mininet(topo=topo, controller=OVSController)
    net.start()

    info("*** Testing connectivity\n")
    net.pingAll()

    topo.startServices(net=net)

    CLI(net) # Open the Mininet CLI for interaction

    topo.stopServices(net=net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
