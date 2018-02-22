```
#!/usr/bin/python
from boto3.session import Session
import boto3

import requests
import logging
from requests_toolbelt.utils import dump
logging.basicConfig(level=logging.DEBUG)

bucketname = 'bucketname'

access_key = ""
secret_key = ""
url = "http://s3.amazonaws.com"
session = Session(access_key, secret_key)
s3_client = session.client('s3',endpoint_url=url,use_ssl = False,config = boto3.session.Config(signature_version = 's3v4'))

success_action_redirect = "http://www.baidu.com"
conditions = [
    {"acl": "public-read"},
    ["starts-with", "$Content-Type", "image/"],
#    ["starts-with", "$key", "prefix/"],
    {"success_action_redirect": success_action_redirect },
    ["content-length-range", 0, 20000000],
]

objectname = 'prefix/keyv4'

form_data = s3_client.generate_presigned_post(
    Conditions = conditions,
    Bucket = bucketname,
  #  Key = "prefix/" + '${filename}',
    Key = objectname,
    ExpiresIn = 3600,
    Fields={"acl": "public-read"}
)

form_data["fields"]['Content-Type'] = 'image/png'
form_data["fields"]['key'] = objectname
form_data["fields"]['success_action_redirect'] = success_action_redirect
files = {"file": "this_is_file_content_!!!!!"}

response = requests.post(form_data["url"], data=form_data["fields"], files=files)
data = dump.dump_all(response)
print(data.decode('utf-8'))
```

success_action_status 测试
```
#!/usr/bin/python
from boto3.session import Session
import boto3

import requests
import logging
from requests_toolbelt.utils import dump
logging.basicConfig(level=logging.DEBUG)

bucketname = ''
objectname    = 'prefix/keyv4'

access_key = ""
secret_key = ""
url = "http://s3.amazonaws.com"
session = Session(access_key, secret_key)
s3_client = session.client('s3',endpoint_url=url,use_ssl = False,config = boto3.session.Config(signature_version = 's3v4'))

conditions = [
    ["starts-with", "$Content-Type", "image/"],
    ["starts-with", "$key", "prefix/"],
    {"success_action_status": '201'},
    ["content-length-range", 0, 20000000],
]
form_data = s3_client.generate_presigned_post(
    Conditions = conditions,
    Bucket = bucketname,
    Key = "prefix/" + '${filename}',
    ExpiresIn = 3600
)
form_data["fields"]['Content-Type'] = 'image/png'
form_data["fields"]['key'] = 'prefix/111222'
form_data["fields"]['success_action_status'] = '201'
files = {"file": "this_is_file_content_!!!!!"}

response = requests.post(form_data["url"], data=form_data["fields"], files=files)
data = dump.dump_all(response)
print(data.decode('utf-8'))
```
