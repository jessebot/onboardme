# Firewall notes
Thing I read: [How to control internet access for each program?](https://askubuntu.com/questions/45072/how-to-control-internet-access-for-each-program)

## Iptables

Most of the firewalls on linux actually just wrap iptables anyway, so here's a bunch of quick how-tos. Remember that iptables requires sudo.

### Start, Stop, List
```bash
# only select one of the middle options
systemctl start/stop/restart iptables
```

List current rules:
```bash
sudo iptables -L -n -v
```

### Blocking and Allowing
Block an IP address:

```bash
sudo iptables -A INPUT -s xxx.xxx.xxx.xxx -j DROP
```

Unblock:
```bash
sudo iptables -D INPUT -s xxx.xxx.xxx.xxx -j DROP
```

Allow a specific port for a specific range of IPs or network. e.g. Allow outgoing connection on port 25 (mail) to network 192.160.5.0/24:

```bash
sudo iptables -A OUTPUT -p tcp -d 192.168.5.0/24 --dport 25 -j ACCEPT
```

Allow loopback (accessing from 127.0.0.1) with:
```bash
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
```

#### Block a social media website example

Find IP of facebook:
```bash
$ host facebook.com
facebook.com has address 31.13.80.36
facebook.com has IPv6 address 2a03:2880:f10e:83:face:b00c:0:25de
```

Find the used network range by facebook:
```bash
$ whois 31.13.80.36 | grep inetnum
inetnum:        31.13.64.0 - 31.13.127.255
```

Block the IP range of facebook:
```bash
sudo iptables -A OUTPUT -p tcp -d 31.13.64.0/18 -j DROP
```

### Logging

Keep logs of dropped packets on iptables, in `/var/log/messages`:
```bash
sudo iptables -A INPUT -i eth0 -j LOG --log-prefix "IPtables dropped packets:"
```

### Flush iptables firewall chains or rules

Flush your firewall chains:
```bash
sudo iptables -F
```

Flush chains from a specific table, example with the nat table:
```bash
sudo iptables -t nat -F
```

### Backup to a file/Restore from a file
```bash
# backup
iptables-save > ~/iptables.rules

# restore
iptables-restore < ~/iptables.rules
```

## UFW notes

Need to get `$remote_ip` at time of running if this is being set up as a secondary machine

```bash
ufw allow from $remote_ip to any port 22
```

This is to create special firewall configs for annoying apps want to phone home while they're supposed to be not running:

```bash
ufw app list
# move special app 
cp ufw/* /etc/ufw/applications.d
ufw app update discord
ufw app info discord
ufw deny discord
```

