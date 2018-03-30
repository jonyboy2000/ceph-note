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
