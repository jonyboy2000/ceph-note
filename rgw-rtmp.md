implment like alioss rtmp push video stream to s3
```
rtmp://testyuliyang.oss-cn-shanghai.aliyuncs.com/live
test-channel3?OSSAccessKeyId=xxxxxxxxxxx&playlistName=playlist.m3u8&Expires=1513858333&Signature=yyyyyyyyyyyyy
```
custom rtmp auth

```
# -*- coding: utf-8 -*-

# base64(hmac-sha1(AccessKeySecret,
#     + Expires + "\n"
#     + "/BucketName/ChannelName"))

import hmac
from hashlib import sha1 as sha
from base64 import encodestring
h = hmac.new("secret-key", "Expires"+"\n"+"/BucketName/ChannelName", digestmod=sha)
print encodestring(h.digest()).strip()   #sr6/RWeRrnzciFO9xYXZHWMimlA=
```

```
import hmac
from hashlib import sha1 as sha
from base64 import encodestring
access_key = "GVXDWEABA4CO2DSA2CPH"
secret_key = "lhV5DfiUPoNKL1IeF6BwUEuFXobEFmuz1iuw03XB"
Expires = str(1534842631)
Bucket = "rtmptest1"
Channel = "channel002"
h = hmac.new(str(secret_key), Expires + "\n" + "/%s/%s" % (Bucket, Channel), digestmod=sha)
res = encodestring(h.digest()).strip()
Signature = res.replace('/','z')
cmd = '''ffmpeg -re -i test.flv -vcodec libx264 -vprofile baseline -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 640x480 -q 10 "rtmp://192.168.153.1:1935/hls/%s?Bucket=%s&AccessKeyId=%s&Expires=%s&Signature=%s"''' % (Channel, Bucket, access_key, Expires, Signature)
print cmd
```

```
ffmpeg -re -i test.flv -vcodec libx264 -vprofile baseline -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 640x480 -q 10 "rtmp://192.168.153.1:1935/hls/channel002?Bucket=rtmptest1&AccessKeyId=GVXDWEABA4CO2DSA2CPH&Expires=1534842631&Signature=tN57NoNVznJMypH+Pu3HtBKQm+U="
```

```
生成直播观流地址
#!/usr/bin/env python
import base64, hmac, os, sha, sys, time, urllib

TWENTY_YEARS_IN_SECONDS = 60 * 60 * 24 * 365 * 20
aws_access_key_id = "GVXDWEABA4CO2DSA2CPH"
aws_secret_access_key = "lhV5DfiUPoNKL1IeF6BwUEuFXobEFmuz1iuw03XB"
resource = "/rtmptest1/channel002/index.m3u8"
seconds_alive = TWENTY_YEARS_IN_SECONDS

# Computations:
expires = int(time.time()) + seconds_alive
resource = urllib.quote(resource)
raw_value = "GET\n\n\n{0}\n{1}".format(expires, resource)
signature = base64.b64encode(hmac.new(aws_secret_access_key, raw_value, sha).digest())

# Result:
#10.152.11.36 为rgw地址

print "http://10.152.11.36{0}?AWSAccessKeyId={1}&Expires={2}&Signature={3}".format(
    resource, urllib.quote(aws_access_key_id), expires, urllib.quote(signature))
    
http://10.152.11.36/rtmptest1/channel002/index.m3u8?AWSAccessKeyId=GVXDWEABA4CO2DSA2CPH&Expires=2165554749&Signature=gw9qRSiwf3KXz5/0QsY3lUVuY6c%3D
```

```
删除点播地址
from boto3.session import Session
import boto3
import time
import base64, hmac, sha, time, urllib

TWENTY_YEARS_IN_SECONDS = 60 * 60 * 24 * 365 * 20

access_key = "yly"
secret_key = "yly"

Bucket = "rtmp"
Channel = "channel002"
Vod = "vod.m3u8"

Marker = "1535251714320"
Marker_end = "1535251746077"

url = 'http://10.254.3.68'

session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url)
paginator = s3_client.get_paginator('list_objects')

operation_parameters = {'Bucket': Bucket,
                        'Prefix': Channel + '/',
                        'Marker': Channel + '/' + Marker
                        }
bucket_object_list = []
durations = []
maxduration = 0
page_iterator = paginator.paginate(**operation_parameters)
for page in page_iterator:
    for key in page['Contents']:
        keyString = key["Key"]
        resource = '/' + Bucket + '/' + keyString
        if resource > str('/' + Bucket + '/' + Channel + '/' + Marker_end):
            break
        seconds_alive = TWENTY_YEARS_IN_SECONDS
        expires = int(time.time()) + seconds_alive
        resource = urllib.quote(resource)
        raw_value = "GET\n\n\n{0}\n{1}".format(expires, resource)
        signature = base64.b64encode(hmac.new(secret_key, raw_value, sha).digest())
        signed_url = "{0}{1}?AWSAccessKeyId={2}&Expires={3}&Signature={4}".format(url,
                                                                                  resource, urllib.quote(access_key),
                                                                                  expires, urllib.quote(signature))
        res = s3_client.head_object(Bucket=Bucket, Key=keyString)
        try:
            if res['Metadata']['extinf'] >= maxduration:
                maxduration = res['Metadata']['extinf']
            durations.append("#EXTINF:%s\n%s\n" % (res['Metadata']['extinf'], signed_url))
        except Exception as e:
            print "not found duration for %s" % (keyString,)

# print durations

vod_str = '''#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:1
#EXT-X-TARGETDURATION:%s\n''' % (maxduration,)

for duration in durations:
    vod_str += duration

if s3_client.put_object(Bucket = Bucket,Key= Channel + '/' +Vod, Body = vod_str)['ResponseMetadata']['HTTPStatusCode'] == 200:
    print "gen vod success"
else:
    print "gen vod failed"

```

genarated exp vod.m3u8
```
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:1
#EXT-X-TARGETDURATION:5.000
#EXTINF:5.000
http://10.254.3.68/rtmp/channel002/1535251714336.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=i2UsXTCqqXrG7bYIgjkudsjGzI8%3D
#EXTINF:4.000
http://10.254.3.68/rtmp/channel002/1535251719320.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=nIUnQut2OyZfSsi7YYTU9cTbzsk%3D
#EXTINF:3.680
http://10.254.3.68/rtmp/channel002/1535251723315.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=p2KT5jgZlf8jiWhrb%2BDVvHxdZzc%3D
#EXTINF:2.080
http://10.254.3.68/rtmp/channel002/1535251727016.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=m3G3%2BB0eZWhaTGsNbOcvg12d8B8%3D
#EXTINF:3.640
http://10.254.3.68/rtmp/channel002/1535251729081.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=bnmCWJNt4xf9J6Ly5%2BIteXF2n4Y%3D
#EXTINF:2.080
http://10.254.3.68/rtmp/channel002/1535251732720.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=HeQCZVs85yJB1ufOoXLlfKmMJIA%3D
#EXTINF:3.280
http://10.254.3.68/rtmp/channel002/1535251734812.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=G/xISnCGZSU%2BqDtPKCm9Z8qnL8I%3D
#EXTINF:2.680
http://10.254.3.68/rtmp/channel002/1535251738091.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=Qkw1UABHI0f60CMCNKwPYX89otY%3D
#EXTINF:2.120
http://10.254.3.68/rtmp/channel002/1535251740757.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=nZlJyC8wiIpnkNuM7j%2BCoNK4pRQ%3D
#EXTINF:3.200
http://10.254.3.68/rtmp/channel002/1535251742895.ts?AWSAccessKeyId=yly&Expires=2166135917&Signature=jw7ogx2f1IzVWaKkhlEAcB0ovOs%3D

```
