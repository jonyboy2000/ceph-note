BIOS里关闭 secret boot
```

内核版本
[root@localhost ~]# uname -r
3.10.0-327.el7.x86_64

安装该版本对应的

yum install https://buildlogs.centos.org/c7.1511.00/kernel/20151119220809/3.10.0-327.el7.x86_64/kernel-3.10.0-327.el7.x86_64.rpm https://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/kernel-debug-devel-3.10.0-862.11.6.el7.x86_64.rpm http://debuginfo.centos.org/7/x86_64/kernel-debuginfo-3.10.0-327.el7.x86_64.rpm http://debuginfo.centos.org/7/x86_64/kernel-debuginfo-common-x86_64-3.10.0-327.el7.x86_64.rpm  https://buildlogs.centos.org/c7.1511.00/kernel/20151119220809/3.10.0-327.el7.x86_64/kernel-devel-3.10.0-327.el7.x86_64.rpm ftp://ftp.rediris.es/volumes/sites/centos.org/7.3.1611/updates/x86_64/Packages/kernel-headers-3.10.0-514.16.1.el7.x86_64.rpm https://buildlogs.centos.org/c7.1511.00/kernel/20151119220809/3.10.0-327.el7.x86_64/kernel-tools-3.10.0-327.el7.x86_64.rpm https://buildlogs.centos.org/c7.1511.00/kernel/20151119220809/3.10.0-327.el7.x86_64/kernel-tools-libs-3.10.0-327.el7.x86_64.rpm http://mirror.centos.org/centos/7/updates/x86_64/Packages/systemtap-3.2-8.el7_5.x86_64.rpm  https://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/systemtap-runtime-3.2-8.el7_5.x86_64.rpm http://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/systemtap-client-3.2-8.el7_5.x86_64.rpm ftp://ftp.pbone.net/mirror/ftp.scientificlinux.org/linux/scientific/7.4/x86_64/updates/fastbugs/systemtap-sdt-devel-3.1-5.el7_4.x86_64.rpm http://mirror.centos.org/centos/7/updates/x86_64/Packages/systemtap-devel-3.2-8.el7_5.x86_64.rpm

安装后查看
rpm -qa|grep kernel |sort
kernel-3.10.0-327.el7.x86_64
kernel-debug-devel-3.10.0-862.11.6.el7.x86_64
kernel-debuginfo-3.10.0-327.el7.x86_64
kernel-debuginfo-common-x86_64-3.10.0-327.el7.x86_64
kernel-devel-3.10.0-327.el7.x86_64
kernel-headers-3.10.0-514.16.1.el7.x86_64
kernel-tools-3.10.0-327.el7.x86_64
kernel-tools-libs-3.10.0-327.el7.x86_64

rpm -qa|grep systemtap
systemtap-3.2-8.el7_5.x86_64
systemtap-runtime-3.2-8.el7_5.x86_64
systemtap-client-3.2-8.el7_5.x86_64
systemtap-sdt-devel-3.1-5.el7_4.x86_64
systemtap-devel-3.2-8.el7_5.x86_64


内核版本
[root@lhdev1 ceph]# uname -r
3.10.0-862.14.4.el7.x86_64

安装该版本对应的
proxychains4 yum install http://mirror.centos.org/centos/7/updates/x86_64/Packages/kernel-3.10.0-862.14.4.el7.x86_64.rpm  https://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/kernel-debug-devel-3.10.0-862.14.4.el7.x86_64.rpm http://debuginfo.centos.org/7/x86_64/kernel-debuginfo-3.10.0-862.14.4.el7.x86_64.rpm http://debuginfo.centos.org/7/x86_64/kernel-debuginfo-common-x86_64-3.10.0-862.14.4.el7.x86_64.rpm https://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/kernel-devel-3.10.0-862.14.4.el7.x86_64.rpm https://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/kernel-headers-3.10.0-862.14.4.el7.x86_64.rpm https://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/kernel-tools-3.10.0-862.14.4.el7.x86_64.rpm https://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/kernel-tools-libs-3.10.0-862.14.4.el7.x86_64.rpm http://mirror.centos.org/centos/7/updates/x86_64/Packages/systemtap-3.2-8.el7_5.x86_64.rpm  https://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/systemtap-runtime-3.2-8.el7_5.x86_64.rpm http://rpmfind.net/linux/centos/7.5.1804/updates/x86_64/Packages/systemtap-client-3.2-8.el7_5.x86_64.rpm ftp://ftp.pbone.net/mirror/ftp.scientificlinux.org/linux/scientific/7.4/x86_64/updates/fastbugs/systemtap-sdt-devel-3.1-5.el7_4.x86_64.rpm http://mirror.centos.org/centos/7/updates/x86_64/Packages/systemtap-devel-3.2-8.el7_5.x86_64.rpm

安装后查看
rpm -qa|grep kernel |sort
kernel-3.10.0-862.14.4.el7.x86_64
kernel-debug-devel-3.10.0-862.14.4.el7.x86_64
kernel-debuginfo-3.10.0-862.14.4.el7.x86_64
kernel-debuginfo-common-x86_64-3.10.0-862.14.4.el7.x86_64
kernel-devel-3.10.0-862.14.4.el7.x86_64
kernel-headers-3.10.0-862.14.4.el7.x86_64
kernel-tools-3.10.0-862.14.4.el7.x86_64
kernel-tools-libs-3.10.0-862.14.4.el7.x86_64

rpm -qa|grep systemtap
systemtap-3.2-8.el7_5.x86_64
systemtap-client-3.2-8.el7_5.x86_64
systemtap-runtime-3.2-8.el7_5.x86_64
systemtap-devel-3.2-8.el7_5.x86_64
systemtap-sdt-devel-3.2-8.el7_5.x86_64

测试systemtap是否安装正确
stap -v -e 'probe vfs.read {printf("read performed\n"); exit()}'

输出以下表示正常
stap -v -e 'probe vfs.read {printf("read performed\n"); exit()}'
Pass 1: parsed user script and 479 library scripts using 243448virt/45036res/3372shr/41980data kb, in 470usr/60sys/540real ms.
Pass 2: analyzed script: 1 probe, 1 function, 7 embeds, 0 globals using 401972virt/199152res/4728shr/200504data kb, in 1690usr/720sys/2404real ms.
Pass 3: using cached /root/.systemtap/cache/7a/stap_7a515b8102e014d6cd6df10f285d8e5e_2721.c
Pass 4: using cached /root/.systemtap/cache/7a/stap_7a515b8102e014d6cd6df10f285d8e5e_2721.ko
Pass 5: starting run.
read performed
Pass 5: run completed in 10usr/40sys/363real ms.
```


测试s3fs
```
[root@localhost s3fs-fuse]# cat s3fs.stp
probe process("/usr/local/bin/s3fs").function("*@*s3fs.cpp*").call
{
  printf("%s\n", pp());
}

process("/usr/local/bin/s3fs").function("s3fs_getattr@/root/s3fs-fuse/src/s3fs.cpp:839").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("directory_empty@/root/s3fs-fuse/src/s3fs.cpp:1109").call
process("/usr/local/bin/s3fs").function("list_bucket@/root/s3fs-fuse/src/s3fs.cpp:2466").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml@/root/s3fs-fuse/src/s3fs.cpp:2676").call
process("/usr/local/bin/s3fs").function("get_prefix@/root/s3fs-fuse/src/s3fs.cpp:2763").call
process("/usr/local/bin/s3fs").function("get_base_exp@/root/s3fs-fuse/src/s3fs.cpp:2724").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml_ex@/root/s3fs-fuse/src/s3fs.cpp:2565").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml_ex@/root/s3fs-fuse/src/s3fs.cpp:2565").call
process("/usr/local/bin/s3fs").function("is_truncated@/root/s3fs-fuse/src/s3fs.cpp:2773").call
process("/usr/local/bin/s3fs").function("get_base_exp@/root/s3fs-fuse/src/s3fs.cpp:2724").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("s3fs_getattr@/root/s3fs-fuse/src/s3fs.cpp:839").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("s3fs_getattr@/root/s3fs-fuse/src/s3fs.cpp:839").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("directory_empty@/root/s3fs-fuse/src/s3fs.cpp:1109").call
process("/usr/local/bin/s3fs").function("list_bucket@/root/s3fs-fuse/src/s3fs.cpp:2466").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml@/root/s3fs-fuse/src/s3fs.cpp:2676").call
process("/usr/local/bin/s3fs").function("get_prefix@/root/s3fs-fuse/src/s3fs.cpp:2763").call
process("/usr/local/bin/s3fs").function("get_base_exp@/root/s3fs-fuse/src/s3fs.cpp:2724").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml_ex@/root/s3fs-fuse/src/s3fs.cpp:2565").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml_ex@/root/s3fs-fuse/src/s3fs.cpp:2565").call
process("/usr/local/bin/s3fs").function("is_truncated@/root/s3fs-fuse/src/s3fs.cpp:2773").call
process("/usr/local/bin/s3fs").function("get_base_exp@/root/s3fs-fuse/src/s3fs.cpp:2724").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("s3fs_open@/root/s3fs-fuse/src/s3fs.cpp:2059").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("s3fs_getattr@/root/s3fs-fuse/src/s3fs.cpp:839").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("directory_empty@/root/s3fs-fuse/src/s3fs.cpp:1109").call
process("/usr/local/bin/s3fs").function("list_bucket@/root/s3fs-fuse/src/s3fs.cpp:2466").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml@/root/s3fs-fuse/src/s3fs.cpp:2676").call
process("/usr/local/bin/s3fs").function("get_prefix@/root/s3fs-fuse/src/s3fs.cpp:2763").call
process("/usr/local/bin/s3fs").function("get_base_exp@/root/s3fs-fuse/src/s3fs.cpp:2724").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml_ex@/root/s3fs-fuse/src/s3fs.cpp:2565").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml_ex@/root/s3fs-fuse/src/s3fs.cpp:2565").call
process("/usr/local/bin/s3fs").function("is_truncated@/root/s3fs-fuse/src/s3fs.cpp:2773").call
process("/usr/local/bin/s3fs").function("get_base_exp@/root/s3fs-fuse/src/s3fs.cpp:2724").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("s3fs_create@/root/s3fs-fuse/src/s3fs.cpp:996").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("directory_empty@/root/s3fs-fuse/src/s3fs.cpp:1109").call
process("/usr/local/bin/s3fs").function("list_bucket@/root/s3fs-fuse/src/s3fs.cpp:2466").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml@/root/s3fs-fuse/src/s3fs.cpp:2676").call
process("/usr/local/bin/s3fs").function("get_prefix@/root/s3fs-fuse/src/s3fs.cpp:2763").call
process("/usr/local/bin/s3fs").function("get_base_exp@/root/s3fs-fuse/src/s3fs.cpp:2724").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml_ex@/root/s3fs-fuse/src/s3fs.cpp:2565").call
process("/usr/local/bin/s3fs").function("append_objects_from_xml_ex@/root/s3fs-fuse/src/s3fs.cpp:2565").call
process("/usr/local/bin/s3fs").function("is_truncated@/root/s3fs-fuse/src/s3fs.cpp:2773").call
process("/usr/local/bin/s3fs").function("get_base_exp@/root/s3fs-fuse/src/s3fs.cpp:2724").call
process("/usr/local/bin/s3fs").function("GetXmlNsUrl@/root/s3fs-fuse/src/s3fs.cpp:2645").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("create_file_object@/root/s3fs-fuse/src/s3fs.cpp:960").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("s3fs_getattr@/root/s3fs-fuse/src/s3fs.cpp:839").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("s3fs_read@/root/s3fs-fuse/src/s3fs.cpp:2119").call
process("/usr/local/bin/s3fs").function("get_object_sse_type@/root/s3fs-fuse/src/s3fs.cpp:735").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("s3fs_write@/root/s3fs-fuse/src/s3fs.cpp:2150").call
process("/usr/local/bin/s3fs").function("s3fs_getattr@/root/s3fs-fuse/src/s3fs.cpp:839").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("s3fs_flush@/root/s3fs-fuse/src/s3fs.cpp:2183").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("s3fs_release@/root/s3fs-fuse/src/s3fs.cpp:2238").call
process("/usr/local/bin/s3fs").function("s3fs_flush@/root/s3fs-fuse/src/s3fs.cpp:2183").call
process("/usr/local/bin/s3fs").function("check_parent_object_access@/root/s3fs-fuse/src/s3fs.cpp:695").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("check_object_access@/root/s3fs-fuse/src/s3fs.cpp:587").call
process("/usr/local/bin/s3fs").function("get_object_attribute@/root/s3fs-fuse/src/s3fs.cpp:435").call
process("/usr/local/bin/s3fs").function("s3fs_release@/root/s3fs-fuse/src/s3fs.cpp:2238").call
```


测试rgw_process.cc中函数的调用
```
cat rgw.stp 
probe process("/root/ceph/build/bin/radosgw").function("*@*rgw_process.cc*").call
{
  printf("%s\n", pp());
}

stap -x 1270 rgw.stp   #upload by s3cmd put 1.txt s3://test1
process("/root/ceph/build/bin/radosgw").function("process_request@/root/ceph/src/rgw/rgw_process.cc:121").call
process("/root/ceph/build/bin/radosgw").function("rgw_process_authenticated@/root/ceph/src/rgw/rgw_process.cc:37").call
```

测试多个文件的调用 rgw2.stp 
```
probe process("/root/ceph/build/bin/radosgw").function("*@*rgw_process.cc*").call
, process("/root/ceph/build/bin/radosgw").function("*@*rgw_op.cc*").call
, process("/root/ceph/build/bin/radosgw").function("*@*rgw_rest_*").call
{
  printf("%s\n", pp());
}
```

```
stap -x 1270 rgw2.stp  #1270为rgw进程号
process("/root/ceph/build/bin/radosgw").function("process_request@/root/ceph/src/rgw/rgw_process.cc:121").call
process("/root/ceph/build/bin/radosgw").function("looks_like_ip_address@/root/ceph/src/rgw/rgw_rest_s3.h:608").call
process("/root/ceph/build/bin/radosgw").function("get_handler@/root/ceph/src/rgw/rgw_rest_s3.cc:3479").call
process("/root/ceph/build/bin/radosgw").function("init_from_header@/root/ceph/src/rgw/rgw_rest_s3.cc:3213").call
process("/root/ceph/build/bin/radosgw").function("RGWHandler_REST_Obj_S3@/root/ceph/src/rgw/rgw_rest_s3.h:587").call
process("/root/ceph/build/bin/radosgw").function("RGWHandler_REST_S3@/root/ceph/src/rgw/rgw_rest_s3.h:506").call
process("/root/ceph/build/bin/radosgw").function("init@/root/ceph/src/rgw/rgw_rest_s3.cc:3349").call
process("/root/ceph/build/bin/radosgw").function("init@/root/ceph/src/rgw/rgw_op.cc:6983").call
process("/root/ceph/build/bin/radosgw").function("op_put@/root/ceph/src/rgw/rgw_rest_s3.cc:3170").call
process("/root/ceph/build/bin/radosgw").function("is_acl_op@/root/ceph/src/rgw/rgw_rest_s3.h:569").call
process("/root/ceph/build/bin/radosgw").function("is_tagging_op@/root/ceph/src/rgw/rgw_rest_s3.h:572").call
process("/root/ceph/build/bin/radosgw").function("RGWPutObj_ObjStore_S3@/root/ceph/src/rgw/rgw_rest_s3.h:209").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("authorize@/root/ceph/src/rgw/rgw_rest_s3.h:515").call
process("/root/ceph/build/bin/radosgw").function("authorize@/root/ceph/src/rgw/rgw_rest_s3.cc:3446").call
process("/root/ceph/build/bin/radosgw").function("is_applicable@/root/ceph/src/rgw/rgw_rest_s3.cc:4289").call
process("/root/ceph/build/bin/radosgw").function("discover_aws_flavour@/root/ceph/src/rgw/rgw_rest_s3.cc:3405").call
process("/root/ceph/build/bin/radosgw").function("authenticate@/root/ceph/src/rgw/rgw_rest_s3.cc:4116").call
process("/root/ceph/build/bin/radosgw").function("get_auth_data@/root/ceph/src/rgw/rgw_rest_s3.cc:3783").call
process("/root/ceph/build/bin/radosgw").function("discover_aws_flavour@/root/ceph/src/rgw/rgw_rest_s3.cc:3405").call
process("/root/ceph/build/bin/radosgw").function("get_auth_data_v2@/root/ceph/src/rgw/rgw_rest_s3.cc:3995").call
process("/root/ceph/build/bin/radosgw").function("authenticate@/root/ceph/src/rgw/rgw_rest_s3.cc:4237").call
process("/root/ceph/build/bin/radosgw").function("null_completer_factory@/root/ceph/src/rgw/rgw_rest_s3.cc:3776").call
process("/root/ceph/build/bin/radosgw").function("~auth_data_t@/root/ceph/src/rgw/rgw_rest_s3.h:720").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("postauth_init@/root/ceph/src/rgw/rgw_rest_s3.cc:3306").call
process("/root/ceph/build/bin/radosgw").function("valid_s3_bucket_name@/root/ceph/src/rgw/rgw_rest_s3.h:641").call
process("/root/ceph/build/bin/radosgw").function("looks_like_ip_address@/root/ceph/src/rgw/rgw_rest_s3.h:608").call
process("/root/ceph/build/bin/radosgw").function("rgw_process_authenticated@/root/ceph/src/rgw/rgw_process.cc:37").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("do_init_permissions@/root/ceph/src/rgw/rgw_op.cc:6993").call
process("/root/ceph/build/bin/radosgw").function("rgw_build_bucket_policies@/root/ceph/src/rgw/rgw_op.cc:395").call
process("/root/ceph/build/bin/radosgw").function("read_bucket_policy@/root/ceph/src/rgw/rgw_op.cc:308").call
process("/root/ceph/build/bin/radosgw").function("get_bucket_policy_from_attr@/root/ceph/src/rgw/rgw_op.cc:260").call
process("/root/ceph/build/bin/radosgw").function("get_bucket_instance_policy_from_attr@/root/ceph/src/rgw/rgw_op.cc:195").call
process("/root/ceph/build/bin/radosgw").function("decode_policy@/root/ceph/src/rgw/rgw_op.cc:156").call
process("/root/ceph/build/bin/radosgw").function("get_iam_policy_from_attr@/root/ceph/src/rgw/rgw_op.cc:269").call
process("/root/ceph/build/bin/radosgw").function("rgw_build_iam_environment@/root/ceph/src/rgw/rgw_op.cc:653").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("is_obj_update_op@/root/ceph/src/rgw/rgw_rest_s3.h:575").call
process("/root/ceph/build/bin/radosgw").function("is_acl_op@/root/ceph/src/rgw/rgw_rest_s3.h:569").call
process("/root/ceph/build/bin/radosgw").function("is_tagging_op@/root/ceph/src/rgw/rgw_rest_s3.h:572").call
process("/root/ceph/build/bin/radosgw").function("do_read_permissions@/root/ceph/src/rgw/rgw_op.cc:7006").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("init_quota@/root/ceph/src/rgw/rgw_op.cc:942").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("verify_op_mask@/root/ceph/src/rgw/rgw_op.cc:781").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("verify_permission@/root/ceph/src/rgw/rgw_op.cc:3090").call
process("/root/ceph/build/bin/radosgw").function("get_params@/root/ceph/src/rgw/rgw_rest_s3.cc:1270").call
process("/root/ceph/build/bin/radosgw").function("create_s3_policy@/root/ceph/src/rgw/rgw_rest_s3.cc:1100").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("pre_exec@/root/ceph/src/rgw/rgw_op.cc:3342").call
process("/root/ceph/build/bin/radosgw").function("rgw_bucket_object_pre_exec@/root/ceph/src/rgw/rgw_op.cc:710").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("execute@/root/ceph/src/rgw/rgw_op.cc:3463").call
process("/root/ceph/build/bin/radosgw").function("select_processor@/root/ceph/src/rgw/rgw_op.cc:3314").call
process("/root/ceph/build/bin/radosgw").function("get_encrypt_filter@/root/ceph/src/rgw/rgw_rest_s3.cc:1503").call
process("/root/ceph/build/bin/radosgw").function("get_data@/root/ceph/src/rgw/rgw_rest_s3.cc:1382").call
process("/root/ceph/build/bin/radosgw").function("get_data@/root/ceph/src/rgw/rgw_rest_s3.cc:1382").call
process("/root/ceph/build/bin/radosgw").function("do_aws4_auth_completion@/root/ceph/src/rgw/rgw_op.cc:923").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("do_aws4_auth_completion@/root/ceph/src/rgw/rgw_op.cc:923").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("populate_with_generic_attrs@/root/ceph/src/rgw/rgw_op.cc:2606").call
process("/root/ceph/build/bin/radosgw").function("dispose_processor@/root/ceph/src/rgw/rgw_op.cc:3337").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("send_response@/root/ceph/src/rgw/rgw_rest_s3.cc:1406").call
process("/root/ceph/build/bin/radosgw").function("generate_cors_headers@/root/ceph/src/rgw/rgw_op.cc:1083").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("~RGWPutObj_ObjStore_S3@/root/ceph/src/rgw/rgw_rest_s3.h:210").call
process("/root/ceph/build/bin/radosgw").function("~RGWPutObj_ObjStore_S3@/root/ceph/src/rgw/rgw_rest_s3.h:210").call
process("/root/ceph/build/bin/radosgw").function("~RGWHandler_REST_Obj_S3@/root/ceph/src/rgw/rgw_rest_s3.h:588").call
process("/root/ceph/build/bin/radosgw").function("~RGWHandler_REST_Obj_S3@/root/ceph/src/rgw/rgw_rest_s3.h:588").call
process("/root/ceph/build/bin/radosgw").function("~RGWHandler_REST_S3@/root/ceph/src/rgw/rgw_rest_s3.h:510").call
process("/root/ceph/build/bin/radosgw").function("~RGWHandler@/root/ceph/src/rgw/rgw_op.cc:6979").call
```


参考https://medium.com/fcamels-notes/%E7%94%A8-systemtap-%E8%BF%BD%E8%B8%AA-user-space-%E7%A8%8B%E5%BC%8F%E5%9F%B7%E8%A1%8C%E7%9A%84%E6%B5%81%E7%A8%8B-2d0b116dcf20
```
probe begin {
  printf("ready\n");
}

probe process("/root/CLionProjects/testmylib2/liblibmy.so").statement("*@library.cpp:*") {
  printf("%s\n", pp());
}
```


```
probe begin {
  printf("ready\n");
}

global indent = 4;
probe process("/root/CLionProjects/testmylib2/liblibmy.so").function("*").call {
  printf("%s -> %s: %s\n", thread_indent(indent), ppfunc(), $$parms);
}
probe process("/root/CLionProjects/testmylib2/liblibmy.so").function("*").return {
  printf("%s <- %s\n", thread_indent(-indent), ppfunc());
}
```
