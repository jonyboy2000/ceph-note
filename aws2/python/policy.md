
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
