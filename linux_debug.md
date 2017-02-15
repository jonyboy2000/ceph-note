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
vncconfig -nowin&
```
