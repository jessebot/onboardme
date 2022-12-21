# Wiregaurd TLDR for a client config

```bash
# generates a key. we care about this. this is something you care about.
wg genkey | wudo tee /etc/wireguard/private.key

# gives only root access (600) removes any perms except root
sudo chmod go= /etc/wireguard/private.key

# create a public key
sudo cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key
```

Edit your vpn.conf? the name is arbitrary? 🤷 most docs call it wg0.conf

```bash
# 🤷
sudo vim /etc/wireguard/home-internal.conf
```

In there we add:
- our address you we want on the VPN
- the private key on the client, the one we just created
- and the public key of the VPN server
- public IP address of the VPN server + port
- subnets you're allowed to use on the VPN (kinda like a mini firewall, like a security group on cloud)
- keepalive setting (timeout after a while)

The template is in our [smol vps config repo], under ansible :)


```bash
# if we want this a service to persist through reboot do:
sudo systemctl enable wg-quick@home-internal
```

```bash
# otherwise we want this
# this has created the virtual network device
sudo wg-quick up home-internal
```

Let's see our newly created network:

```bash
sudo wg
```

In there, you care about:

| thing                   | Description                              |
|-------------------------|------------------------------------------|
| interface home-internal | this is our interface we set up          |
| "latest handshake" | if it's not there, you're not connected. |

If "latest handshake" is not there, then the VPN server does not have your key. Contact your server admin.


# POV: server admin is you


```bash
# Add the user's `PublicKey` to your toml/ini style file and their allowed `AllowedIPs`
sudo vi /etc/wireguard/wg0.conf
```

The template is in our [smol vps config repo], under ansible, again :)

```bash
# restart the VPN for the changes to the config to take effect
wg-quick down wg0; wg-quick up wg0
```

SUCCESS 🎉
