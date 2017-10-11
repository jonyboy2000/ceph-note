```
radosgw-admin realm  create --rgw-realm=default --default
radosgw-admin realm get-default
default realm: 5ac674fd-8e5d-4715-b973-c636e25583a9

ceph osd pool create default.rgw.buckets.data.tst 8 8
radosgw-admin pool add --pool default.rgw.buckets.data.tst
radosgw-admin zonegroup  modify --rgw-zonegroup=default --realm-id=5ac674fd-8e5d-4715-b973-c636e25583a9
radosgw-admin zone       modify --rgw-zonegroup=default  --rgw-zone=default --realm-id=5ac674fd-8e5d-4715-b973-c636e25583a9

radosgw-admin  zone      placement add --rgw-zone=default --placement-id=test --index_pool=default.rgw.buckets.index --data_pool=default.rgw.buckets.data.tst --data_extra_pool=default.rgw.buckets.non-ec 
radosgw-admin  zonegroup placement add --rgw-zonegroup=default --placement-id=test
#radosgw-admin zonegroup placement default --rgw-zonegroup=default --placement-id=test

radosgw-admin period update --commit --rgw-zone=default --rgw-zonegroup=default --rgw-realm=default
systemctl restart ceph-radosgw@rgw.yly-test-1
radosgw-admin period get --rgw-realm=default

s3cmd mb s3://bucket1 --bucket-location=:test
```
