
```
yum -y install dnsmasq


grep  "^[^#;]" /etc/dnsmasq.conf

cat >  /etc/dnsmasq.conf << EOF
domain-needed
no-resolv
no-poll
listen-address=192.168.153.165
expand-hosts
local=/ecloud.today/
conf-dir=/etc/dnsmasq.d,.rpmnew,.rpmsave,.rpmorig
EOF

cat > /etc/dnsmasq.d/address.conf << EOF
address=/eos.ecloud.today/192.168.153.165
address=/.eos.ecloud.today/192.168.153.165
address=/eos-website.ecloud.today/192.168.153.165
address=/.eos-website.ecloud.today/192.168.153.165
EOF

systemctl restart dnsmasq

nslookup  eos.ecloud.today
```
