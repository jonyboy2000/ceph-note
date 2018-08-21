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
