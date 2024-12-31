# coti_assignment
Mininet for COTI assignment, please 4.0 PLS!

## Set-up
OS: [Ubuntu Desktop 24.04.01 LTS](https://ubuntu.com/download/desktop)
Configuration: Default Install (click next on everything, EXCEPT install the 3rd party dependencies and file formats)
VM Settings: 
- Memory: 8GB
- Processors: 4
- Hard Disk: 40GB 
- Network: NAT
- Everything else left default

## Installing Mininet
Mininet Version: 2.3.0

Following the [Mininet guide](http://mininet.org/download/) 'Option 3: Installation From Packages':
``` bash
sudo apt install mininet                # Use apt to install mininet
mn --version                            # Check that it shows 2.3.0
sudo mn --switch ovsbr --test pingall   # Test if all the switches are working
```

## Installing Docker
Followed the [guide](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) on 'Install using the apt repository'.

### Installing juice-shop Docker image
Only need to install the image once.
``` bash
sudo docker pull bkimminich/juice-shop
```

## Starting the Mininet
``` bash
sudo python3 retail_network.py
```
### Accessing the Web Server
Access the Web Server using Firefox at [http://localhost:3000](http://localhost:3000). The service will stop when mininet is exit.