
```
policy='''{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": [
      "arn:aws:s3:::test1/*"
    ],
    "Condition": {
        "StringLike": {
          "aws:Referer": "http://www.baidu.com/*"
        }
      }
  }]
}
'''
response = requests.put(url, auth=S3Auth(access_key, secret_key,service_url='10.144.91.36'),data=policy)



curl -o downfile -v http://10.144.91.36/test1/10M  --header "referer: http://www.baidu.com/1"
```



```
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"AWS":"arn:aws:iam:::user/yly2"},
    "Action": "s3:GetObject",
    "Resource": [
      "arn:aws:s3:::testpolicy/*"
    ],
    "Condition": {
        "StringLike": {
          "aws:Referer": "http://www.baidu.com/*"
        }
      }
  }]
}
```

```
ceph-request get '/testpolicy/1M' -c yly2.request.local.7480 --download dfile  --verbose --header '{"referer": "http://www.baidu.com/1"}'
< GET /testpolicy/1M HTTP/1.1
< Host: 127.0.0.1:7480
< Connection: keep-alive
< Accept-Encoding: gzip, deflate
< Accept: */*
< User-Agent: python-requests/2.18.4
< referer: http://www.baidu.com/1
< date: Wed, 29 Aug 2018 00:20:46 GMT
< Authorization: AWS yly2:7PPIvScG5/cDwN7s/VlE2YLe25A=
<

> HTTP/1.1 200 OK
> Content-Length: 1048576
> Accept-Ranges: bytes
> Last-Modified: Tue, 28 Aug 2018 23:36:50 GMT
> ETag: "b6d81b360a5672d80c27430f39153e2c"
> x-amz-meta-s3cmd-attrs: atime:1534468537/ctime:1529606992/gid:0/gname:root/md5:b6d81b360a5672d80c27430f39153e2c/mode:33188/mtime:1529606992/uid:0/uname:root
> x-amz-request-id: tx000000000000000000011-005b85e6de-5e27-default
> Content-Type: application/octet-stream
> Date: Wed, 29 Aug 2018 00:20:46 GMT
> Connection: Keep-Alive
>
```

