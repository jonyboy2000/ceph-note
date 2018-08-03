
```
ceph auth get-or-create client.restapi osd 'allow *' mon 'allow rx' -o /etc/ceph/ceph.client.restapi.keyring

cat >> /etc/ceph/ceph.conf <<EOF
[client.restapi]
keyring = /etc/ceph/ceph.client.restapi.keyring
public addr = 127.0.0.1:5000
EOF

/usr/bin/ceph-rest-api --conf /etc/ceph/ceph.conf
```

nginx做前端

```
user root;
master_process off;
daemon off;
worker_processes  1;
events {
    worker_connections 1024;
}

http {
    server {
        listen 6066;
        location / {
            allow 10.254.3.76;
            allow 10.254.3.68;
            deny all;
            default_type text/html;
            proxy_pass http://127.0.0.1:5000;
        }
    }
}

```
