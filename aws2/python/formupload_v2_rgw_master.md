```
#!/usr/bin/python
from boto3.session import Session
import boto3
import botocore
botocore.session.Session().set_debug_logger()
bucketname = 'test2'
objectname = 'prefix/keyv6'
access_key = "yly"
secret_key = "yly"
url = "http://192.168.153.177:8000"
session = Session(access_key, secret_key)
s3_client = session.client(
    's3',
    endpoint_url=url,
    use_ssl = False,
)

conditions = [
    ["starts-with", "$Content-Type", "image/"],
    ["starts-with", "$key", "prefix/"],
    {"success_action_redirect": "http://www.baidu.com"},
    ["content-length-range", 0, 20000000],
]

form_data = s3_client.generate_presigned_post(
    Conditions = conditions,
    Bucket = bucketname,
    Key=objectname
)

form_data["fields"]['Content-Type'] = 'image/png'
form_data["fields"]['key'] = objectname
form_data["fields"]['success_action_redirect'] = 'http://www.baidu.com'
files = {"file": "this_is_file_content_!!!!!"}

import requests
import logging
from requests_toolbelt.utils import dump
logging.basicConfig(level=logging.DEBUG)

response = requests.post(form_data["url"], data=form_data["fields"], files=files)
data = dump.dump_all(response)
print(data.decode('utf-8'))
```

```
#!/usr/bin/python
from boto3.session import Session
import boto3
BUCKET = 'test222'
KEY    = 'key'
TEST_FILE = 'test-rgw-s3-aws2-form.html'
access_key = "yly3"
secret_key = "yly3"
url = "http://192.168.153.177:8000" 
session = Session(access_key, secret_key)
s3_client = session.client(
    's3',
    endpoint_url=url,
    use_ssl = False,
)
conditions = [
    ["content-length-range", 10, 1000000000]
]

form_data = s3_client.generate_presigned_post(
    Conditions = conditions,
    Bucket = BUCKET,
    Key = KEY
)

#files = {"file": "file_content"}
#response = requests.post(form_data["url"], data=form_data["fields"], files=files)

html = """\
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>
  <body>
      <form action="{url}" method="post" enctype="multipart/form-data">
""".format(url=form_data['url'])

for k, v in form_data['fields'].items():
	html += """
           <input type="hidden" name="{key}" value="{value}" />
        """.format(key=k,value=v)

html += """
      File:
      <input type="file"   name="file" /> <br />
    <input type="submit" name="submit" value="Upload to Amazon S3" />
  </form>
</html>
"""

file = open(TEST_FILE, "w")
file.write(html)
file.close()

print TEST_FILE + " created."

```


```

<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>
  <body>
      <form action="http://192.168.153.177:8000/test222" method="post" enctype="multipart/form-data">

           <input type="hidden" name="policy" value="eyJjb25kaXRpb25zIjogW1siY29udGVudC1sZW5ndGgtcmFuZ2UiLCAxMCwgMTAwMDAwMDAwMF0sIHsiYnVja2V0IjogInRlc3QyMjIifSwgeyJrZXkiOiAidGVzdC0xLTItMS1rZXkifV0sICJleHBpcmF0aW9uIjogIjIwMTgtMDEtMDlUMDk6MjM6MzZaIn0=" />
        
           <input type="hidden" name="AWSAccessKeyId" value="yly3" />
        
           <input type="hidden" name="key" value="test-1-2-1-key" />
        
           <input type="hidden" name="signature" value="9KCbU9Nxd+9mR/uP+bLGtu7NnYk=" />
        
      File:
      <input type="file"   name="file" /> <br />
    <input type="submit" name="submit" value="Upload to Amazon S3" />
  </form>
</html>

```

v4签名(非boto)版本
```
import datetime
import json
import hmac
import hashlib
import base64
import copy
import os
import sys

class Utils(object):
    @staticmethod
    def hmac(key, string, hex=False):
        try:
            hmac256 = hmac.new(key.encode() if isinstance(key, str) else key, msg=string.encode('utf-8') if isinstance(string, str) else string, digestmod=hashlib.sha256) # v3
        except Exception:
            hmac256 = hmac.new(key, msg=string, digestmod=hashlib.sha256) # v2

        return hmac256.hexdigest() if hex else hmac256.digest()

    @staticmethod
    def merge_dicts(a, b, path=None):
        aClone = copy.deepcopy(a);
        if path is None: path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    aClone[key] = Utils.merge_dicts(a[key], b[key], path + [str(key)])
                else:
                    aClone[key] = b[key]
            else:
                aClone[key] = b[key]
        return aClone

    @staticmethod
    def getExtension(filename):
        return os.path.splitext(filename)[1][1:]

    @staticmethod
    def getServerPath():
        return os.path.abspath(os.path.dirname(sys.argv[0]))

    @staticmethod
    def isFileValid(filename, mimetype, allowedExts, allowedMimeTypes):
        if not allowedExts or not allowedMimeTypes:
            return False

        extension = Utils.getExtension(filename)
        return extension.lower() in allowedExts and mimetype in allowedMimeTypes

    @staticmethod
    def isValid(validation, filePath, mimetype):
        if not validation:
            return True

        if callable(validation):
            return validation(filePath, mimetype)

        if isinstance(validation, dict):
            return Utils.isFileValid(filePath, mimetype, validation['allowedExts'], validation['allowedMimeTypes'])

        return False

bucket = "happybucket2"
region = "us-east-1"
keyStart = ""
acl = "public-read"
accessKeyId = "aaa"
secret = "bbb"

dateString = datetime.datetime.now().strftime("%Y%m%d") # Ymd format.
credential = '/'.join([accessKeyId, dateString, region, 's3/aws4_request'])
xAmzDate = dateString + 'T000000Z'

# Build policy.
policy = {
    # 5 minutes into the future
    'expiration': (datetime.datetime.now() + datetime.timedelta(minutes=60)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    'conditions': [
        {'bucket': bucket},
        ["starts-with", "$key", keyStart],
        {'acl': acl },
        {'x-amz-algorithm': 'AWS4-HMAC-SHA256'},
        {'x-amz-credential': credential},
        {'x-amz-date': xAmzDate}
    ],
}
# python 2-3 compatible:
try:
    policyBase64 = base64.b64encode(json.dumps(policy).encode()).decode('utf-8') # v3
except Exception:
    policyBase64 = base64.b64encode(json.dumps(policy)) # v2

dateKey = Utils.hmac('AWS4' + secret, dateString);
dateRegionKey = Utils.hmac(dateKey, region)
dateRegionServiceKey = Utils.hmac(dateRegionKey, 's3')
signingKey = Utils.hmac(dateRegionServiceKey, 'aws4_request')
signature = Utils.hmac(signingKey, policyBase64, True)

res = {
    'bucket': bucket,
    'region': 's3-' + region if region != 'us-east-1' else 's3',
    'keyStart': keyStart,
    'params': {
        'acl': acl,
        'policy': policyBase64,
        'x-amz-algorithm': 'AWS4-HMAC-SHA256',
        'x-amz-credential': credential,
        'x-amz-date': xAmzDate,
        'x-amz-signature': signature
    }
}
# print res

html = """
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>
  <body>
      <form action="{url}" method="post" enctype="multipart/form-data">
""".format(url='http://s3.amazonaws.com/happybucket2')
for k, v in res['params'].items():
        html += """
           <input type="hidden" name="{key}" value="{value}" />
        """.format(key=k,value=v)
html +="""
     """
html += '      <input type="hidden" name="key" value="%s${filename}" />' % (keyStart,)

html += """
      File:

      <input type="file"   name="file" /> <br />
    <input type="submit" name="submit" value="Upload to Amazon S3" />
  </form>
</html>
""".format(keyStart='http://s3.amazonaws.com/happybucket2')
file = open("form2.html", "w")
file.write(html)
file.close()
print " created."
```
