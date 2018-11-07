
```
proxychains yum install http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/privoxy-3.0.26-1.el7.x86_64.rpm

forward-socks5   /               127.0.0.1:1080 .
listen-address 127.0.0.1:8119

privoxy --no-daemon /etc/privoxy/config
```





proxy
```

cat > ~/.gitconfig <<EOF
[http]
   proxy = socks5://127.0.0.1:1080
[https]
   proxy = socks5://127.0.0.1:1080
EOF

mkdir  ~/.pip/ && cat >>  ~/.pip/pip.conf <<EOF
[global]
proxy = http://127.0.0.1:8119
EOF

cat >> /etc/wgetrc <<EOF
http_proxy = http://127.0.0.1:8119
https_proxy = http://127.0.0.1:8119
EOF

cat > ~/.curlrc <<EOF
http_proxy=http://127.0.0.1:8119
https_proxy=http://127.0.0.1:8119
proxy = http://127.0.0.1:8119
EOF

cat >> /etc/yum.conf  <<EOF
proxy = http://127.0.0.1:8119
EOF


cmake
http_proxy=http://127.0.0.1:8119 https_proxy=http://127.0.0.1:8119 make cython_rados monmaptool ceph-mon ceph-osd radosgw radosgw-admin ceph-authtool ceph-conf crushtool monmaptool rados ceph-mgr -j4
```


