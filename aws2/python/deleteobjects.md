```
# -*- coding: utf-8 -*-
import boto.s3.connection
# 导出桶下对象列表
# sudo radosgw-admin bucket list --bucket=tdk-bucket1 --format=json > objects
import json
data = json.loads(open('/root/objects','rb').read())
print data

myconn = boto.s3.connection.S3Connection(
    aws_access_key_id="admin1",
    aws_secret_access_key="admin1",
    host="10.139.11.90",
    is_secure=False,
    port=8000,
    calling_format=boto.s3.connection.OrdinaryCallingFormat())
mybucket = myconn.get_bucket("tdk-bucket1")

for d in data:
    if data[4][u'owner'] == "admin1":
        mybucket.delete_key(key_name=data[32][u'name'],version_id=data[4][u'instance'])
```
