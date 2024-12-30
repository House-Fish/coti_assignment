from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.link import TCLink

def topo():
    net = Mininet(controller=Controller, link=TCLink, switch=OVSSwitch)

    # Add controller
    c0 = net.addController('c0')

    # Add switches
    firewall = net.addSwitch('s1')  # Firewall
    dmz = net.addSwitch('s2')  # DMZ
    internal = net.addSwitch('s3')  # Internal Zone

    # Add hosts
    attacker = net.addHost('h1', ip='10.0.0.1/24')  # Attacker Machine
    web_server = net.addHost('h2', ip='10.0.0.2/24')  # Web Server
    email_server = net.addHost('h3', ip='10.0.1.1/24')  # Email Server
    user_machine = net.addHost('h4', ip='10.0.1.2/24')  # User Machine
    siem = net.addHost('h5', ip='10.0.1.3/24')  # SIEM

    # Add links
    net.addLink(attacker, firewall)  # Attacker -> Firewall
    net.addLink(firewall, dmz)  # Firewall -> DMZ
    net.addLink(web_server, dmz)  # Web Server in DMZ
    net.addLink(firewall, internal)  # Firewall -> Internal Zone
    net.addLink(email_server, internal)  # Email Server in Internal Zone
    net.addLink(user_machine, internal)  # User Machine in Internal Zone
    net.addLink(siem, internal)  # SIEM in Internal Zone

    net.start()

    print("Firewall-based network topology is running!")
    print("Attacker Machine: 10.0.0.1")
    print("Web Server: 10.0.0.2")
    print("Email Server: 10.0.1.1")
    print("User Machine: 10.0.1.2")
    print("SIEM: 10.0.1.3")

    # Open CLI for interaction
    from mininet.cli import CLI
    CLI(net)

    net.stop()

if __name__ == '__main__':
    topo()
