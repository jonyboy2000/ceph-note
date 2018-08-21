implment like
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
生成观流地址
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
print "http://10.152.11.36{0}?AWSAccessKeyId={1}&Expires={2}&Signature={3}".format(
    resource, urllib.quote(aws_access_key_id), expires, urllib.quote(signature))
    
http://10.152.11.36:8081/rtmptest1/channel002/index.m3u8?AWSAccessKeyId=GVXDWEABA4CO2DSA2CPH&Expires=2165554749&Signature=gw9qRSiwf3KXz5/0QsY3lUVuY6c%3D
```
