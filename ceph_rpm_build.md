# ceph编译rpm包

```
docker run --name=rpmbuild -i -v `pwd`/rpm:/ceph -t docker.io/centos  /bin/bash
sed -i "s/.el7/.el7.centos/g" /etc/rpm/macros.dist
```
