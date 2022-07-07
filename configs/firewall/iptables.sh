#!/bin/bash
IPT="sudo iptables"

# Remote IPs - IPs that remote hosts that want access to this machine
REMOTE_IPS="thing1 thing2"

# Server IP - that of localhost
SERVER_IP="$(ip addr show eth0 | grep 'inet ' | cut -f2 | awk '{ print $2}')"
eth_res=$?
if [ $eth_res -ne 0 ]; then
    SERVER_IP="$(ip addr show eno1 | grep 'inet ' | cut -f2 | awk '{ print $2}')"
fi

# Your DNS servers you use: cat /etc/resolv.conf
DNS_SERVER=$(cat /etc/resolv.conf | grep 192.168)

# Allow connections to this package servers
PACKAGE_SERVER="ftp.us.debian.org security.debian.org github.com"

echo "flush iptable rules"
$IPT -F
$IPT -X
$IPT -t nat -F
$IPT -t nat -X
$IPT -t mangle -F
$IPT -t mangle -X

echo "Set default policy to 'DROP'"
$IPT -P INPUT   DROP
$IPT -P FORWARD DROP
$IPT -P OUTPUT  DROP

## This should be one of the first rules.
## so dns lookups are already allowed for your other rules
for ip in $DNS_SERVER; do
	echo "Allowing DNS lookups (tcp, udp port 53, 5353) to server '$ip'"
	$IPT -A OUTPUT -p udp -d $ip --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
	$IPT -A INPUT  -p udp -s $ip --sport 53 -m state --state ESTABLISHED     -j ACCEPT
	$IPT -A OUTPUT -p tcp -d $ip --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
	$IPT -A INPUT  -p tcp -s $ip --sport 53 -m state --state ESTABLISHED     -j ACCEPT

    echo "Allowing the avahi daemon for DNS to run..."
	$IPT -A OUTPUT -p udp -d $ip --dport 5353 -m state --state NEW,ESTABLISHED -j ACCEPT
	$IPT -A INPUT  -p udp -s $ip --sport 5353 -m state --state ESTABLISHED     -j ACCEPT
	$IPT -A OUTPUT -p tcp -d $ip --dport 5353 -m state --state NEW,ESTABLISHED -j ACCEPT
	$IPT -A INPUT  -p tcp -s $ip --sport 5353 -m state --state ESTABLISHED     -j ACCEPT
done

echo "allow all and everything on localhost"
$IPT -A INPUT -i lo -j ACCEPT
$IPT -A OUTPUT -o lo -j ACCEPT

for ip in $PACKAGE_SERVER; do
	echo "Allow connection to '$ip' on port 21"
	$IPT -A OUTPUT -p tcp -d "$ip" --dport 21  -m state --state NEW,ESTABLISHED -j ACCEPT
	$IPT -A INPUT  -p tcp -s "$ip" --sport 21  -m state --state ESTABLISHED     -j ACCEPT
done

for remote_ip in $REMOTE_IPS; do
    echo "Allow outgoing/incoming connections to port 22 (SSH) for $remote_ip"
    $IPT -A OUTPUT -p tcp -d $remote_ip --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
    $IPT -A INPUT  -p tcp -s $remote_ip --sport 22 -m state --state ESTABLISHED     -j ACCEPT

    echo "Allow outgoing/incoming icmp connections (pings) for $remote_ip"
    $IPT -A OUTPUT -p icmp -d $remote_ip  -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
    $IPT -A INPUT  -p icmp -s $remote_ip  -m state --state ESTABLISHED,RELATED     -j ACCEPT
done

#######################################################################################################
## Global iptable rules. Not IP specific
$IPT -A INPUT -p tcp --sport 443 -j ACCEPT
$IPT -A OUTPUT -p tcp -s $SERVER_IP --dport 443 -j ACCEPT
$IPT -A INPUT -p tcp --sport 80 -j ACCEPT
$IPT -A OUTPUT -p tcp -s $SERVER_IP --dport 80 -j ACCEPT

echo "Allow outgoing connections to port 123 (ntp syncs)"
$IPT -A OUTPUT -p udp --dport 123 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPT -A INPUT  -p udp --sport 123 -m state --state ESTABLISHED     -j ACCEPT

# Log before dropping
$IPT -A INPUT  -j LOG  -m limit --limit 12/min --log-level 4 --log-prefix 'IP INPUT drop: '
$IPT -A INPUT  -j DROP

$IPT -A OUTPUT -j LOG  -m limit --limit 12/min --log-level 4 --log-prefix 'IP OUTPUT drop: '
$IPT -A OUTPUT -j DROP

exit 0
