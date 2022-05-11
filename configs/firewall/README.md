# Firewall notes
- [How to control internet access for each program?](https://askubuntu.com/questions/45072/how-to-control-internet-access-for-each-program)

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
