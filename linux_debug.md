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

http://vasir.net/blog/ubuntu/replace_string_in_multiple_files
```
grep -rl yum openstack/ | xargs sed -i 's/yum/proxychains yum/g'
```


cat  /etc/systemd/system/vncserver@\:3.service
```
[Unit]
Description=Remote desktop service (VNC)
After=syslog.target network.target

[Service]
Type=forking
# Clean any existing files in /tmp/.X11-unix environment
ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill :3 > /dev/null 2>&1 || :'
ExecStart=/usr/sbin/runuser -l onest -c "/usr/bin/vncserver :3 -geometry 1680x1050"
PIDFile=/home/onest/.vnc/%H%i.pid
ExecStop=/bin/sh -c '/usr/bin/vncserver -kill :3 > /dev/null 2>&1 || :'

[Install]
WantedBy=multi-user.target

```

random 1.1GiB
```
openssl rand -out 1.1GiB.bin  -base64 $(( 2**30 * 3/4 ))
```
