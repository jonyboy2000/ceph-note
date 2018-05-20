# 认证
```
./radosgw-admin realm  create --rgw-realm=default
./radosgw-admin zonegroup modify  --rgw-zonegroup=default  --rgw-realm=default  --master
./radosgw-admin zone  modify  --rgw-zone=default --rgw-zonegroup=default  --rgw-realm=default  --master
./radosgw-admin zone placement add --rgw-zone=default --placement-id=new   --index-pool default.rgw.buckets.index  --data-pool new.rgw.buckets.data  --data-extra-pool=new.rgw.buckets.non-ec
./ceph osd pool create new.rgw.buckets.data 8 8
./ceph osd pool create new.rgw.buckets.non-ec 8 8
./radosgw-admin zonegroup placement add --rgw-zonegroup=default --placement-id=new
./radosgw-admin zonegroup placement modify --rgw-zonegroup=default --placement-id=new  --tags="authuser"

[root@yuliyang src]# s3cmd mb s3://test2 --bucket-location=:new
ERROR: Access to bucket 'test2' was denied
ERROR: S3 error: 403 (AccessDenied)
./radosgw-admin metadata get user:yly | jq '.data.placement_tags = ["authuser"]' > /tmp/json
./radosgw-admin metadata put user:yly < /tmp/json

s3cmd mb s3://test2 --bucket-location=:new
./radosgw-admin bucket stats --bucket=test2
```
