
```
config = Config(connect_timeout=30000, read_timeout=30000, retries={'max_attempts': 0}, s3={'addressing_style': 'virtual')

#config_dict = { 'signature_version' : 's3', 'connect_timeout': 30000, 'read_timeout': 30000}
#config = boto3.session.Config(**config_dict)


client = session.client('s3', endpoint_url=url, config=config)
```

```
[root@promote ~]# cat  uploadbucket1.py
from boto3.session import Session
import botocore
botocore.session.Session().set_debug_logger()
import boto3
access_key = "yly"
secret_key = "yly"
url = 'http://eos-beijing-1.cmecloud.cn'
session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url)
resp = s3_client.put_object(Bucket="bucket1", Key="boto1bucket1obj", Body="111")
print resp
[root@promote ~]# cat ~/.aws/config
[default]
s3 =
    signature_version = s3
    addressing_style = virtual
```
