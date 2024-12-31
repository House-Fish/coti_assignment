from mininet.log import info

def start_juice_shop(host):
    """Start Juice Shop in a Docker container on the specified host."""
    info(f"*** Starting Juice Shop on {host.name}\n")
    host.cmd(f"docker run -d --name juice-shop-{host.name} -p 3000:3000 bkimminich/juice-shop")

def stop_juice_shop(host):
    """Stop and remove the Juice Shop Docker container."""
    info("*** Stopping and removing Juice Shop container\n")
    host.cmd(f"docker stop juice-shop-{host.name} && docker rm juice-shop-{host.name}")