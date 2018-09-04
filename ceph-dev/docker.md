

# install docker on centos7
```
get docker rpm from https://drive.google.com/file/d/1azZa614qTHJG3qJQQH_s5p8a4CTGFnJo/view?usp=sharing


yum localinstall docker-1.10.3-46.el7.centos.14.x86_64.rpm docker-common-1.10.3-46.el7.centos.14.x86_64.rpm docker-selinux-1.10.3-46.el7.centos.14.x86_64.rpm  oci-register-machine-0-1.8.gitaf6c129.el7.x86_64.rpm oci-systemd-hook-0.1.4-5.git41491a3.el7.x86_64.rpm  policycoreutils-python-2.5-22.el7.x86_64.rpm  audit-libs-python-2.8.1-3.el7.x86_64.rpm  setools-libs-3.3.8-2.el7.x86_64.rpm libcgroup-0.41-15.el7.x86_64.rpm checkpolicy-2.5-6.el7.x86_64.rpm libsemanage-python-2.5-11.el7.x86_64.rpm  python-IPy-0.75-6.el7.noarch.rpm


configure proxy

https://github.com/wzyuliyang/ceph-note/blob/master/sock52http.md

/etc/sysconfig/docker

HTTP_PROXY="http://127.0.0.1:8119"
HTTPS_PROXY="http://127.0.0.1:8119"


cp ceph rpms to `pwd`/data
docker run -it -v `pwd`/data:/data  docker.io/centos  /bin/bash

cd /data
i=10.2.9-26 &&  cmd="yum localinstall ceph-mon-$i.el7.centos.x86_64.rpm ceph-osd-$i.el7.centos.x86_64.rpm ceph-radosgw-$i.el7.centos.x86_64.rpm  ceph-base-$i.el7.centos.x86_64.rpm ceph-common-$i.el7.centos.x86_64.rpm  ceph-selinux-$i.el7.centos.x86_64.rpm  libcephfs1-$i.el7.centos.x86_64.rpm  librados2-$i.el7.centos.x86_64.rpm librbd1-$i.el7.centos.x86_64.rpm  librgw2-$i.el7.centos.x86_64.rpm  libradosstriper1-$i.el7.centos.x86_64.rpm  python-rbd-$i.el7.centos.x86pm  python-rados-$i.el7.centos.x86_64.rpm  python-cephfs-$i.el7.centos.x86_64.rpm python-rbd-$i.el7.centos.x86_64.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/f/fcgi-2.4.0-25.el7.x86_64.rpm  http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/lttng-ust-2.4.1-4.el7.x86_64.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/leveldb-1.12.0-11.el7.x86_64.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/libbabeltrace-1.2.4-3.el7.x86_64.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/u/userspace-rcu-0.7.16-1.el7.x86_64.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-pecan-0.4.5-2.el7.noarch.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-simplegeneric-0.8-7.el7.noarch.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-singledispatch-3.4.0.2-2.el7.noarch.rpm" && eval $cmd

exit

docker ps -a # get the container id  cf3af49a47c8

docker commit cf3af49a47c8 onest-6.2.6
docker save onest-6.2.6 > onest-6.2.6_10.2.9-25.tar

# run container
mkdir `pwd`/clusetr1
docker run  -it -p 8080:8080 -v `pwd`/clusetr1:/ceph:rw  onest-6.2.6  /bin/bash

# in container 

cd /ceph
wget https://gist.githubusercontent.com/joke-lee/fc85c7eeff129dcb06baca4f2cdefd41/raw/ac2693df6dfc13517e5afe373b49581d28c6c8d0/vstart-j-rpm.sh -O vstart.sh
chmod +x vstart.sh
# run vstart
CEPH_RGW_PORT=8080 CEPH_BUILD_ROOT=/usr CEPH_PORT=6790 ./vstart.sh -n --mon_num 1 --mds_num 0 --short -r -X -i 127.0.0.1

CTRL+P and CTRL+Q #exit without shutdown container
```
