
```
ceph auth get-or-create client.restapi osd 'allow *' mon 'allow rx' -o /etc/ceph/ceph.client.restapi.keyring

cat >> /etc/ceph/ceph.conf <<EOF
[client.restapi]
keyring = /etc/ceph/ceph.client.restapi.keyring
public addr = 127.0.0.1:6066
EOF

/usr/bin/ceph-rest-api --conf /etc/ceph/ceph.conf
```

nginx做前端
