
## multipart copy upload
```
# -*- coding: utf-8 -*-
import math
from boto3.session import Session
import boto3
access_key = ""
secret_key = ""
url = "http://s3.amazonaws.com"
session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url)

src_bucket = "wzyuliyangbucket01"
src_obj = "15M"
dest_bucket = "wzyuliyangbucket01"
dest_obj = "copy"

objectSize = s3_client.head_object(Bucket=src_bucket, Key=src_obj)['ContentLength']
mpu = s3_client.create_multipart_upload(Bucket=dest_bucket, Key=dest_obj, StorageClass='STANDARD_IA')
psize = 10 * 1024 * 1024
part_info = {
    'Parts': []
}
bytePosition = 0
i = 1
while bytePosition < objectSize:
    lastbyte = bytePosition + psize - 1
    if lastbyte >= objectSize:
        lastbyte = objectSize - 1
    print "mp.copy_part_from_key part %d (%d %d)" % (i, bytePosition, lastbyte)
    res = s3_client.upload_part_copy(Bucket=dest_bucket, CopySource=src_bucket+"/"+src_obj,
                                     CopySourceRange='bytes=%d-%d'%(bytePosition,lastbyte),
                                     Key=dest_obj,
                                     PartNumber=i, UploadId=mpu["UploadId"])
    part_info['Parts'].append({
        'PartNumber': i,
        'ETag': res['CopyPartResult']['ETag']
    })
    i = i + 1
    bytePosition += psize
s3_client.complete_multipart_upload(Bucket=dest_bucket, Key=dest_obj, UploadId=mpu["UploadId"], MultipartUpload=part_info)
```


## copy object
```
from boto3.session import Session
import boto3
access_key = "yly"
secret_key = "yly"
session = Session(access_key, secret_key)
url = "http://127.0.0.1"
config_dict = { 'signature_version' : 's3', 'connect_timeout': 30000, 'read_timeout': 30000}
config = boto3.session.Config(**config_dict)
s3_client = session.client('s3', endpoint_url=url, config=config)
print s3_client.copy_object(Bucket="test1", Key="obj_to_ia2", CopySource=str('test1'+'/'+"obj"), StorageClass='STANDARD_IA')
```

## multipart

```
from boto3.session import Session
import boto3
import botocore
access_key = "yly"
secret_key = "yly"
session = Session(access_key, secret_key)
url = "http://127.0.0.1"
config_dict = { 'signature_version' : 's3', 'connect_timeout': 30000, 'read_timeout': 30000}
config = boto3.session.Config(**config_dict)
s3_client = session.client('s3', endpoint_url=url, config=config)
mpu = s3_client.create_multipart_upload(Bucket="test1",Key="m1", StorageClass='STANDARD_IA')
part_info = {
    'Parts': []
}
print mpu["UploadId"]

```

```
from boto3.session import Session
import boto3

access_key = "yly"
secret_key = "yly"
url = "http://127.0.0.1"
session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url, config = boto3.session.Config(
         signature_version = 's3'
    ))

# s3_client.create_bucket(Bucket="onest-storage-class")
# print [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]


mpu = s3_client.create_multipart_upload(Bucket="onest-storage-class",Key="multi", StorageClass='STANDARD_IA')
part_info = {
    'Parts': []
}

data = open('5M','rb').read()
response = s3_client.upload_part(Bucket="onest-storage-class", Key="multi", PartNumber=1, UploadId=mpu["UploadId"],Body=data)
part_info['Parts'].append({
    'PartNumber': 1,
    'ETag': response['ETag']
})

s3_client.complete_multipart_upload(Bucket="onest-storage-class",Key="multi",UploadId=mpu["UploadId"], MultipartUpload=part_info)

```

## post object
```
#!/usr/bin/python
from boto3.session import Session
import boto3
import botocore
botocore.session.Session().set_debug_logger()
bucketname = 'onest-storage-class'
objectname = 'prefix/keyv6'
access_key = "yly"
secret_key = "yly"
url = "http://127.0.0.1"

session = Session(access_key, secret_key)
s3_client = session.client(
    's3',
    endpoint_url=url,
    use_ssl = False,
)
import ipdb; ipdb.set_trace() # BREAKPOINT

conditions = [
    ["starts-with", "$Content-Type", "image/"],
    ["starts-with", "$key", "prefix/"],
    {'x-amz-storage-class': 'STANDARD_IA'},
    # {"success_action_redirect": "http://www.baidu.com"},
    ["content-length-range", 0, 20000000],
]
form_data = s3_client.generate_presigned_post(
    Conditions = conditions,
    Bucket = bucketname,
    Key=objectname
)

form_data["fields"]['Content-Type'] = 'image/png'
form_data["fields"]['key'] = objectname
form_data["fields"]['x-amz-storage-class'] = 'STANDARD_IA'
# form_data["fields"]['success_action_redirect'] = 'http://www.baidu.com'
files = {"file": open('5M','rb')}

import requests
import logging
from requests_toolbelt.utils import dump
logging.basicConfig(level=logging.DEBUG)

response = requests.post(form_data["url"], data=form_data["fields"], files=files)
data = dump.dump_all(response)
print(data.decode('utf-8'))

```
