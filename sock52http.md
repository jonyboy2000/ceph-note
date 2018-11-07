
```
proxychains yum install http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/privoxy-3.0.26-1.el7.x86_64.rpm

forward-socks5   /               127.0.0.1:1080 .
listen-address 127.0.0.1:8119

privoxy --no-daemon /etc/privoxy/config
```


proxy
```
 ~/.gitconfig
[http]
        proxy = socks5://127.0.0.1:1080
[https]
        proxy = socks5://127.0.0.1:1080

~/.pip/pip.conf

[global]
proxy = http://127.0.0.1:8119

~/.wgetrc
use_proxy = on
http_proxy =  http://127.0.0.1:8119
https_proxy =  http://127.0.0.1:8119


~/.curlrc
http_proxy=http://127.0.0.1:8119
https_proxy=http://127.0.0.1:8119

/etc/yum.conf
proxy=http://127.0.0.1:8119
```
