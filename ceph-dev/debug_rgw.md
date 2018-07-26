# 由于主要关注rgw端，因此在rados直接使用rpm安装,ceph-radosgw模块编译调试

## (L) (Master) branch ceph
```
单机启动2个集群
CEPH_NUM_OSD=1 CEPH_NUM_MON=1 CEPH_NUM_MGR=1  CEPH_NUM_MDS=0 CEPH_NUM_RGW=1 VSTART_DEST=cluster1  ../src/vstart.sh --debug --new -x --localhost --without-dashboard --filestore
CEPH_NUM_OSD=1 CEPH_NUM_MON=1 CEPH_NUM_MGR=1  CEPH_NUM_MDS=0 CEPH_NUM_RGW=1 VSTART_DEST=cluster2  ../src/vstart.sh --debug --new -x --localhost --without-dashboard --filestore

```
```
#restart rgw
./bin/radosgw -f  -c /etc/ceph/ceph.conf --cluster ceph \
--name client.rgw.rgw1 --setuser ceph --setgroup ceph  \
--keyring /etc/ceph/keyring  --logfile /var/log/ceph-rgw.debug \
--debug-rgw 10/10  -m 192.168.153.156:6789
```

## L rpm vstart 启动rpm安装的单机集群
```
wget https://gist.githubusercontent.com/joke-lee/fc85c7eeff129dcb06baca4f2cdefd41/raw/0b4a4b2a453421a965d221acc6489eec330d2762/vstart-l-rpm.sh -O vstart.sh

# yum install ceph-mon ceph-osd ceph-radosgw ceph-mgr
#单机一个集群
CEPH_BUILD_ROOT=/usr CEPH_NUM_OSD=1 ./vstart.sh -n --mon_num 1 --osd_num 4 --mds_num 0 --mgr_num 1 --rgw_num 1

#单机多个集群
mkdir ceph1 && cp vstart.sh ceph1/ && cd ceph1
CEPH_BUILD_ROOT=/usr CEPH_PORT=6790 CEPH_NUM_OSD=1 ./vstart.sh -n --mon_num 1 --osd_num 1 --mds_num 0 --mgr_num 1 --rgw_num 1 --rgw_port 8001
mkdir ceph2 && cp vstart.sh ceph2/ && cd ceph2
CEPH_BUILD_ROOT=/usr CEPH_PORT=6890 CEPH_NUM_OSD=1 ./vstart.sh -n --mon_num 1 --osd_num 1 --mds_num 0 --mgr_num 1 --rgw_num 1 --rgw_port 8002
```

# jewel rpm vstart 启动rpm安装的单机集群


```
wget https://gist.githubusercontent.com/joke-lee/fc85c7eeff129dcb06baca4f2cdefd41/raw/ac2693df6dfc13517e5afe373b49581d28c6c8d0/vstart-j-rpm.sh -O vstart.sh 
yum install ceph-mon ceph-osd ceph-radosgw
mkdir /tmp/run/ceph1 && cd  /tmp/run/ceph1
#上传vstart.sh stop.sh 脚本到/tmp/run/ceph1 /tmp/run/ceph2
CEPH_RGW_PORT=8080 CEPH_BUILD_ROOT=/usr CEPH_PORT=6790 ./vstart.sh -n --mon_num 1 --mds_num 0 --short -r -X -i 127.0.0.1
mkdir /tmp/run/ceph2 && cd  /tmp/run/ceph2
CEPH_RGW_PORT=8080 CEPH_BUILD_ROOT=/usr CEPH_PORT=6890 ./vstart.sh -n --mon_num 1 --mds_num 0 --short -r -X -i 127.0.0.1
```

# jewel版本vstart启动(非rpm安装)
```
#单个集群
CEPH_RGW_PORT=80 CEPH_PORT=6790 CEPH_NUM_MON=1 ./vstart.sh -n --mon_num 1 --osd_num 1 --mds_num 0 --short -r -X -i 127.0.0.1
#多集群
VSTART_DEST=/root/ceph/src/ceph1  CEPH_RGW_PORT=80  CEPH_PORT=6790 CEPH_NUM_MON=1 ./vstart.sh -n --mon_num 1 --osd_num 1 --mds_num 0 --short -r -X -i 127.0.0.1
VSTART_DEST=/root/ceph/src/ceph2  CEPH_RGW_PORT=8081  CEPH_PORT=6791 CEPH_NUM_MON=1 ./vstart.sh -n --mon_num 1 --osd_num 1 --mds_num 0 --short -r -X -i 127.0.0.1
```
