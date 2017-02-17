```
journalctl -b -f -u  ceph-rest-api
```


```
[root@ceph13 ~]# ethtool bond4 |grep Speed
	Speed: 20000Mb/s
[root@ceph13 ~]# ethtool bond1 |grep Speed
	Speed: 1000Mb/s

```


```
yum groupinstall "GNOME Desktop"
yum install tigervnc-server -y
vncpasswd #设置密码
vncserver :1
vncserver -geometry 1920x1200   
vncserver -geometry 1680x1050  
vncconfig -nowin&
```

```
yum install privoxy
vim /etc/privoxy/config
systemctl start privoxy
forward-socks5   /               127.0.0.1:1080 .
listen-address 127.0.0.1:7777
```

```
[root@ceph13 devstack]# ip route add 10.128.3.0/24 via 10.142.50.254
```
