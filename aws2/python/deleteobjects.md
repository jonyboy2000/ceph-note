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


```
from boto3.session import Session
import os
import json
import boto3
access_key = "yly"
secret_key = "yly"
url = "http://127.0.0.1:7480"
session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url )
objects = []
objects.append({'VersionId': "zBUePDrBv4mVhCie0fQoEa4DSnsyJa3",'Key': "1.txt"})
objects.append({'VersionId': "K3S6A3r.2ScTjVqL56ImO.EdOblpbxI",'Key': "1.txt"})
print s3_client.delete_objects(Bucket="test2", Delete={'Objects':objects})
```
