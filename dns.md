
```
yum -y install dnsmasq

cat >  /etc/dnsmasq.conf << EOF
resolv-file=/etc/resolv.dnsmasq.conf
strict-order
resolv-file=/etc/dnsmasq.d/resolv.dnsmasq.conf
addn-hosts=/etc/dnsmasq.d/dnsmasq.hosts
address=/eos.ecloud.today/192.168.153.165
address=/*.eos.ecloud.today/192.168.153.165
address=/eos-website.ecloud.today/192.168.153.165
address=/*.eos-website.ecloud.today/192.168.153.165
EOF

systemctl restart dnsmasq

nslookup  eos.ecloud.today
```
