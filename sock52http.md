
```
proxychains yum install http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/privoxy-3.0.26-1.el7.x86_64.rpm

forward-socks5   /               127.0.0.1:1080 .
listen-address 127.0.0.1:8119

privoxy --no-daemon /etc/privoxy/config
```
