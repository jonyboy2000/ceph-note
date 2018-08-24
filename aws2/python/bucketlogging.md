
```
s3cmd setacl s3://{存日志桶名字} --acl-grant=write:LogDeliver
s3cmd setacl s3://{存日志桶名字} --acl-grant=read_acp:LogDeliver
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
