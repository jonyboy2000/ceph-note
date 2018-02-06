
```
import requests
import logging
from requests_toolbelt.utils import dump
logging.basicConfig(level=logging.DEBUG)
access_key = 'yly'
secret_key = 'yly'
url = 'http://test1.eos.cloud.com:8000/obj1'
response = requests.put(url, auth=S3Auth(access_key, secret_key,service_url='eos.cloud.com:8000'),data='''1234567890''')
data = dump.dump_all(response)
print(data.decode('utf-8'))
```
