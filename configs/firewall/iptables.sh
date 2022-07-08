#!/bin/bash -
#===============================================================================
#         USAGE: ./iptables.sh 
#
#   DESCRIPTION: just some basic iptables config to make sure nothing happens 
#                outside of basic web traffic, SSH/ICMP to specific locations,
#                and packages managers working as normal
#
#      AUTHOR:    Jesse Hitch
#      CREATED:   07/07/2022 20:55:13
#      REVISION:  ---
#===============================================================================
IPT="sudo iptables"
# Server IP - that of localhost
SERVER_IP="$(ip addr show eno1 | grep 'inet ' | cut -f2 | awk '{ print $2}')"

# Remote IPs - IPs that remote hosts that want access to this machine
REMOTE_IPS=$1
SSH_PORT=$2

# Your DNS servers you use: cat /etc/resolv.conf
DNS_SERVER="$(cat /etc/resolv.conf | grep 192.168 | awk '{print $2}')"

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

echo "Allow connections to HTTPS and HTTP"
$IPT -A INPUT -p tcp --sport 443 -j ACCEPT
$IPT -A OUTPUT -p tcp -s $SERVER_IP --dport 443 -j ACCEPT
$IPT -A INPUT -p tcp --sport 80 -j ACCEPT
$IPT -A OUTPUT -p tcp -s $SERVER_IP --dport 80 -j ACCEPT

for ip in $PACKAGE_SERVER; do
	echo "Allow connection to '$ip' on port 21"
	$IPT -A OUTPUT -p tcp -d "$ip" --dport 21  -m state --state NEW,ESTABLISHED -j ACCEPT
	$IPT -A INPUT  -p tcp -s "$ip" --sport 21  -m state --state ESTABLISHED     -j ACCEPT
done

for remote_ip in $REMOTE_IPS; do
    echo "Allow outgoing/incoming connections to port 22 (SSH) for $remote_ip"
    $IPT -A OUTPUT -p tcp -d $remote_ip --dport 22 -j ACCEPT
    $IPT -A INPUT  -p tcp -s $remote_ip --sport 22 -j ACCEPT

    echo "Allow outgoing/incoming icmp connections (pings) for $remote_ip"
    $IPT -A OUTPUT -p icmp -d $remote_ip -j ACCEPT
    $IPT -A INPUT  -p icmp -s $remote_ip -j ACCEPT
done

#############################################################################################
# Global iptable rules. Not IP specific

echo "Allow outgoing connections to port 123 (ntp syncs)"
$IPT -A OUTPUT -p udp --dport 123 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPT -A INPUT  -p udp --sport 123 -m state --state ESTABLISHED     -j ACCEPT

# Log before dropping
$IPT -A INPUT  -j LOG  -m limit --limit 12/min --log-level 4 --log-prefix 'IP INPUT drop: '
$IPT -A INPUT  -j DROP

$IPT -A OUTPUT -j LOG  -m limit --limit 12/min --log-level 4 --log-prefix 'IP OUTPUT drop: '
$IPT -A OUTPUT -j DROP

exit 0
