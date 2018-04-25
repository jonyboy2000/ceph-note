```
pip install xmltodict  requests_aws
```

```
-*- coding: UTF-8 -*-
import requests
import xmltodict
from xmltodict import parse, unparse, OrderedDict
from awsauth import S3Auth

host = '127.0.0.1'
access_key = 'user001'
secret_key = 'user001'
bucketname = 'bucket1'
objectname = 'yyyyysssy'

#申请uploadId
cmd = '/%s/%s?uploads' % (bucketname,objectname)
url = 'http://%s%s' % (host,cmd)
response = requests.post(url, auth=S3Auth(access_key, secret_key,service_url=host))
UploadId = xmltodict.parse(response.content)['InitiateMultipartUploadResult']['UploadId']

#上传分块1
cmd = '/%s/%s?partNumber=1&uploadId=%s' % (bucketname,objectname,UploadId)
url = 'http://%s%s' % (host,cmd)
with open('5M', 'rb') as fin:
    data = fin.read()
response = requests.put(url, auth=S3Auth(access_key, secret_key,service_url=host),data=data)

#上传分块2
cmd = '/%s/%s?partNumber=2&uploadId=%s' % (bucketname,objectname,UploadId)
url = 'http://%s%s' % (host,cmd)
with open('5M', 'rb') as fin:
    data = fin.read()
response = requests.put(url, auth=S3Auth(access_key, secret_key,service_url=host),data=data)

#上传分块3
cmd = '/%s/%s?partNumber=3&uploadId=%s' % (bucketname,objectname,UploadId)
url = 'http://%s%s' % (host,cmd)
with open('5M', 'rb') as fin:
    data = fin.read()
response = requests.put(url, auth=S3Auth(access_key, secret_key,service_url=host),data=data)

cmd = '/%s/%s?uploadId=%s' % (bucketname,objectname,UploadId)
url = 'http://%s%s' % (host,cmd)
response = requests.delete(url, auth=S3Auth(access_key, secret_key,service_url=host))


#获取当前所有分块列表
#cmd = '/%s/%s?uploadId=%s' % (bucketname,objectname,UploadId)
#url = 'http://%s%s' % (host,cmd)
#response = requests.get(url, auth=S3Auth(access_key, secret_key,service_url=host))
#obj2 = []
#for i in xmltodict.parse(response.content)['ListPartsResult']['Part']:
#    obj2.append({'PartNumber': i['PartNumber'], 'ETag': i['ETag']})
#obj = {'CompleteMultipartUpload': OrderedDict((
#    ('Part',obj2),
#))}

#发送完成分块上传请求
#completeme = xmltodict.unparse(obj,full_document=False)

#cmd = '/%s/%s?uploadId=%s' % (bucketname,objectname,UploadId)
#url = 'http://%s%s' % (host,cmd)
#response = requests.post(url, auth=S3Auth(access_key, secret_key,service_url=host),data=completeme)

```


```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boto3.session import Session
from botocore.config import Config as boto3Config
import logging
import math
from multiprocessing import Pool
import os
import boto
from boto.s3.connection import S3Connection
import Queue, multiprocessing, signal
from multiprocessing.pool import ThreadPool

def generate(result):
   for chunk in iter(lambda: result['Body'].read(5*1024*1024), b''):
      yield chunk

session_src = Session("eos", "eos")
session_dst = Session("eos", "eos")

client_src = session_src.client('s3', endpoint_url="http://127.0.0.1",
                                config=boto3Config(connect_timeout=5,
                                              retries={'max_attempts': 5}))
client_dst = session_dst.client('s3', endpoint_url="http://127.0.0.1",
                                config=boto3Config(connect_timeout=5,
                                              retries={'max_attempts': 5}))
src_bucket = "largesource"
src_key = "10M"
dest_bucket = "largedest"
dest_key = "10M"
s3_response = client_src.get_object(Bucket=src_bucket, Key=src_key)
expect_etag = s3_response['ETag']
conn = boto.connect_s3(
        "eos",
        "eos",
        host='127.0.0.1',
        is_secure=False,
        port=80,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )

bucket = conn.get_bucket(dest_bucket)
mp = bucket.initiate_multipart_upload(dest_key)

def _upload_part(bucketname, aws_key, aws_secret, multipart_id, part_num, chunk):
    print 'Start uploading part #%d ...' % part_num
    client_dst.upload_part(
        Bucket=bucketname,
        Key=dest_key,
        PartNumber=part_num,
        UploadId=multipart_id,
        Body=chunk,
    )
    print 'Finish uploading part #%d ...' % part_num

pool = Pool(processes=multiprocessing.cpu_count())
for part_index, chunk in enumerate(generate(s3_response), start=1):
    print part_index, mp.id
    pool.apply_async(_upload_part, ["largedest", "eos", "eos", mp.id, part_index, chunk])


pool.close()
pool.join()

paginator = client_dst.get_paginator('list_parts')
part_iterator = paginator.paginate(Bucket='largedest',Key=dest_key,UploadId=mp.id)
part_info_dict = {'Parts': []}

for parts in part_iterator:
    for part in parts[u'Parts']:
        part_info_dict['Parts'].append({
            'PartNumber': part[u'PartNumber'],
            'ETag': part['ETag']
        })

completed_ctx = {
    'Bucket': "largedest",
    'Key': dest_key,
    'UploadId': mp.id,
    'MultipartUpload': part_info_dict
}
response = client_dst.complete_multipart_upload(**completed_ctx)
print response['ETag']

```
