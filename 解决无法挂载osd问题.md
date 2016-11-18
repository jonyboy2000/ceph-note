```
[root@graphite ~]# ln -s /usr/lib/systemd/system/ceph-disk\@.service  /etc/systemd/system/ceph-osd.target.wants/ceph-disk@dev-sdb1.service
[root@graphite ~]# ln -s /usr/lib/systemd/system/ceph-disk\@.service  /etc/systemd/system/ceph-osd.target.wants/ceph-disk@dev-sdc1.service
[root@graphite ~]# ln -s /usr/lib/systemd/system/ceph-disk\@.service  /etc/systemd/system/ceph-osd.target.wants/ceph-disk@dev-sdd1.service
[root@graphite ~]# ln -s /usr/lib/systemd/system/ceph-disk\@.service  /etc/systemd/system/ceph-osd.target.wants/ceph-disk@dev-sde1.service
```
