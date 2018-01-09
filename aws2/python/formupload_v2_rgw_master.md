
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
