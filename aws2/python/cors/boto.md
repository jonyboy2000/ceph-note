```
import boto
import boto.s3.connection
boto.set_stream_logger('boto')
from boto.s3.key import Key
host = '10.139.13.205'  #J
access_key = 'yly'
secret_key = 'yly'
conn = boto.connect_s3(
                access_key,
                secret_key,
                host = host,
                is_secure = False,
                port=80,
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                )
bucket = conn.get_bucket("corsceph")
from boto.s3.cors import CORSConfiguration
cors_cfg = CORSConfiguration()
for i in range(1,102):
    cors_cfg.add_rule('GET', '*')

#bucket.set_cors(cors_cfg)
print bucket.get_cors()
```


```
#!/usr/bin/python
from boto3.session import Session
import boto3
access_key = "yly"
secret_key = "yly"
url = "http://10.139.12.23"
session = Session(access_key, secret_key)
s3_client = session.client(
    's3',
    endpoint_url=url,
    use_ssl = False,
    config = boto3.session.Config(
         signature_version = 's3v4'
    )
)
response = s3_client.put_bucket_cors(
            Bucket="public",
            CORSConfiguration={
                'CORSRules': [
                    {
                        'AllowedMethods': ['GET', 'PUT', 'DELETE'],
                        'AllowedOrigins': ['*'],
                        'AllowedHeaders': ['*'],
                    },
                ],
            },
        )
```
