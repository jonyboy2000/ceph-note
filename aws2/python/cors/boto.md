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
