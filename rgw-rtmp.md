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
