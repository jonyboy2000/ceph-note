```
[7.3]
baseurl=http://mirror.centos.org/centos/7.3.1611/os/x86_64
gpgcheck=0

[7.3-update]
baseurl=http://mirror.centos.org/centos/7.3.1611/updates/x86_64
gpgcheck=0
```

```
yum install ceph-mon ceph-osd ceph-radosgw -y
```
