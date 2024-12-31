from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.cli import CLI
from mininet.util import quietRun 

class RetailNetwork(Topo):
    def build(self):
        # Add switches
        firewall = self.addSwitch('s1')  # Firewall
        dmz = self.addSwitch('s2')  # DMZ
        internal = self.addSwitch('s3')  # Internal Zone

        # Add hosts
        attacker = self.addHost('h1', ip='10.0.0.1/24')  # Attacker Machine
        web_server = self.addHost('h2', ip='10.0.0.2/24')  # Web Server
        email_server = self.addHost('h3', ip='10.0.1.1/24')  # Email Server
        user_machine = self.addHost('h4', ip='10.0.1.2/24')  # User Machine
        siem = self.addHost('h5', ip='10.0.1.3/24')  # SIEM

        # Add links
        self.addLink(attacker, firewall)  # Attacker -> Firewall
        self.addLink(firewall, dmz)  # Firewall -> DMZ
        self.addLink(web_server, dmz)  # Web Server in DMZ
        self.addLink(email_server, dmz)  # Email Server in DMZ 
        self.addLink(firewall, internal)  # Firewall -> Internal Zone
        self.addLink(user_machine, internal)  # User Machine in Internal Zone
        self.addLink(siem, internal)  # SIEM in Internal Zone

    # Function to start the services in the Mininet host
    def startServices(self):
        None

def run():
    topo = RetailNetwork()
    net = Mininet(topo=topo)
    net.start()
    topo.startServices()
    CLI(net) # Open the Mininet CLI for interaction
    net.stop()

if __name__ == '__main__':
    run()
