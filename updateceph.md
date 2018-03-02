```
for i in `rpm -qa|grep 10.2.10 | awk  -F"-10" '{print $1}'` ;do wget https://4.chacra.ceph.com/r/ceph/master/01fc18c447d5a0d6538f6b47af9c79a591c64ffb/centos/7/flavors/default/x86_64/$i-13.0.1-2409.g01fc18c.el7.x86_64.rpm;done
wget https://4.chacra.ceph.com/r/ceph/master/01fc18c447d5a0d6538f6b47af9c79a591c64ffb/centos/7/flavors/default/x86_64/python-rgw-13.0.1-2409.g01fc18c.el7.x86_64.rpm
wget https://4.chacra.ceph.com/r/ceph/master/01fc18c447d5a0d6538f6b47af9c79a591c64ffb/centos/7/flavors/default/x86_64/libcephfs2-13.0.1-2409.g01fc18c.el7.x86_64.rpm
yum localinstall *.rpm
```
