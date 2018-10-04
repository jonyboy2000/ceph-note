
```
yum install http://ftp.riken.jp/Linux/cern/centos/7.2/updates/Debug/x86_64/kernel-debuginfo-3.10.0-327.el7.x86_64.rpm http://ftp.riken.jp/Linux/cern/centos/7.2/updates/Debug/x86_64/kernel-debuginfo-common-x86_64-3.10.0-327.el7.x86_64.rpm
```

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
