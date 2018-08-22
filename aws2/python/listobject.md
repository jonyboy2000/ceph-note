```
from boto3.session import Session
import boto3
import time
import base64, hmac, os, sha, sys, time, urllib
TWENTY_YEARS_IN_SECONDS = 60 * 60 * 24 * 365 * 20
access_key = "yly"
secret_key = "yly"
Bucket = "rtmp"
Channel = "channel002"

Marker =     "1534863870730"
Marker_end = "1534863875109"
url = 'http://10.254.3.68'
session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url )
paginator = s3_client.get_paginator('list_objects')

operation_parameters = {'Bucket': Bucket,
                        'Prefix': Channel + '/',
                        'Marker': Channel + '/' + Marker
                        }
bucket_object_list = []
page_iterator = paginator.paginate(**operation_parameters)
for page in page_iterator:
  for key in page['Contents']:
    keyString = key[ "Key" ]
    resource = '/' + Bucket + '/' +keyString
    if resource > str('/' + Bucket + '/' + Channel +'/' + Marker_end):
      break
    seconds_alive = TWENTY_YEARS_IN_SECONDS
    expires = int(time.time()) + seconds_alive
    resource = urllib.quote(resource)
    raw_value = "GET\n\n\n{0}\n{1}".format(expires, resource)
    signature = base64.b64encode(hmac.new(secret_key, raw_value, sha).digest())
    signed_url = "{0}{1}?AWSAccessKeyId={2}&Expires={3}&Signature={4}".format(url,
    resource, urllib.quote(access_key), expires, urllib.quote(signature))
    bucket_object_list.append(signed_url)

print bucket_object_list

```
