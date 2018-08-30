
```
s3cmd setacl s3://{存日志桶名字} --acl-grant=write:LogDeliver
s3cmd setacl s3://{存日志桶名字} --acl-grant=read_acp:LogDeliver
```

```
s3cmd -c yly.s3cfg setacl s3://beijing2-logging-loop --acl-grant=write:bl_deliver
s3cmd -c yly.s3cfg setacl s3://beijing2-logging-loop --acl-grant=read_acp:bl_deliver

from boto3.session import Session
import boto3
access_key = "yly"
secret_key = "yly"
url = 'http://127.0.0.1:8083'
#url = 'http://172.20.243.26:8083'
session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url)
bl =  {
        'LoggingEnabled': {
            'TargetBucket': 'beijing2-logging-loop',
            'TargetPrefix': 'logs/'
        }
    }
print s3_client.put_bucket_logging(Bucket="beijing2-logging-loop", BucketLoggingStatus = bl)
```

```
bl =  {
        'LoggingEnabled': {
            'TargetBucket': '存日志桶名字',
            'TargetPrefix': '目录前缀/'
        }
    }
s3_client.put_bucket_logging(Bucket="桶名字", BucketLoggingStatus = bl)
```
