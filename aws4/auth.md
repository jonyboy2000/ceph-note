```
import urllib
print urllib.quote('!')

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

canonicalrequest = '''PUT
/alpha!soup/

host:s3.ecloud.today
user-agent:Boto/2.48.0 Python/2.7.5 Linux/3.10.0-693.11.6.el7.x86_64
x-amz-content-sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
x-amz-date:20180325T035121Z

host;user-agent;x-amz-content-sha256;x-amz-date
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'''

hsh = hashlib.sha256(canonicalrequest.encode())
canonical_request_hash = hsh.hexdigest()  # 8022bfe928617feede7994648f87933711ea8a747ae696acca56baa0a9fb9970


signing_key = getSignatureKey("s3testuser1","20180325","us-east-1","s3")
string_to_sign = '''AWS4-HMAC-SHA256
20180325T035121Z
20180325/us-east-1/s3/aws4_request'''+'\n'+canonical_request_hash

signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
print signature  # 30dcf3967d47efecbbe8bfe3f11180cb748e4ef66abf01d7649069bf350394ad

```


![Imgur](https://i.imgur.com/AiFCtPd.png)


```
import urllib
print urllib.quote('!')  # %21
```

```
import urllib
print urllib.quote('!')

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

canonicalrequest = '''PUT
/alpha%21soup/

host:s3.ecloud.today
user-agent:Boto/2.48.0 Python/2.7.5 Linux/3.10.0-693.11.6.el7.x86_64
x-amz-content-sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
x-amz-date:20180325T035121Z

host;user-agent;x-amz-content-sha256;x-amz-date
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'''

hsh = hashlib.sha256(canonicalrequest.encode())
canonical_request_hash = hsh.hexdigest()  # 8022bfe928617feede7994648f87933711ea8a747ae696acca56baa0a9fb9970


signing_key = getSignatureKey("s3testuser1","20180325","us-east-1","s3")
string_to_sign = '''AWS4-HMAC-SHA256
20180325T035121Z
20180325/us-east-1/s3/aws4_request'''+'\n'+canonical_request_hash

signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
print signature   #2fb2f06d245317d467b3dce4d02b86f53e3dfdbf57434ff542443fe238b3173a
```
