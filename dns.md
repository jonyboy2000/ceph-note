
```
yum -y install dnsmasq

cat >  /etc/dnsmasq.conf << EOF
server=8.8.8.8
resolv-file=/etc/resolv.dnsmasq.conf
strict-order
resolv-file=/etc/dnsmasq.d/resolv.dnsmasq.conf
addn-hosts=/etc/dnsmasq.d/dnsmasq.hosts
address=/eos.ecloud.today/192.168.153.165
address=/*.eos.ecloud.today/192.168.153.165
address=/eos-website.ecloud.today/192.168.153.165
address=/*.eos-website.ecloud.today/192.168.153.165
EOF


start 
systemctl start dnsmasq

edit
/etc/resolv.conf
nameserver 127.0.0.1



test
nslookup  eos.ecloud.today
nslookup  www.baidu.com
```
