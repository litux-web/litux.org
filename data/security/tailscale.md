type: article
title: Tailscale VPN
last-updated: 2023-02-10

[Tailscale](https://tailscale.com) is a service that provides secure remote access to shared resources by using the [WireGuard](https://www.wireguard.com) VPN protocol and providing applications for all relevant operating systems and devices.

The Tailscale free plan allows for up to three users and up to a hundred devices, which is more than enough for personal usage.

With Tailscale we can seamlessly and securely access resources like our home network or personal server network from our devices without the need for any iteration after the setup. For example, if we have an `SSH` or Remote Desktop session open, and move to a different network (even after going into standby for many minutes), the sessions will remain active.

With Tailscale we can also set up instances to become exit nodes and use those nodes on our devices.


## Tailscale installation on Ubuntu
From [Setting up Tailscale on Ubuntu 22.04](https://tailscale.com/kb/1187/install-ubuntu-2204/)
```
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt-get update
sudo apt-get install tailscale
```

## Starting and approving the instance
```
sudo tailscale up
```
This will show a link to open on the browser where we can approve the instance.

In the case of advertising routes or an exit node, we also need to approve those on the [Admin Console](https://login.tailscale.com/admin/machines).


## Getting access to the local network
```
sudo tailscale up --advertise-routes=192.168.0.0/16,10.0.0.0/8
```

## Setting up Exit Node on Ubuntu
From [Subnet routers and traffic relay nodes](https://tailscale.com/kb/1019/subnets/?tab=linux#enable-ip-forwarding) and [Exit Nodes (route all traffic)](https://tailscale.com/kb/1103/exit-nodes/)
```
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

sudo tailscale up --advertise-exit-node
sudo tailscale up --advertise-routes=192.168.0.0/16,10.0.0.0/8 --advertise-exit-node
```

